# Theophysics Dashboard Customization Plan

This document outlines how to customize the Dashboard Navigator plugin for Theophysics analytics.

## Current Plugin Structure

```
obsidian-plugin/src/
├── main.ts                    # Plugin entry point
├── dn.ts                      # Main dashboard modal (1900+ lines)
├── settings.ts                # Settings tab
├── data/
│   └── dndatamanager.ts       # Data caching and file categorization
├── utils/
│   ├── dnpiechart.ts          # Pie chart rendering
│   ├── dntablemanager.ts      # Table management
│   ├── dntagsuggestions.ts    # Tag autocomplete
│   ├── dnlinks.ts             # Backlinks/outlinks
│   ├── tags.ts                # Tag extraction
│   └── format.ts              # Formatting utilities
└── modals/                    # Various modal dialogs
```

## Data Available in global_analytics/

| File | Contains |
|------|----------|
| `MASTER_AXIOMS.json` | 19 axioms with UUIDs, equations, frameworks, papers |
| `MASTER_TAGS.json` | 35 unique tags with file mappings |
| `MASTER_CONCEPTS.json` | Concept definitions |
| `MASTER_DEFINITIONS.json` | Term definitions |
| `MASTER_SEMANTIC.json` | Semantic markup data |
| `MASTER_AGGREGATED_ANALYTICS.json` | Overview of all data categories |

## Customization Plan

### Phase 1: Core Data Integration

1. **New Data Manager** (`src/data/theophysicsDataManager.ts`)
   - Parse JSON files from global_analytics/Master_Sheet/
   - Categories: Axioms, Laws, Proofs, Evidence, Equations
   - Track by paper (P1-P12), framework, type

2. **New Data Interface** (`src/data/theophysicsTypes.ts`)
   ```typescript
   interface TheophysicsAxiom {
     uuid: string;
     text: string;
     axiom_type: 'law' | 'proof' | 'hypothesis' | 'principle';
     source_paper: number;
     paper_title: string;
     framework: string;
     equations: string[];
     related_concepts: string[];
     confidence: number;
   }

   interface TheophysicsData {
     axioms: TheophysicsAxiom[];
     by_paper: Map<number, TheophysicsAxiom[]>;
     by_framework: Map<string, TheophysicsAxiom[]>;
     by_type: Map<string, TheophysicsAxiom[]>;
   }
   ```

### Phase 2: Custom Dashboard Views

3. **Theophysics Dashboard View** (`src/views/theophysicsView.ts`)
   - Paper progress grid (P1-P12)
   - Framework breakdown pie chart
   - Axiom type distribution
   - Recent research activity

4. **Custom Pie Chart Data**
   - By Paper: P1 (11), P2 (11), P3-P12 (pending)
   - By Type: Laws (11), Proofs (8), Hypotheses (3), Principles (2)
   - By Framework: Logos Field (8), Witness Field (5), etc.

### Phase 3: Enhanced Search

5. **Custom Search Filters**
   - `@axiom` - Search axioms only
   - `@proof` - Search proofs only
   - `@P1` through `@P12` - Filter by paper
   - `@logos` - Logos Field items
   - `@witness` - Witness Field items
   - `@equation:` - Search by equation content

6. **UUID Cross-Reference Search**
   - Search by UUID: `uuid:TP-AX-LAW-a1b2c3d4`
   - Show related items across papers

### Phase 4: Theophysics-Specific Features

7. **Equation Gallery**
   - Display LaTeX equations
   - Group by framework
   - Show spiritual↔physical mappings

8. **Paper Progress Tracker**
   - Status: Complete, In Progress, Planned
   - Axiom count per paper
   - Evidence strength metrics

9. **Evidence Dashboard**
   - Scientific citations
   - Scripture references
   - Cross-validation status

## Files to Modify

| Original File | Changes |
|---------------|---------|
| `main.ts` | Add Theophysics data manager, new commands |
| `dn.ts` | Add Theophysics view button, custom dashboard |
| `dnpiechart.ts` | Support Theophysics categories |
| `dndatamanager.ts` | Integrate with Theophysics data |
| `settings.ts` | Add Theophysics settings (data path, etc.) |

## New Files to Create

1. `src/data/theophysicsDataManager.ts`
2. `src/data/theophysicsTypes.ts`
3. `src/views/theophysicsView.ts`
4. `src/utils/theophysicsSearch.ts`
5. `src/utils/equationRenderer.ts`

## Settings to Add

```typescript
interface TheophysicsSettings {
  analytics_path: string;           // Path to global_analytics
  show_equations: boolean;          // Render LaTeX equations
  default_paper_filter: number;     // Default to show (0 = all)
  show_framework_colors: boolean;   // Color by framework
}
```

## Build & Install

```bash
cd obsidian-plugin
npm install
npm run build
# Copy main.js, manifest.json, styles.css to:
# .obsidian/plugins/theophysics-dashboard/
```

## Integration with Python Backend

The Python backend in `python_backend/` can:
1. Regenerate analytics JSON files
2. Update MASTER_AXIOMS.json when papers change
3. Validate semantic markup consistency
4. Push updates to the Obsidian plugin

## Next Steps

1. [ ] Set up npm dependencies
2. [ ] Create theophysicsDataManager.ts
3. [ ] Add Theophysics view to dn.ts
4. [ ] Modify pie chart for Theophysics categories
5. [ ] Implement custom search filters
6. [ ] Test with sample vault
7. [ ] Document installation process
