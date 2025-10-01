#!/bin/sh
echo "[INFO] Inicializando Streamlit Dashboard..."

API_URL=${API_URL:-http://backend:5000}

echo "[INFO] API URL: ${API_URL}"

exec streamlit run frontend/app.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=true \
  --browser.gatherUsageStats=false