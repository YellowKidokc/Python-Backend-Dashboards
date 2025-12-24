---
cssclass: dashboard-adaptive
tags:
- meta
- dashboard
- auto-scope
scope: auto
display_mode: detailed
uuid: 1acfe9d9-57ec-5021-a93d-56679a4a6c11
title: 📊 ADAPTIVE DASHBOARD
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\ADAPTIVE_DASHBOARD.md
uuid_generated_at: '2025-11-22T01:23:02.805376'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

# 📊 ADAPTIVE DASHBOARD
## Context-Aware Analytics Engine

```dataviewjs
// ═══════════════════════════════════════════════════════════
// AUTO-DETECT SCOPE
// ═══════════════════════════════════════════════════════════
const currentFolder = dv.current().file.folder;
const isRootLevel = currentFolder === "" || currentFolder === ".";
const scopeName = isRootLevel ? "GLOBAL (Entire Vault)" : `LOCAL (${currentFolder})`;

dv.header(2, `📍 Current Scope: ${scopeName}`);
dv.paragraph(`*Dashboard automatically adjusts metrics based on location*`);
dv.paragraph(`**Last Updated:** ${new Date().toLocaleString()}`);
```

---

## 📈 SCOPE STATISTICS

### File Counts by Type
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';

const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

// Group by content_type
const byType = {};
for (let p of pages) {
    const type = p.content_type || p.type || "unclassified";
    byType[type] = (byType[type] || 0) + 1;
}

if (Object.keys(byType).length > 0) {
    dv.table(
        ["Content Type", "Count", "% of Scope"],
        Object.entries(byType)
            .sort((a,b) => b[1] - a[1])
            .map(([type, count]) => [
                type,
                count,
                `${Math.round(100 * count / pages.length)}%`
            ])
    );
} else {
    dv.paragraph("*No files found in current scope*");
}
```

### Zone Distribution (if applicable)
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

const byZone = {};
for (let p of pages) {
    const zone = p.scan_zone || "Unorganized";
    byZone[zone] = (byZone[zone] || 0) + 1;
}

if (Object.keys(byZone).length > 1) {
    dv.table(
        ["Scan Zone", "Files"],
        Object.entries(byZone)
            .sort((a,b) => b[1] - a[1])
    );
}
```

---

## 🏷️ TAG ANALYSIS

### Tag Frequency
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

const tags = {};
for (let p of pages) {
    for (let t of (p.file.tags || [])) {
        tags[t] = (tags[t] || 0) + 1;
    }
}

if (Object.keys(tags).length > 0) {
    dv.table(
        ["Tag", "Occurrences", "% of Files"],
        Object.entries(tags)
            .sort((a,b) => b[1] - a[1])
            .slice(0, 20)
            .map(([tag, count]) => [
                tag,
                count,
                `${Math.round(100 * count / pages.length)}%`
            ])
    );
} else {
    dv.paragraph("*No tags found in current scope*");
}
```

### Tag Co-Occurrence (Top Pairs)
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

const pairs = {};
for (let p of pages) {
    const pageTags = p.file.tags || [];
    for (let i = 0; i < pageTags.length; i++) {
        for (let j = i + 1; j < pageTags.length; j++) {
            const pair = [pageTags[i], pageTags[j]].sort().join(" + ");
            pairs[pair] = (pairs[pair] || 0) + 1;
        }
    }
}

const topPairs = Object.entries(pairs)
    .sort((a,b) => b[1] - a[1])
    .slice(0, 10);

if (topPairs.length > 0) {
    dv.table(
        ["Tag Pair", "Co-occurrences"],
        topPairs
    );
}
```

---

## 🔗 CONNECTIVITY ANALYSIS

### Link Density Distribution
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

const linkCounts = {
    "Highly Connected (>10 links)": 0,
    "Well Connected (5-10 links)": 0,
    "Moderately Connected (2-4 links)": 0,
    "Weakly Connected (1 link)": 0,
    "Isolated (0 links)": 0
};

for (let p of pages) {
    const total = (p.file.outlinks?.length || 0) + (p.file.inlinks?.length || 0);
    if (total > 10) linkCounts["Highly Connected (>10 links)"]++;
    else if (total >= 5) linkCounts["Well Connected (5-10 links)"]++;
    else if (total >= 2) linkCounts["Moderately Connected (2-4 links)"]++;
    else if (total === 1) linkCounts["Weakly Connected (1 link)"]++;
    else linkCounts["Isolated (0 links)"]++;
}

dv.table(
    ["Connection Level", "Files", "% of Scope"],
    Object.entries(linkCounts).map(([level, count]) => [
        level,
        count,
        `${Math.round(100 * count / pages.length)}%`
    ])
);
```

### Most Connected Files
```dataview
TABLE WITHOUT ID
    file.link as "File",
    length(file.outlinks) as "→ Out",
    length(file.inlinks) as "← In",
    (length(file.outlinks) + length(file.inlinks)) as "Total"
FROM "[[SCOPE_FOLDER]]"
WHERE file.name != this.file.name
SORT (length(file.outlinks) + length(file.inlinks)) DESC
LIMIT 15
```

### Isolated Files (Action Required)
```dataview
TABLE WITHOUT ID
    file.link as "File",
    word_count as "Words",
    file.mtime as "Last Modified"
FROM "[[SCOPE_FOLDER]]"
WHERE file.name != this.file.name
  AND length(file.outlinks) = 0 
  AND length(file.inlinks) = 0
SORT word_count DESC
```

---

## ⚠️ QUALITY METRICS

### Completion Status
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

const statusBuckets = {
    "Complete (>500 words)": pages.filter(p => (p.word_count || 0) >= 500).length,
    "In Progress (200-500)": pages.filter(p => (p.word_count || 0) >= 200 && (p.word_count || 0) < 500).length,
    "Stub (<200 words)": pages.filter(p => (p.word_count || 0) < 200).length
};

dv.table(
    ["Status", "Count", "% of Files"],
    Object.entries(statusBuckets).map(([status, count]) => [
        status,
        count,
        `${Math.round(100 * count / pages.length)}%`
    ])
);
```

### Files Needing Attention
```dataview
TABLE WITHOUT ID
    file.link as "File",
    word_count as "Words",
    choice(word_count < 200, "🔴 Stub", choice(length(file.outlinks) = 0, "🟡 No Links", "🟢 OK")) as "Status",
    file.mtime as "Last Modified"
FROM "[[SCOPE_FOLDER]]"
WHERE file.name != this.file.name
  AND (word_count < 200 OR (length(file.outlinks) = 0 AND length(file.inlinks) = 0))
SORT word_count ASC
LIMIT 20
```

---

## 📅 TEMPORAL PATTERNS

### Recent Activity (Last 14 Days)
```dataview
TABLE WITHOUT ID
    file.link as "File",
    word_count as "Words",
    length(file.outlinks) as "Links",
    file.mtime as "Modified"
FROM "[[SCOPE_FOLDER]]"
WHERE file.name != this.file.name
  AND file.mtime >= date(now) - dur(14 days)
SORT file.mtime DESC
```

### Creation Timeline
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

const byMonth = {};
for (let p of pages) {
    if (p.file.ctime) {
        const month = p.file.ctime.toFormat("yyyy-MM");
        byMonth[month] = (byMonth[month] || 0) + 1;
    }
}

if (Object.keys(byMonth).length > 0) {
    dv.table(
        ["Month", "Files Created"],
        Object.entries(byMonth)
            .sort((a,b) => b[0].localeCompare(a[0]))
            .slice(0, 12)
    );
}
```

### Dormant Files (>60 Days)
```dataview
TABLE WITHOUT ID
    file.link as "File",
    word_count as "Words",
    file.mtime as "Last Modified",
    (date(now) - file.mtime).days + " days ago" as "Age"
FROM "[[SCOPE_FOLDER]]"
WHERE file.name != this.file.name
  AND file.mtime < date(now) - dur(60 days)
SORT file.mtime ASC
LIMIT 15
```

---

## 🧠 ADVANCED INSIGHTS

### Bridge Notes (Connecting Clusters)
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

// Files with high out-degree AND in-degree (bridge candidates)
const bridges = pages
    .map(p => ({
        file: p.file.link,
        outCount: p.file.outlinks?.length || 0,
        inCount: p.file.inlinks?.length || 0,
        balance: Math.abs((p.file.outlinks?.length || 0) - (p.file.inlinks?.length || 0))
    }))
    .filter(p => p.outCount >= 3 && p.inCount >= 3)
    .sort((a,b) => a.balance - b.balance)
    .slice(0, 10);

if (bridges.length > 0) {
    dv.table(
        ["File", "→ Out", "← In", "Balance"],
        bridges.map(b => [b.file, b.outCount, b.inCount, b.balance])
    );
} else {
    dv.paragraph("*No bridge notes detected - consider adding cross-references*");
}
```

### Emerging Concepts (New Tags This Week)
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

const recentPages = pages.filter(p => 
    p.file.ctime && p.file.ctime >= dv.date("now") - dv.duration("7 days")
);

const newTags = {};
for (let p of recentPages) {
    for (let t of (p.file.tags || [])) {
        newTags[t] = (newTags[t] || 0) + 1;
    }
}

if (Object.keys(newTags).length > 0) {
    dv.table(
        ["Tag", "Appearances (Last 7 Days)"],
        Object.entries(newTags)
            .sort((a,b) => b[1] - a[1])
            .slice(0, 10)
    );
} else {
    dv.paragraph("*No new files created in the last 7 days*");
}
```

### Conceptual Density Score
```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

if (pages.length > 0) {
    const totalWords = pages.reduce((sum, p) => sum + (p.word_count || 0), 0);
    const totalLinks = pages.reduce((sum, p) => sum + (p.file.outlinks?.length || 0), 0);
    const totalTags = pages.reduce((sum, p) => sum + (p.file.tags?.length || 0), 0);
    
    const avgWords = Math.round(totalWords / pages.length);
    const avgLinks = (totalLinks / pages.length).toFixed(1);
    const avgTags = (totalTags / pages.length).toFixed(1);
    
    const density = totalWords > 0 ? (totalLinks / (totalWords / 100)).toFixed(2) : 0;
    
    dv.paragraph(`
**Scope Metrics:**
- Average File Length: ${avgWords} words
- Average Links per File: ${avgLinks}
- Average Tags per File: ${avgTags}
- Conceptual Density: ${density} links per 100 words
    `);
}
```

---

## 🎯 RECOMMENDED ACTIONS

```dataviewjs
const folder = dv.current().file.folder || "";
const query = folder ? `"${folder}"` : '""';
const pages = dv.pages(query).where(p => p.file.name !== dv.current().file.name);

const actions = [];

// Check for isolated files
const isolated = pages.filter(p => 
    (p.file.outlinks?.length || 0) === 0 && (p.file.inlinks?.length || 0) === 0
).length;
if (isolated > 0) {
    actions.push(`🔴 **Link ${isolated} isolated files** - they're not connected to the knowledge graph`);
}

// Check for stubs
const stubs = pages.filter(p => (p.word_count || 0) < 200).length;
if (stubs > 0) {
    actions.push(`🟡 **Expand ${stubs} stub files** - they're under 200 words`);
}

// Check for dormant files
const dormant = pages.filter(p => 
    p.file.mtime && p.file.mtime < dv.date("now") - dv.duration("60 days")
).length;
if (dormant > 0) {
    actions.push(`🟢 **Review ${dormant} dormant files** - no edits in 60+ days`);
}

// Check for recent activity
const recent = pages.filter(p => 
    p.file.mtime && p.file.mtime >= dv.date("now") - dv.duration("7 days")
).length;
if (recent > 0) {
    actions.push(`✅ **${recent} files updated this week** - good momentum!`);
}

if (actions.length > 0) {
    dv.list(actions);
} else {
    dv.paragraph("✨ **All metrics healthy** - no immediate actions required");
}
```

---

## 🛠️ SCOPE CONFIGURATION

**To change scope manually:**
Edit the frontmatter at the top of this file:

```yaml
scope: auto              # Auto-detect from folder location
scope: global            # Force vault-wide analysis
scope: "03_PUBLICATIONS" # Force specific folder
```

**To create a zone-specific dashboard:**
1. Copy this file to target folder
2. Set `scope: auto` in frontmatter
3. Dashboard will automatically analyze that folder only

**To switch between LOCAL and GLOBAL views:**
- Place dashboard in **folder** → LOCAL scope
- Place dashboard in **root** → GLOBAL scope

---

## 📖 NAVIGATION

- [[GLOBAL_VAULT_STATS]] - Vault-wide overview
- [[BREAKTHROUGH_MAP]] - Conceptual breakthroughs
- [[🚀 START_HERE]] - User guide

---

*This adaptive dashboard automatically adjusts its scope based on location. For database-powered analytics, see GLOBAL_VAULT_STATS.md*
