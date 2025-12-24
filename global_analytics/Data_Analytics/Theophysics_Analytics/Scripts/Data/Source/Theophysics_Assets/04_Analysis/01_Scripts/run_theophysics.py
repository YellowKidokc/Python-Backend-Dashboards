#!/usr/bin/env python3
import os, re, sqlite3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "07_Data" / "theophysics.db"
SRC_DIRS = [ROOT.parent/"topics", ROOT.parent/"notes"]
YAML_RE = re.compile(r'^---\n(.*?)\n---', re.DOTALL)

def parse_yaml(text):
    m = YAML_RE.search(text)
    if not m: return None, None
    yaml_text = m.group(0)
    d = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("-"):
            k,v = line.split(":",1)
            d[k.strip()] = v.strip()
    return d, yaml_text

def get_id(conn, table, field, value):
    cur = conn.execute(f"SELECT id FROM {table} WHERE {field}=?", (value,))
    row = cur.fetchone()
    return row[0] if row else None

def ensure(conn, table, **kv):
    fields = ",".join(kv.keys())
    qmarks = ",".join(["?"]*len(kv))
    try:
        conn.execute(f"INSERT INTO {table} ({fields}) VALUES ({qmarks})", tuple(kv.values()))
    except sqlite3.IntegrityError:
        pass

def main():
    conn = sqlite3.connect(DB)
    for pdir in SRC_DIRS:
        if not pdir.exists():
            continue
        for p in pdir.rglob("*.md"):
            text = p.read_text(encoding="utf-8", errors="ignore")
            meta, yml = parse_yaml(text)
            if not meta or "uid" not in meta:
                continue
            uid = meta["uid"]
            name = meta.get("name") or meta.get("title") or uid
            ntype = meta.get("type","atom")
            layer = meta.get("layer","info")
            coh = float(meta.get("coherence_score", "0") or 0.0)
            ensure(conn, "node_types", name=ntype)
            ensure(conn, "layers", name=layer.capitalize(), code=layer)
            type_id = get_id(conn, "node_types","name", ntype)
            layer_id = get_id(conn, "layers","code", layer)
            conn.execute("""
              INSERT INTO nodes(uid, name, type_id, layer_id, coherence_score, yaml)
              VALUES(?,?,?,?,?,?)
              ON CONFLICT(uid) DO UPDATE SET
                name=excluded.name,
                type_id=excluded.type_id,
                layer_id=excluded.layer_id,
                coherence_score=excluded.coherence_score,
                yaml=excluded.yaml
            """,(uid, name, type_id, layer_id, coh, yml))
    conn.commit()
    print("Synced notes -> DB")

if __name__ == "__main__":
    main()
