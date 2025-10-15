#!/bin/sh
echo "[INFO] Iniciando Streamlit Dashboard (desenvolvimento)..."

poetry install --no-root 2>&1 | grep -v "lock file" || true

API_URL=${API_URL:-http://backend-dev:5000}
=
PORT_TO_USE=${PORT:-8501}

echo "[INFO] API URL: ${API_URL}"

exec streamlit run frontend/app.py \
  --server.port=$PORT_TO_USE \
  --server.address=0.0.0.0 \
  --server.runOnSave=true \
  --server.headless=true \
  --browser.gatherUsageStats=false