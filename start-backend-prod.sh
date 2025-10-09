#!/bin/sh
echo "[INFO] Iniciando Flask API em Produção..."

# Pegar a porta da variável de ambiente (Heroku usa $PORT)
PORT=${PORT:-5000}

echo "[INFO] Backend rodando na porta: ${PORT}"

# Usar Gunicorn para produção
exec gunicorn \
  --bind 0.0.0.0:${PORT} \
  --workers 4 \
  --worker-class sync \
  --timeout 120 \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  app.main:app