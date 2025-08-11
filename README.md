# Meridian Studio

Meridian Studio is a modern visual graph builder for Meridian Runtime. It provides a web UI to create, validate, execute, and analyze computational graphs with real-time message tracing and performance analytics.

## Tech Stack

- Frontend: Vite + React 18 + TypeScript, Tailwind CSS, shadcn/ui (scaffold-ready)
- Runtime for frontend tooling: Deno 2 (npm interop) — no Node required
- Backend: FastAPI (Python), Pydantic, SQLAlchemy, Alembic
- DB/Auth: Supabase (PostgreSQL), Redis (optional)
- Realtime: WebSockets for execution updates and metrics
- Containers: Docker + docker-compose

## Repository Layout

```
meridian-studio/
├── frontend/              # Vite + React app (runs via Deno 2 tasks)
├── backend/               # FastAPI app
├── supabase/
│   └── migrations/        # SQL migrations (Supabase/Postgres)
├── docker-compose.yml     # Local dev stack (frontend, backend, db, supabase, redis)
├── .env.example           # Environment variables template
├── LICENSE
└── README.md
```

## Prerequisites

- Deno 2.x (`deno --version`)
- Python 3.11+
- uv (Python package manager by Astral)
- Docker + Docker Compose
- GitHub CLI (optional for repo ops)

If Deno is not installed: `brew install deno` (macOS) or see `https://deno.com`.

If uv is not installed:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Quickstart (Docker Compose)

1. Copy env file and fill secrets:

```
cp .env.example .env
```

Ensure `JWT_SECRET` is the same for both Supabase and the backend (docker-compose passes it to both). Fill Supabase keys from your project or local stack.

2. Start the stack:

```
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000 (docs at `/docs`)
- Supabase Studio: http://localhost:54321
- Postgres: localhost:54322

## Local Development

### Frontend (Deno 2 + Vite)

```
cd frontend
cp .env.example .env.local
# set VITE_API_URL, VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY
 deno task dev
```

Build/preview:

```
deno task build
deno task preview
```

Environment variables (e.g. `VITE_API_URL`) are provided via `.env` and docker-compose, and are accessible in code as `import.meta.env.VITE_API_URL`.

### Backend (uv + FastAPI)

Create virtual environment and install deps:

```
cd backend
uv venv
. .venv/bin/activate
uv pip install -e .
```

Run API locally:

```
uvicorn app.main:app --reload --port 8000
```

### Database (Supabase/Postgres)

The `supabase/migrations/0001_init.sql` migration sets up core tables and indexes for users, graphs, executions, message tracing, and edge metrics. When using Docker Compose, the DB is provisioned automatically on first run.

## Notes on Deno 2 Usage

- Vite and all npm dependencies are executed via Deno’s npm interop (`npm:` spec). No Node is required.
- Tasks are defined in `frontend/deno.jsonc`.
- You can still develop with Node if desired; the project structure is compatible, but Deno 2 is the default.

## Licensing

This project is licensed under the MIT License — see `LICENSE`.

## Status

This is an initial scaffold aligned with the design, requirements, and tasks specs under `.kiro/specs/web-visual-graph-builder/`. Stubs for APIs and migrations are included to unblock incremental development.

### Auth Notes
- Email/password auth is supported via Supabase. Enable it in Supabase Auth settings (Providers > Email).
- Social providers (Google/GitHub) are optional and can be added later by configuring provider keys and auth callback URLs in Supabase, then adding UI buttons that call `supabase.auth.signInWithOAuth`.
- Frontend attaches the Supabase access token as `Authorization: Bearer <token>` for authenticated API calls.
