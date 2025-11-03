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
    
    echo "[INFO] Starting Datadog Agent..."
    datadog-agent run > /tmp/datadog-agent.log 2>&1 &
    DD_AGENT_PID=$!
    echo "[INFO] Datadog Agent PID: $DD_AGENT_PID"
    
    echo "[INFO] Starting Datadog APM Trace Agent..."
    /opt/datadog-agent/embedded/bin/trace-agent --config=/etc/datadog-agent/datadog.yaml > /tmp/trace-agent.log 2>&1 &
    TRACE_AGENT_PID=$!
    echo "[INFO] Trace Agent PID: $TRACE_AGENT_PID"
    
    echo "[INFO] Starting Datadog Process Agent..."
    /opt/datadog-agent/embedded/bin/process-agent --config=/etc/datadog-agent/datadog.yaml > /tmp/process-agent.log 2>&1 &
    PROCESS_AGENT_PID=$!
    echo "[INFO] Process Agent PID: $PROCESS_AGENT_PID"
    
    echo "[INFO] Waiting for agents to initialize..."
    sleep 5
    
    if kill -0 $DD_AGENT_PID 2>/dev/null; then
      echo "[INFO] ✅ Datadog Agent is running (PID: $DD_AGENT_PID)"
    else
      echo "[ERROR] ❌ Datadog Agent failed to start!"
      echo "[ERROR] Agent logs:"
      cat /tmp/datadog-agent.log | tail -20
    fi
    
    if kill -0 $TRACE_AGENT_PID 2>/dev/null; then
      echo "[INFO] ✅ Datadog APM Trace Agent is running (PID: $TRACE_AGENT_PID)"
    else
      echo "[ERROR] ❌ Datadog APM Trace Agent failed to start!"
      echo "[ERROR] Trace Agent logs:"
      cat /tmp/trace-agent.log | tail -20
    fi
    
    if kill -0 $PROCESS_AGENT_PID 2>/dev/null; then
      echo "[INFO] ✅ Datadog Process Agent is running (PID: $PROCESS_AGENT_PID)"
    else
      echo "[WARN] ⚠️  Datadog Process Agent may have failed to start"
      echo "[WARN] Process Agent logs:"
      cat /tmp/process-agent.log | tail -10
    fi
    
    echo "[INFO] Checking if Trace Agent is listening on port 8126..."
    sleep 2
    if nc -z 127.0.0.1 8126 2>/dev/null; then
      echo "[INFO] ✅ Trace Agent is listening on port 8126"
    else
      echo "[ERROR] ❌ Trace Agent is NOT listening on port 8126!"
      echo "[ERROR] This will cause ddtrace to fail or use agentless mode"
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
