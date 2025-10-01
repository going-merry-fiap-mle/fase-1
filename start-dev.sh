#!/bin/sh
# Script de inicializacao do ambiente de desenvolvimento
# Projeto: FIAP Fase 1 - API de Livros
# Descricao: Inicia Flask com hot-reload (stat-based) e Streamlit

echo "[INFO] Configurando ambiente de desenvolvimento..."

# Instalar dependencias do projeto
poetry install --no-root 2>&1 | grep -v "lock file" || true

echo "[INFO] Iniciando servicos..."

# Iniciar Flask com stat reloader
FLASK_APP=api.main:app \
FLASK_ENV=development \
FLASK_DEBUG=1 \
python -c "
import os
os.environ.setdefault('WERKZEUG_RUN_MAIN', 'false')

from werkzeug.serving import run_simple
from api.main import app

print('[INFO] Flask inicializado com stat reloader')

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
" &

FLASK_PID=$!

# Aguardar inicializacao do Flask
sleep 2

# Iniciar Streamlit
streamlit run frontend/app.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.runOnSave=true \
  --server.headless=true \
  --browser.gatherUsageStats=false 2>&1 | grep -v "Collecting usage" &

STREAMLIT_PID=$!

echo ""
echo "========================================="
echo "Ambiente de Desenvolvimento Iniciado"
echo "========================================="
echo ""
echo "Servicos disponiveis:"
echo "  - API Flask:       http://localhost:5000"
echo "  - Documentacao:    http://localhost:5000/apidocs"
echo "  - Health Check:    http://localhost:5000/api/v1/health"
echo "  - Streamlit:       http://localhost:8501"
echo ""
echo "Hot-reload:          ATIVADO (stat-based polling)"
echo "Modo:                Desenvolvimento"
echo ""
echo "Para parar os servicos, pressione Ctrl+C"
echo "========================================="
echo ""

# Aguardar processos em background
wait $FLASK_PID $STREAMLIT_PID