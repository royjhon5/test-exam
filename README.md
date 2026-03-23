# Multi-tenant Alerts Prototype

A working prototype using **Django + Python Ninja** for the backend and **Vite + React** for the frontend.

## Features
- Tenant-scoped alerts API with strict isolation.
- Mock LLM enrichment step.
- React dashboard with tenant switcher, pagination, and virtualized rendering.
- Architecture document and system diagram.

## Backend
### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py runserver
```

### Windows PowerShell
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
py backend/manage.py migrate
py backend/manage.py runserver
```

If `python` is not recognized on Windows, use the `py` launcher as shown above or install Python from python.org and enable the PATH option during setup.

Run `migrate` once before first startup so Django can create the built-in auth/session tables.

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
