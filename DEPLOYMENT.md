# Deployment Notes

## Target

- Platform: Railway
- App host: Railway web service
- Database: Railway Postgres
- Environment: staging first, production after validation

## Railway Config

This project includes [railway.json](./railway.json) using Railway config-as-code.

It defines:

- `buildCommand`: `pip install -r requirements.txt`
- `preDeployCommand`: `python manage.py migrate`
- `startCommand`: `gunicorn mirageland.wsgi --bind 0.0.0.0:$PORT`
- `healthcheckPath`: `/health/`

## Required Environment Variables

- `DJANGO_SETTINGS_MODULE=mirageland.settings.production`
- `SECRET_KEY=<strong-secret>`
- `ALLOWED_HOSTS=<your-domain>,<your-railway-domain>`
- `CSRF_TRUSTED_ORIGINS=https://<your-domain>,https://<your-railway-domain>`
- `SECURE_SSL_REDIRECT=True`

## Database Variables

The settings now support both local-style DB vars and Railway-style Postgres vars:

- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT`

## Staging Checklist

1. Create a Railway environment for staging
2. Attach Postgres
3. Set production env vars
4. Deploy from `main`
5. Verify `/health/`
6. Verify `/catalogue/`, `/quests/`, and `/room/`
7. Confirm static assets load correctly

## Notes

- Railway healthchecks use the hostname `healthcheck.railway.app`, so production settings allow that host.
- The production settings also allow `.up.railway.app` for Railway-generated domains.
- WhiteNoise is enabled only in production settings.

