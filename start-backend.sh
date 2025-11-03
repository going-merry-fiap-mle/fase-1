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
  echo "[INFO] Heroku detected (DYNO=$DYNO), verifying Datadog APM configuration"

  if [ -n "${DD_TRACE_AGENT_URL:-}" ]; then
    echo "[WARN] DD_TRACE_AGENT_URL is still set: $DD_TRACE_AGENT_URL"
    echo "[WARN] Force unsetting to use local agent"
    unset DD_TRACE_AGENT_URL
  fi

  echo "[INFO] Final Datadog APM configuration:"
  echo "  DD_AGENT_HOST: ${DD_AGENT_HOST:-NOT SET}"
  echo "  DD_TRACE_AGENT_PORT: ${DD_TRACE_AGENT_PORT:-NOT SET}"
  echo "  DD_DOGSTATSD_PORT: ${DD_DOGSTATSD_PORT:-NOT SET}"
  echo "  DD_TRACE_AGENT_URL: ${DD_TRACE_AGENT_URL:-(correctly unset)}"

  if [ "${DD_AGENT_HOST}" != "127.0.0.1" ]; then
    echo "[ERROR] DD_AGENT_HOST is not 127.0.0.1! Forcing..."
    export DD_AGENT_HOST="127.0.0.1"
  fi

  if [ "${DD_TRACE_AGENT_PORT}" != "8126" ]; then
    echo "[ERROR] DD_TRACE_AGENT_PORT is not 8126! Forcing..."
    export DD_TRACE_AGENT_PORT="8126"
  fi

  if [ -z "${DD_LOGS_INJECTION:-}" ]; then
    export DD_LOGS_INJECTION="true"
    echo "[INFO] Enabling DD_LOGS_INJECTION for log/trace correlation"
  fi

  echo "[INFO] Waiting for Datadog agents to be ready..."
  sleep 5

  if command -v nc >/dev/null 2>&1; then
    if nc -z 127.0.0.1 8126; then
      echo "[INFO] Datadog Trace Agent is listening on port 8126"
    else
      echo "[ERROR] Datadog Trace Agent NOT listening on port 8126!"
      echo "[ERROR] ddtrace will fail or use agentless fallback"
      echo "[ERROR] Check entrypoint.sh logs for agent startup errors"
    fi
  fi
else
  echo "[INFO] Local/container environment detected"
  export DD_AGENT_HOST="${DD_AGENT_HOST:-localhost}"
  export DD_TRACE_AGENT_PORT="${DD_TRACE_AGENT_PORT:-8126}"
  echo "[INFO] Using DD_AGENT_HOST=$DD_AGENT_HOST:$DD_TRACE_AGENT_PORT"
fi

echo "[INFO] Starting Flask application with Datadog APM..."
exec poetry run ddtrace-run python -m app.main