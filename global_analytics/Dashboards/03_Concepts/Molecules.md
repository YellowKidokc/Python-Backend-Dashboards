---
uuid: b994a285-6b8a-5e52-9b9d-ddde3459e07f
title: 🧬 Molecule Index
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\Molecules.md
uuid_generated_at: '2025-11-22T01:23:04.231570'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🧬 Molecule Index
```dataview
TABLE file.link AS Molecule, phase, internal_consistency, predictive_power, coherence_score
FROM "04_Integration"
WHERE type = "molecule" OR contains(file.name, "MOL_")
SORT coherence_score DESC
```
