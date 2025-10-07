#!/bin/sh
echo "[INFO] Iniciando Flask API (desenvolvimento)..."

poetry install --no-root 2>&1 | grep -v "lock file" || true

FLASK_APP=api.main:app \
FLASK_ENV=development \
FLASK_DEBUG=1 \
python -c "
import os
os.environ.setdefault('WERKZEUG_RUN_MAIN', 'false')

from werkzeug.serving import run_simple
from api.main import app

print('[INFO] Flask API com hot-reload (stat-based)')

run_simple(
    hostname='0.0.0.0',
    port=5000,
    application=app,
    use_reloader=True,
    use_debugger=True,
    threaded=True,
    reloader_interval=1,
    reloader_type='stat'
)
"