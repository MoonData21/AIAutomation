# AI Stock Analysis API

## Project Structure
FastAPI backend + Streamlit frontend

## Stack
- FastAPI + uvicorn
- SQLAlchemy async + SQLite
- Anthropic Claude API
- Yahoo Finance
- Pydantic Settings

## Key Files
- `app/main.py` - FastAPI entry point
- `app/core/config.py` - pydantic settings
- `app/db/session.py` - database engine + init_db
- `app/db/base.py` - SQLAlchemy Base
- `app/db/models/workflow_run.py` - WorkflowRun model
- `app/repositories/workflow_repository.py` - CRUD operations
- `app/api/routes/analyze.py` - analyze endpoint
- `railway.toml` - Railway deployment config

## Known Issues
- `app.repositories.workflow_repository` module not found on Railway despite existing locally
- `__init__.py` present in repositories folder