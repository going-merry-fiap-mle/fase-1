#!/bin/bash

set -e

echo "[INFO] Starting Datadog integration for Heroku Docker deployment..."

if [ -n "${DD_TRACE_AGENT_URL:-}" ]; then
  echo "[INFO] Unsetting DD_TRACE_AGENT_URL to force local agent usage"
  unset DD_TRACE_AGENT_URL
fi

export DD_AGENT_HOST="127.0.0.1"
export DD_TRACE_AGENT_PORT="8126"
export DD_DOGSTATSD_PORT="8125"

echo "[INFO] Forcing local Datadog Agent configuration:"
echo "  DD_AGENT_HOST: $DD_AGENT_HOST"
echo "  DD_TRACE_AGENT_PORT: $DD_TRACE_AGENT_PORT"
echo "  DD_TRACE_AGENT_URL: (unset)"

if [ -n "${DYNO:-}" ]; then
  echo "[INFO] Heroku environment detected (DYNO=$DYNO)"
  
  if [ -z "${DD_API_KEY:-}" ]; then
    echo "[WARN] DD_API_KEY not set. Datadog Agent will not start."
    echo "[WARN] Set it with: heroku config:set DD_API_KEY=<your-key> -a <app-name>"
  else
    echo "[INFO] DD_API_KEY is set"
    
    export DD_HEROKU_DYNO=true
    echo "[INFO] DD_HEROKU_DYNO set to true"
    
    export DD_SITE="${DD_SITE:-us5.datadoghq.com}"
    export DD_SERVICE="${DD_SERVICE:-fase-1-backend}"
    export DD_ENV="${DD_ENV:-production}"
    export DD_LOGS_INJECTION="${DD_LOGS_INJECTION:-true}"
    export DD_TRACE_SAMPLE_RATE="${DD_TRACE_SAMPLE_RATE:-1.0}"
    
    echo "[INFO] Datadog configuration:"
    echo "  DD_SITE: $DD_SITE"
    echo "  DD_SERVICE: $DD_SERVICE"
    echo "  DD_ENV: $DD_ENV"
    echo "  DD_AGENT_HOST: $DD_AGENT_HOST (forced local)"
    echo "  DD_TRACE_AGENT_PORT: $DD_TRACE_AGENT_PORT (forced local)"
    echo "  DD_TRACE_AGENT_URL: (UNSET - no agentless fallback allowed)"
    
    echo "[INFO] Processing Datadog configuration template..."
    if [ -f /etc/datadog-agent/datadog.yaml ]; then
      cat /etc/datadog-agent/datadog.yaml | \
        sed "s/\${DD_API_KEY}/$DD_API_KEY/g" | \
        sed "s/\${DD_SITE}/$DD_SITE/g" | \
        sed "s/\${DD_SERVICE}/$DD_SERVICE/g" | \
        sed "s/\${DD_ENV}/$DD_ENV/g" | \
        sed "s/\${DYNO}/$DYNO/g" | \
        sed "s/\${DD_HEROKU_DYNO}/$DD_HEROKU_DYNO/g" > /tmp/datadog.yaml.processed
      
      mv /tmp/datadog.yaml.processed /etc/datadog-agent/datadog.yaml
      echo "[INFO] Datadog configuration processed successfully"
    fi
    
    echo "[INFO] Skipping main Datadog Agent (not needed for APM-only setup)"
    echo "[INFO] Main agent causes issues with Heroku's ephemeral hostnames"
    
    echo "[INFO] Starting Datadog APM Trace Agent (standalone mode)..."
    /opt/datadog-agent/embedded/bin/trace-agent --config=/etc/datadog-agent/datadog.yaml > /tmp/trace-agent.log 2>&1 &
    TRACE_AGENT_PID=$!
    echo "[INFO] Trace Agent PID: $TRACE_AGENT_PID"
    
    echo "[INFO] Skipping Datadog Process Agent (optional, not critical for APM)"
    
    echo "[INFO] Waiting for Trace Agent to initialize..."
    sleep 5
    
    if kill -0 $TRACE_AGENT_PID 2>/dev/null; then
      echo "[INFO] ✅ Datadog APM Trace Agent is running (PID: $TRACE_AGENT_PID)"
      
      echo "[INFO] Checking if Trace Agent is listening on port 8126..."
      sleep 2
      if nc -z 127.0.0.1 8126 2>/dev/null; then
        echo "[INFO] ✅ Trace Agent is listening on port 8126"
        echo "[INFO] 🎉 Datadog APM setup complete and ready!"
      else
        echo "[ERROR] ❌ Trace Agent is NOT listening on port 8126!"
        echo "[ERROR] This will cause ddtrace to fail"
        echo "[ERROR] Trace Agent logs:"
        cat /tmp/trace-agent.log | tail -20
      fi
    else
      echo "[ERROR] ❌ Datadog APM Trace Agent failed to start!"
      echo "[ERROR] Trace Agent logs:"
      cat /tmp/trace-agent.log | tail -20
    fi
  fi
else
  echo "[INFO] Local/non-Heroku environment detected"
  echo "[INFO] Datadog Agent will not be started automatically"
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
