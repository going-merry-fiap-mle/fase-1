#!/bin/bash

set -e

echo "[INFO] Starting Datadog integration for Heroku Docker deployment..."

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
    
    export DD_AGENT_HOST="127.0.0.1"
    export DD_TRACE_AGENT_PORT="8126"
    export DD_DOGSTATSD_PORT="8125"
    
    echo "[INFO] Datadog configuration:"
    echo "  DD_SITE: $DD_SITE"
    echo "  DD_SERVICE: $DD_SERVICE"
    echo "  DD_ENV: $DD_ENV"
    echo "  DD_AGENT_HOST: $DD_AGENT_HOST"
    echo "  DD_TRACE_AGENT_PORT: $DD_TRACE_AGENT_PORT"
    
    echo "[INFO] Starting Datadog Agent..."
    datadog-agent run > /tmp/datadog-agent.log 2>&1 &
    DD_AGENT_PID=$!
    
    echo "[INFO] Starting Datadog APM Trace Agent..."
    /opt/datadog-agent/embedded/bin/trace-agent --config=/etc/datadog-agent/datadog.yaml > /tmp/trace-agent.log 2>&1 &
    TRACE_AGENT_PID=$!
    
    echo "[INFO] Starting Datadog Process Agent..."
    /opt/datadog-agent/embedded/bin/process-agent --config=/etc/datadog-agent/datadog.yaml > /tmp/process-agent.log 2>&1 &
    PROCESS_AGENT_PID=$!
    
    sleep 3
    
    if kill -0 $DD_AGENT_PID 2>/dev/null; then
      echo "[INFO] ✅ Datadog Agent started successfully (PID: $DD_AGENT_PID)"
    else
      echo "[WARN] ⚠️  Datadog Agent may have failed to start"
      cat /tmp/datadog-agent.log
    fi
    
    if kill -0 $TRACE_AGENT_PID 2>/dev/null; then
      echo "[INFO] ✅ Datadog APM Trace Agent started successfully (PID: $TRACE_AGENT_PID)"
    else
      echo "[WARN] ⚠️  Datadog APM Trace Agent may have failed to start"
      cat /tmp/trace-agent.log
    fi
    
    if kill -0 $PROCESS_AGENT_PID 2>/dev/null; then
      echo "[INFO] ✅ Datadog Process Agent started successfully (PID: $PROCESS_AGENT_PID)"
    else
      echo "[WARN] ⚠️  Datadog Process Agent may have failed to start"
      cat /tmp/process-agent.log
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
