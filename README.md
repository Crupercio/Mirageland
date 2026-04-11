# Mirageland

Mirageland is a local-first Django and Three.js project for a story-driven virtual figurine collector game. We are building it in small working phases, keeping the project safe for GitHub from the start, and only deploying once the product loop is proven.

## Working Approach

- Develop locally first
- Use PostgreSQL from day one
- Keep secrets in `.env`, never in committed files
- Complete one meaningful phase at a time
- Push to GitHub only after a phase is working and verified

## Source Of Truth

- [mirageland_analysis.md](./mirageland_analysis.md)
- [mirageland_execution_plan.md](./mirageland_execution_plan.md)
- [mirageland_project_brief.md](./mirageland_project_brief.md)
- [mirageland_vertical_slice.md](./mirageland_vertical_slice.md)
- [mirageland_tracker.md](./mirageland_tracker.md)

## Git And Security Rules

- Commit `.env.example`, never commit `.env`
- Do not hardcode API keys, passwords, or tokens
- Keep media, generated assets, and local build artifacts out of Git unless intentionally versioned
- Use small commits tied to one completed task or milestone
- Push after local verification, not in the middle of broken work

## Recommended Git Workflow

- `main` for stable working milestones
- `feature/<name>` branches for active work
- Merge back into `main` after local testing

## Phase Checkpoints

Each major phase should end with:

1. feature working locally
2. basic verification completed
3. tracker updated
4. commit created
5. push to GitHub

## Local Setup

1. Copy `.env.example` to `.env`
2. Set your real `SECRET_KEY`
3. Set your local PostgreSQL credentials in `.env`
4. Run `python manage.py makemigrations`
5. Run `python manage.py migrate`
6. Start the app with `python manage.py runserver 8500`

If PostgreSQL is not ready yet, the project includes a temporary fallback for local verification only:

- set `USE_SQLITE=True` in `.env`

That fallback is only for bootstrapping. Our intended local database is still PostgreSQL.

## Railway Deployment

Recommended first live setup:

1. Create a Railway project and connect this GitHub repo
2. Add a PostgreSQL service in Railway
3. Set these variables on the web service:
   `DJANGO_SETTINGS_MODULE=mirageland.settings.production`
   `SECRET_KEY=<strong-secret>`
   `ALLOWED_HOSTS=<your-domain>,<your-railway-domain>`
   `CSRF_TRUSTED_ORIGINS=https://<your-domain>,https://<your-railway-domain>`
   `SECURE_SSL_REDIRECT=True`
4. Railway Postgres will also provide connection variables such as `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, and `PGPASSWORD`
5. Deploy and confirm `/health/` returns `200`

The repository now includes `railway.json` config-as-code so the service has:

- a build command
- a pre-deploy migration command
- a Gunicorn start command
- a `/health/` healthcheck path

## Next Step

Start with Phase 1 in [mirageland_tracker.md](./mirageland_tracker.md): lock the vertical slice before we scaffold code.
