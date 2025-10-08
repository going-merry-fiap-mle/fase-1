#!/bin/sh
echo "[INFO] Inicializando Streamlit Dashboard em Produção..."

# Pegar porta da variável de ambiente (Heroku usa $PORT)
PORT=${PORT:-8501}

# API URL configurável
API_URL=${API_URL:-http://backend:5000}

echo "[INFO] Frontend rodando na porta: ${PORT}"
echo "[INFO] API URL: ${API_URL}"

exec streamlit run frontend/app.py \
  --server.port=${PORT} \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=true \
  --server.enableXsrfProtection=true \
  --browser.gatherUsageStats=false