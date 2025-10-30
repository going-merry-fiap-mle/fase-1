#!/bin/sh
echo "[INFO] Iniciando Flask API em Produção..."

# Pegar a porta da variável de ambiente (Heroku usa $PORT)
PORT=${PORT:-5000}

echo "[INFO] Backend rodando na porta: ${PORT}"
if command -v alembic >/dev/null 2>&1; then
  echo "[INFO] Running alembic migrations..."
  alembic upgrade head || echo "[WARN] Alembic migrations failed or skipped; continuing startup"
else
  echo "[WARN] alembic not installed in environment; skipping migrations"
fi


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