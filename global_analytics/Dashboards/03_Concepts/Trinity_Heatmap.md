---
uuid: c10e7181-0229-59eb-b99e-fcfd85b986e0
title: 🔺 Trinity Coherence Heatmap (DataviewJS)
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\Trinity_Heatmap.md
uuid_generated_at: '2025-11-22T01:23:04.402517'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🔺 Trinity Coherence Heatmap (DataviewJS)
```dataviewjs
const rows = dv.pages().where(p => p.trinity_aspects && p.title).map(p => {
  const F = p.trinity_aspects.Father ?? 0;
  const S = p.trinity_aspects.Son ?? 0;
  const H = p.trinity_aspects.Spirit ?? 0;
  return {title: p.file.link, Father: Number(F), Son: Number(S), Spirit: Number(H)};
}).array();

dv.table(["Note","Father","Son","Spirit"],
  rows.map(r => [r.title, r.Father.toFixed(2), r.Son.toFixed(2), r.Spirit.toFixed(2)]));
```
