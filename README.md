# Python-Backend-Dashboards

Theophysics Analytics Backend - Python tools, dashboards, and Obsidian plugin development.

## Repository Structure

```
├── python_backend/              # Main Python Backend Application
│   ├── core/                    # Core modules (API manager, query engine, etc.)
│   ├── ui/                      # PySide6 GUI components
│   ├── engine/                  # Processing engines
│   ├── scripts/                 # Utility scripts
│   ├── data/                    # Data storage (SQLite, cache)
│   ├── config/                  # Configuration files
│   ├── templates/               # Query templates
│   ├── knowledge_base/          # Knowledge base files
│   ├── main.py                  # Main application entry
│   ├── api_query_launcher.py    # API Query GUI launcher
│   └── requirements.txt         # Python dependencies
│
├── global_analytics/            # Analytics data and dashboards
│   ├── Dashboards/              # Obsidian dashboard templates
│   ├── Data_Analytics/          # Analytics data files
│   ├── Master_Sheet/            # Master data (axioms, concepts, definitions)
│   ├── Reports/                 # Generated reports
│   └── theophysics_analytics/   # Python analytics engine
│
└── obsidian-plugin/             # Theophysics Analytics Dashboard (forked from Dashboard Navigator)
    ├── src/                     # TypeScript source
    ├── manifest.json            # Obsidian plugin manifest
    ├── styles.css               # Plugin styles
    └── THEOPHYSICS_CUSTOMIZATION_PLAN.md  # Customization roadmap
```

## Obsidian Plugin (Theophysics Analytics Dashboard)

Forked from [Dashboard Navigator](https://github.com/drbap/dashboard-navigator-for-obsidian) by Bernardo Pires (MIT License).

**Planned Features:**
- Paper progress tracking (P1-P12)
- Axiom/Proof/Law categorization with pie charts
- Framework breakdown (Logos Field, Witness Field, Grace Function, etc.)
- Custom search filters: `@axiom`, `@proof`, `@P1`, `@equation:`
- UUID cross-reference lookup
- Equation gallery with LaTeX rendering

See [THEOPHYSICS_CUSTOMIZATION_PLAN.md](obsidian-plugin/THEOPHYSICS_CUSTOMIZATION_PLAN.md) for details.

## Python Backend Features

- **API Query Builder** - GUI for building and executing API queries
- **Academic APIs** - Semantic Scholar, PubMed, arXiv, CrossRef, OpenAlex
- **HeartMath/HRV Research** - Specialized API presets for coherence research
- **Job Scheduling** - Save, load, and schedule API query jobs
- **SQLite Tracking** - Track all API calls and results
- **Auto-Linker** - Automatic note linking for Obsidian

## Quick Start

```bash
cd python_backend
pip install -r requirements.txt
python api_query_launcher.py   # Launch API Query GUI
python main.py                 # Launch main application
```

## Related Repositories

- [Python-OBS-backend](https://github.com/YellowKidokc/Python-OBS-backend) - Original backend deployment
