# Multi-tenant Alerts Prototype

A working prototype using **Django + Python Ninja** for the backend and **Vite + React** for the frontend.

## Features
- Tenant-scoped alerts API with strict isolation.
- Mock LLM enrichment step.
- React dashboard with tenant switcher, pagination, and virtualized rendering.
- Architecture document and system diagram.

## Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/alerts`.
Use request headers:
- `X-Tenant-Id`: `tenant-acme` or `tenant-globex`
- `X-User-Role`: `admin` or `analyst`

## Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `http://127.0.0.1:8000` by default.
Set `VITE_API_BASE_URL` to override it.

## Tests
```bash
python -m unittest discover -s backend/tests -t backend
```
