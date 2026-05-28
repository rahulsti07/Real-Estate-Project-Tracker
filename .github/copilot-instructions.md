# ProjectTracker Workspace Instructions

## Project Overview
Real Estate Variance Analysis System built with Python, Streamlit, and SQLite.
- **Purpose:** Monitor projected vs actual parameters with 30% deviation flagging
- **Stack:** Python 3.8+, Streamlit, Pandas, Plotly, SQLite
- **Main App:** `app.py`

## Workspace Structure
```
Project Tracker/
├── app.py              # Main Streamlit dashboard
├── src/
│   ├── database.py     # Database management
│   ├── variance_engine.py  # Variance calculations
│   └── utils.py        # Utility functions
├── data/               # Data & database
├── requirements.txt    # Dependencies
└── README.md          # Full documentation
```

## Quick Commands

### Install & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Reset Database
```bash
# Delete data/projecttracker.db (recreates on next run)
```

## Key Features
- ✅ 30% deviation flagging for major variances
- ✅ Multi-project management with SQLite persistence
- ✅ CSV import/export functionality
- ✅ Interactive Streamlit dashboard
- ✅ Real-time variance calculations & visualizations

## Development Notes
- Deviation threshold: 30% (configurable in `src/variance_engine.py`)
- Database auto-initializes on first run
- Streamlit auto-reloads on file changes

## Next Steps
1. Run `pip install -r requirements.txt`
2. Execute `streamlit run app.py`
3. Create a project and import sample data
4. Review variance analysis dashboard
