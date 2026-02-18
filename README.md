# IAS (Inspection/Failures App)

PyQt6 desktop application for aircraft inspection and failure tracking using SQLite database with Peewee ORM.

## Features

- ✈️ Aircraft management by type and division
- 🔧 Maintenance groups and systems tracking
- 📋 Aggregate/unit failure recording
- 🔍 Search and filter capabilities
- 📊 Grouped table views with context menus

## Quick Start

### 1. Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Run the application

```bash
python run.py
```

Or directly:
```bash
python -m app.main
```

## Development

### Install development dependencies

```bash
pip install -r requirements-dev.txt
```

### Run tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=app
```

### Code linting

```bash
# Run ruff linter
ruff check .

# Run ruff formatter
ruff format .

# Run type checker
mypy app/
```

### Database Migrations

**Create a new migration:**
```bash
python manage.py migrate create migration_name
```

**Run pending migrations:**
```bash
python manage.py migrate
```

**Rollback last migration:**
```bash
python manage.py migrate rollback
```

**Check migration status:**
```bash
python manage.py status
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `IAS_DATABASE_PATH` | Path to SQLite database | `./data/database.db` |

## Project Structure

```
IAS/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database and migrations setup
│   ├── models/              # Peewee ORM models
│   │   ├── __init__.py
│   │   ├── base.py          # Base model class
│   │   ├── aircraft.py      # Aircraft-related models
│   │   ├── failures.py      # Failure tracking models
│   │   └── osob.py          # Aircraft features models
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── dialogs/         # Dialog windows
│   │   ├── models/          # Qt table models
│   │   ├── widgets/         # Custom widgets
│   │   └── windows/         # Main windows
│   ├── repositories/        # Data access layer (TODO)
│   ├── services/            # Business logic (TODO)
│   └── utils/               # Utility functions
├── data/                    # Legacy compatibility module
├── migrations/              # Database migrations
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_db_models.py    # Model tests
│   └── test_models.py       # Table model tests
├── manage.py                # Management script
├── run.py                   # Application launcher
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml           # Project configuration
└── README.md
```

## Dependencies

### Production
- **PyQt6** >= 6.0.0 - GUI framework
- **peewee** >= 3.0.0 - ORM for SQLite
- **peewee-migrate** >= 1.0.0 - Database migrations

### Development
- **pytest** >= 7.0.0 - Testing framework
- **pytest-qt** >= 4.0.0 - PyQt6 testing support
- **pytest-cov** >= 4.0.0 - Coverage reporting
- **ruff** >= 0.1.0 - Fast Python linter
- **mypy** >= 1.0.0 - Static type checker

## Notes

⚠️ **Important:** On first run, the application will create the database and run migrations automatically.

## Optional: Create Executable

To create a distributable binary:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=IAS run.py
```

## License

MIT License
