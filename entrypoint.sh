#!/bin/bash

set -e

echo "[INFO] Starting application container..."

if [ -n "${DYNO:-}" ]; then
  echo "[INFO] Heroku environment detected (DYNO=$DYNO)"
  
  export DD_SERVICE="${DD_SERVICE:-fase-1-backend}"
  export DD_ENV="${DD_ENV:-production}"
  export DD_LOGS_INJECTION="${DD_LOGS_INJECTION:-true}"
  
  echo "[INFO] Datadog configuration (logs only):"
  echo "  DD_SERVICE: $DD_SERVICE"
  echo "  DD_ENV: $DD_ENV"
  echo "  DD_LOGS_INJECTION: $DD_LOGS_INJECTION"
  echo "[INFO] APM agents disabled - using log drain for monitoring"
else
  echo "[INFO] Local environment detected"
fi

echo "[INFO] Starting Xvfb for headless operations..."
Xvfb :99 -screen 0 1920x1080x24 > /tmp/xvfb.log 2>&1 &
XVFB_PID=$!

sleep 2

if kill -0 $XVFB_PID 2>/dev/null; then
  echo "[INFO] ✅ Xvfb started successfully (PID: $XVFB_PID)"
else
  echo "[WARN] ⚠️  Xvfb may have failed to start"
fi

echo "[INFO] Starting Flask application..."
exec /app/start-backend.sh
