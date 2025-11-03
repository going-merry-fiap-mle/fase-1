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

if [ -n "${DYNO:-}" ]; then
  echo "[INFO] Heroku detected (DYNO=$DYNO), configuring agentless mode for Datadog APM"

  if [ -z "${DD_TRACE_AGENT_URL:-}" ]; then
    if [ -n "${DD_SITE:-}" ]; then
      export DD_TRACE_AGENT_URL="https://trace.agent.${DD_SITE}"
      echo "[INFO] DD_TRACE_AGENT_URL not set; defaulting to ${DD_TRACE_AGENT_URL} (from DD_SITE)"
    else
      export DD_TRACE_AGENT_URL="https://trace.agent.datadoghq.com"
      echo "[INFO] DD_SITE not set; defaulting DD_TRACE_AGENT_URL to ${DD_TRACE_AGENT_URL}"
    fi
  fi

  if [ -z "${DD_LOGS_INJECTION:-}" ]; then
    export DD_LOGS_INJECTION="true"
    echo "[INFO] Enabling DD_LOGS_INJECTION for log/trace correlation"
  fi
else
  echo "[INFO] Local/container environment detected, using DD_AGENT_HOST=${DD_AGENT_HOST:-localhost}"
fi

exec poetry run ddtrace-run python -m app.main