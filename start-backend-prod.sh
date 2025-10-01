#!/bin/sh
echo "[INFO] Inicializando Flask API..."

python -c "
from api.main import app
import os

host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', 5000))

print('[INFO] Flask API rodando em producao')

app.run(
    host=host,
    port=port,
    debug=False,
    use_reloader=False,
    threaded=True
)
"