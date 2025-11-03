echo "[INFO] Iniciando Flask API..."

poetry install --no-root --no-interaction 2>&1 | grep -v "lock file" || true

mkdir -p /app/data

if [ -z "${DATABASE_URL:-}" ]; then
  export DATABASE_URL="sqlite:////app/data/app.db"
  echo "[INFO] DATABASE_URL not set, falling back to ${DATABASE_URL}"
else
  echo "[INFO] Using DATABASE_URL from environment"
fi

if command -v alembic >/dev/null 2>&1; then
  echo "[INFO] Running alembic migrations..."
  alembic upgrade head || echo "[WARN] Alembic migrations failed or skipped; continuing startup"
else
  echo "[WARN] alembic not installed in environment; skipping migrations"
fi

exec poetry run ddtrace-run python -m app.main