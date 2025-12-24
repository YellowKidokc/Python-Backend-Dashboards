# Theophysics Backend Dashboards

Analytics engine and dashboard system for the Theophysics research project.

## Structure

```
├── global_analytics/           # Analytics data and dashboards
│   ├── Dashboards/            # Obsidian dashboard templates
│   ├── Data_Analytics/        # Analytics data files
│   ├── Master_Sheet/          # Master data (axioms, concepts, definitions)
│   ├── Reports/               # Generated reports
│   └── theophysics_analytics/ # Python analytics engine
│
├── obsidian-plugin/           # Forked Dashboard Navigator (coming soon)
│   └── src/                   # TypeScript plugin source
│
└── README.md
```

## Components

### Global Analytics (`global_analytics/`)

Contains all analytics data, dashboards, and the Python analytics engine:

- **Dashboards/** - Obsidian markdown dashboards for paper management
- **Master_Sheet/** - Core data files:
  - `MASTER_AXIOMS.json` - All axioms (A1, A2, etc.)
  - `MASTER_CONCEPTS.json` - Concept definitions
  - `MASTER_DEFINITIONS.json` - Term definitions
  - `MASTER_SEMANTIC.json` - Semantic markup data
  - `MASTER_TAGS.json` - Tag taxonomy
- **theophysics_analytics/** - Python scripts for analysis

### Python Analytics Engine

```bash
cd global_analytics/theophysics_analytics
pip install -r requirements.txt
python run_analytics.py
```

### Obsidian Dashboard Plugin (Coming Soon)

Forked from [Dashboard Navigator](https://github.com/drbap/dashboard-navigator-for-obsidian) - will be customized for Theophysics-specific analytics.

## Related Repositories

- [Python-OBS-backend](https://github.com/YellowKidokc/Python-OBS-backend) - Main PySide6 GUI application
- [Dashboard Navigator Fork](https://github.com/YellowKidokc/dashboard-navigator-for-obsidian) - Obsidian plugin (to be integrated)

## License

MIT License
