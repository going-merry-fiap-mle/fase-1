echo "[INFO] Iniciando Flask API (desenvolvimento)..."

poetry install --no-root --no-interaction 2>&1 | grep -v "lock file" || true

exec poetry run python -m app.main