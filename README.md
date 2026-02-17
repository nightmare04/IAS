# IAS (Inspection/Failures App)

This repository is a small PyQt6 desktop application that uses a local SQLite database (Peewee ORM). The main entrypoint is `main.py`.

Quick start (Windows PowerShell)

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the app

It's recommended to run the small launcher `run.py` which ensures the project root is on `sys.path` and avoids relative-import issues when running from the repository folder:

```powershell
python run.py
```

Notes
- The app uses `./data/database.db`. On startup `main.py` calls `init_table.drop_tables()` which will drop the tables and recreate them, erasing existing data. Remove or modify `init_app()` in `main.py` if you want to preserve your data.
- There is no build step — this is a Python desktop app. If you want distributable binaries consider using `pyinstaller` or `briefcase`.

Files of interest
- `main.py` — application entrypoint
- `data/init_table.py`, `data/models.py`, `data/example.py` — database schema and example data
- `forms/` and `custom_components/` — PyQt UI code

Optional next steps
- Add `pyproject.toml` or `setup.cfg` for packaging
- Add a `requirements-dev.txt` and unit tests
- Make DB initialization non-destructive and migration-friendly (e.g. use `peewee` migrations or `alembic` for SQLAlchemy)
