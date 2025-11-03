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
  echo "[INFO] Heroku detected (DYNO=$DYNO), configuring Datadog APM with local agent"
  
  export DD_AGENT_HOST="${DD_AGENT_HOST:-127.0.0.1}"
  export DD_TRACE_AGENT_PORT="${DD_TRACE_AGENT_PORT:-8126}"
  export DD_DOGSTATSD_PORT="${DD_DOGSTATSD_PORT:-8125}"
  
  echo "[INFO] Datadog APM configuration:"
  echo "  DD_AGENT_HOST: $DD_AGENT_HOST"
  echo "  DD_TRACE_AGENT_PORT: $DD_TRACE_AGENT_PORT"
  echo "  DD_DOGSTATSD_PORT: $DD_DOGSTATSD_PORT"

  if [ -z "${DD_LOGS_INJECTION:-}" ]; then
    export DD_LOGS_INJECTION="true"
    echo "[INFO] Enabling DD_LOGS_INJECTION for log/trace correlation"
  fi
else
  echo "[INFO] Local/container environment detected"
  export DD_AGENT_HOST="${DD_AGENT_HOST:-localhost}"
  export DD_TRACE_AGENT_PORT="${DD_TRACE_AGENT_PORT:-8126}"
  echo "[INFO] Using DD_AGENT_HOST=$DD_AGENT_HOST:$DD_TRACE_AGENT_PORT"
fi

exec poetry run ddtrace-run python -m app.main