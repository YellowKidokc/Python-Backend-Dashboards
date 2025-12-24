"""
vault_refresh_v2.py
DUAL-LAYER SCANNING ARCHITECTURE
- GLOBAL: Single knowledge graph across entire vault
- LOCAL: Folder-aware context metadata for spatial intelligence

Key Features:
1. Scan zones: Define content regions (Logos Papers, Library, Glossary, etc.)
2. Folder context: Track file location for LOCAL dashboards
3. Content type detection: Paper, Note, Concept, Reference, etc.
4. Cross-domain linking: Connect files across folder boundaries
5. Adaptive indexing: Different metadata strategies per zone

Author: David Lowe / Claude
Date: 2025-11-18
"""

import os, re, sqlite3, hashlib, datetime, json
from pathlib import Path
from typing import Dict, Tuple, List, Optional, Set
from dataclasses import dataclass

DB_NAME = "theophysics.db"

# Regex patterns
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TITLE_RE = re.compile(r"^\s*#\s+(.*)$", re.MULTILINE)

# ═══════════════════════════════════════════════════════════════
# SCAN ZONE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

@dataclass
class ScanZone:
    """Defines a content region with specific indexing rules"""
    name: str
    pattern: str  # Regex to match folder paths
    content_type: str  # paper, note, concept, reference, glossary
    priority: int  # Higher priority zones override lower ones
    metadata_strategy: str  # full, minimal, glossary, reference

SCAN_ZONES = [
    # High-priority zones (specific folders)
    ScanZone("Logos Papers", r"03_PUBLICATIONS[\\/].*Logos.*", "paper", 100, "full"),
    ScanZone("Glossary", r"02_LIBRARY[\\/].*Glossary.*", "glossary", 90, "glossary"),
    ScanZone("Publications", r"03_PUBLICATIONS[\\/]", "paper", 80, "full"),
    ScanZone("Library", r"02_LIBRARY[\\/]", "note", 70, "full"),
    ScanZone("Inbox", r"01_INBOX[\\/]", "note", 60, "minimal"),
    
    # Vault system (scanned but not surfaced in dashboards)
    ScanZone("System", r"00_VAULT_SYSTEM[\\/]", "system", 50, "minimal"),
    
    # Default catch-all
    ScanZone("Unorganized", r".*", "note", 0, "full"),
]

def detect_zone(relative_path: str) -> ScanZone:
    """Determine which scan zone a file belongs to"""
    matched = [z for z in SCAN_ZONES if re.search(z.pattern, relative_path)]
    return max(matched, key=lambda z: z.priority) if matched else SCAN_ZONES[-1]

# ═══════════════════════════════════════════════════════════════
# DATABASE SCHEMA
# ═══════════════════════════════════════════════════════════════

def ensure_db(db_path: Path):
    """Create enhanced schema with LOCAL+GLOBAL support"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Core notes table with spatial metadata
    cur.execute("""CREATE TABLE IF NOT EXISTS notes(
        uid TEXT PRIMARY KEY,
        title TEXT,
        path TEXT,
        relative_path TEXT,
        folder_context TEXT,
        scan_zone TEXT,
        content_type TEXT,
        domain TEXT,
        tags TEXT,
        word_count INTEGER,
        hash TEXT,
        created_at TEXT,
        updated_at TEXT,
        metadata JSON
    )""")
    
    # Concepts table (unchanged)
    cur.execute("""CREATE TABLE IF NOT EXISTS concepts(
        concept TEXT PRIMARY KEY,
        mentions INTEGER DEFAULT 0,
        zones TEXT
    )""")
    
    # Co-mentions with zone tracking
    cur.execute("""CREATE TABLE IF NOT EXISTS co_mentions(
        concept1 TEXT,
        concept2 TEXT,
        count INTEGER,
        zones TEXT,
        PRIMARY KEY(concept1, concept2)
    )""")
    
    # Typed relationships
    cur.execute("""CREATE TABLE IF NOT EXISTS edges(
        src TEXT, 
        dst TEXT, 
        rel TEXT, 
        weight REAL,
        cross_zone INTEGER,
        PRIMARY KEY (src, dst, rel)
    )""")
    
    # Metrics (unchanged)
    cur.execute("""CREATE TABLE IF NOT EXISTS metrics(
        uid TEXT PRIMARY KEY, 
        SIS REAL, 
        LCS REAL, 
        SRI REAL
    )""")
    
    # New: Folder stats for LOCAL dashboards
    cur.execute("""CREATE TABLE IF NOT EXISTS folder_stats(
        folder_path TEXT PRIMARY KEY,
        scan_zone TEXT,
        file_count INTEGER,
        word_count INTEGER,
        concept_count INTEGER,
        updated_at TEXT
    )""")
    
    # Indexes for performance
    cur.execute("CREATE INDEX IF NOT EXISTS idx_notes_zone ON notes(scan_zone)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_notes_type ON notes(content_type)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_notes_folder ON notes(folder_context)")
    
    con.commit()
    con.close()

# ═══════════════════════════════════════════════════════════════
# METADATA EXTRACTION
# ═══════════════════════════════════════════════════════════════

def parse_frontmatter(md: str) -> Dict:
    """Minimal YAML-ish parser"""
    m = FRONTMATTER_RE.match(md)
    if not m:
        return {}
    blob = m.group(1)
    data = {}
    current_key = None
    for line in blob.splitlines():
        if re.match(r"^\s*#", line):
            continue
        kv = re.match(r"^\s*([A-Za-z0-9_\-]+)\s*:\s*(.*)\s*$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                items = [x.strip().strip(",") for x in val[1:-1].split(",") if x.strip()]
                data[key] = items
            elif val == "" or val == "|":
                data[key] = ""
                current_key = key
            else:
                data[key] = val
                current_key = key if val.endswith("|") else None
        elif current_key:
            data[current_key] = (data.get(current_key,"") + "\n" + line).strip()
    return data

def extract_title(md: str) -> str:
    m = TITLE_RE.search(md)
    return m.group(1).strip() if m else ""

def normalize_to_string(value) -> str:
    """Convert any value (including lists) to a string"""
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value if v)
    return str(value)

def sha1_text(txt: str) -> str:
    return hashlib.sha1(txt.encode("utf-8", errors="ignore")).hexdigest()

def words_count(md: str) -> int:
    body = re.sub(FRONTMATTER_RE, "", md)
    body = re.sub(r"`[^`]+`", " ", body)
    body = re.sub(r"\[\[.*?\]\]", " ", body)
    tokens = re.findall(r"[A-Za-z0-9']+", body)
    return len(tokens)

def discover_concepts(front: Dict, title: str, md: str) -> List[str]:
    """Extract concepts from tags, frontmatter, and title"""
    concepts = []
    
    # From tags
    tags = front.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    concepts += [t for t in tags if t]
    
    # From explicit concepts key
    extra = front.get("concepts", []) or front.get("key_concepts", [])
    if isinstance(extra, str):
        extra = [t.strip() for t in extra.split(",") if t.strip()]
    concepts += [t for t in extra if t]
    
    # From title (capitalized words)
    caps = re.findall(r"\b([A-Z][a-zA-Z\-]{2,})\b", title)
    concepts += caps
    
    # Normalize
    norm = []
    seen = set()
    for c in concepts:
        cc = re.sub(r'[^A-Za-z0-9\-]+', '-', c.strip()).strip('-').lower()
        if cc and cc not in seen:
            seen.add(cc)
            norm.append(cc)
    return norm

def generate_uid(relative_path: Path, front: Dict) -> str:
    """Generate UID from path or use existing frontmatter UID"""
    if "uid" in front:
        return front["uid"]
    parts = [s for s in relative_path.parts if s]
    return "UID-" + "-".join(re.sub(r'[^A-Za-z0-9]+','',x)[:8].upper() for x in parts)

# ═══════════════════════════════════════════════════════════════
# SCANNING LOGIC
# ═══════════════════════════════════════════════════════════════

def upsert_note(con: sqlite3.Connection, row: Tuple):
    """Insert or update note with full metadata"""
    cur = con.cursor()
    cur.execute("""INSERT INTO notes(
        uid, title, path, relative_path, folder_context, scan_zone, content_type,
        domain, tags, word_count, hash, created_at, updated_at, metadata
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT(uid) DO UPDATE SET
        title=excluded.title,
        path=excluded.path,
        relative_path=excluded.relative_path,
        folder_context=excluded.folder_context,
        scan_zone=excluded.scan_zone,
        content_type=excluded.content_type,
        domain=excluded.domain,
        tags=excluded.tags,
        word_count=excluded.word_count,
        hash=excluded.hash,
        updated_at=excluded.updated_at,
        metadata=excluded.metadata
    """, row)

def add_concepts(con: sqlite3.Connection, concepts: List[str], zone: str):
    """Track concepts with zone information"""
    if not concepts:
        return
    cur = con.cursor()
    for c in concepts:
        cur.execute("""INSERT INTO concepts(concept, mentions, zones) 
                      VALUES (?,1,?)
                      ON CONFLICT(concept) DO UPDATE SET 
                          mentions = mentions + 1,
                          zones = CASE 
                              WHEN zones LIKE '%' || ? || '%' THEN zones
                              ELSE zones || ',' || ?
                          END
                    """, (c, zone, zone, zone))

def scan_vault(vault_dir: Path, db_path: Path, verbose: bool = False) -> Dict:
    """
    Scan entire vault with LOCAL+GLOBAL intelligence
    Returns: Statistics dictionary
    """
    ensure_db(db_path)
    con = sqlite3.connect(db_path)
    
    stats = {
        "total_files": 0,
        "by_zone": {},
        "by_type": {},
        "folders": set()
    }
    
    for root, _, files in os.walk(vault_dir):
        for f in files:
            if not f.lower().endswith(".md"):
                continue
                
            p = Path(root) / f
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                try:
                    text = p.read_text(encoding="latin-1")
                except Exception:
                    if verbose:
                        print(f"⚠️  Cannot read: {p}")
                    continue
            
            # Extract metadata
            front = parse_frontmatter(text)
            
            # Normalize fields that might be lists in YAML
            title = normalize_to_string(front.get("title")) or extract_title(text) or p.stem
            domain = normalize_to_string(front.get("domain") or front.get("layer") or "meta").lower()
            
            # Determine spatial context
            relative_path = p.relative_to(vault_dir)
            folder_context = str(relative_path.parent)
            zone = detect_zone(str(relative_path))
            
            # Tags
            tags = front.get("tags", [])
            if isinstance(tags, list):
                tags_str = ",".join(tags)
            else:
                tags_str = str(tags)
            
            # Metrics
            wc = words_count(text)
            h = sha1_text(text)
            uid = generate_uid(relative_path, front)
            
            # Timestamps
            mtime = p.stat().st_mtime
            created = datetime.datetime.fromtimestamp(p.stat().st_ctime).isoformat(timespec="seconds")
            updated = datetime.datetime.fromtimestamp(mtime).isoformat(timespec="seconds")
            
            # Store additional metadata as JSON (normalize lists)
            metadata = json.dumps({
                "author": normalize_to_string(front.get("author")),
                "year": normalize_to_string(front.get("year")),
                "relevance": normalize_to_string(front.get("relevance")),
                "supports": normalize_to_string(front.get("supports")),
                "challenges": normalize_to_string(front.get("challenges"))
            })
            
            # Insert/update note
            upsert_note(con, (
                uid, title, str(p), str(relative_path), folder_context,
                zone.name, zone.content_type, domain, tags_str, wc, h,
                created, updated, metadata
            ))
            
            # Extract and track concepts
            concepts = discover_concepts(front, title, text)
            add_concepts(con, concepts, zone.name)
            
            # Update stats
            stats["total_files"] += 1
            stats["by_zone"][zone.name] = stats["by_zone"].get(zone.name, 0) + 1
            stats["by_type"][zone.content_type] = stats["by_type"].get(zone.content_type, 0) + 1
            stats["folders"].add(folder_context)
            
            if verbose and stats["total_files"] % 100 == 0:
                print(f"✓ Indexed {stats['total_files']} files...")
    
    con.commit()
    con.close()
    
    return stats

# ═══════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Vault-wide scanner with LOCAL+GLOBAL intelligence")
    ap.add_argument("--vault", required=True, help="Path to Obsidian vault root")
    ap.add_argument("--db", default=str(Path(__file__).resolve().parent / "theophysics.db"))
    ap.add_argument("--verbose", "-v", action="store_true", help="Show detailed progress")
    args = ap.parse_args()
    
    vault_path = Path(args.vault)
    db_path = Path(args.db)
    
    print(f"🔍 Scanning vault: {vault_path}")
    print(f"💾 Database: {db_path}\n")
    
    stats = scan_vault(vault_path, db_path, verbose=args.verbose)
    
    print(f"\n✅ Scan complete!")
    print(f"   Total files: {stats['total_files']}")
    print(f"   Unique folders: {len(stats['folders'])}")
    print(f"\n📊 By Zone:")
    for zone, count in sorted(stats['by_zone'].items(), key=lambda x: -x[1]):
        print(f"      {zone}: {count}")
    print(f"\n📝 By Type:")
    for ctype, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
        print(f"      {ctype}: {count}")

if __name__ == "__main__":
    main()
