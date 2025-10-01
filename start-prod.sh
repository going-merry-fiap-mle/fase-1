#!/bin/sh
# Script de inicializacao do ambiente de producao
# Projeto: FIAP Fase 1 - API de Livros
# Descricao: Inicia Flask e Streamlit em modo producao

echo "[INFO] Inicializando ambiente de producao..."

# Iniciar Flask em modo producao (SEM hot-reload)
python -c "
from api.main import app
import os

host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', 5000))

print('[INFO] Flask inicializado em modo producao')

app.run(
    host=host,
    port=port,
    debug=False,
    use_reloader=False,
    threaded=True
)
" &

FLASK_PID=$!

# Aguardar Flask inicializar
sleep 3

# Iniciar Streamlit em modo producao
streamlit run frontend/app.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=true \
  --browser.gatherUsageStats=false &

STREAMLIT_PID=$!

echo ""
echo "========================================="
echo "Ambiente de Producao Iniciado"
echo "========================================="
echo ""
echo "Servicos disponiveis:"
echo "  - API Flask:       http://localhost:5000"
echo "  - Documentacao:    http://localhost:5000/apidocs"
echo "  - Health Check:    http://localhost:5000/api/v1/health"
echo "  - Streamlit:       http://localhost:8501"
echo ""
echo "Modo:                Producao"
echo "Hot-reload:          DESATIVADO"
echo "Debug:               DESATIVADO"
echo ""
echo "Para aplicar mudancas, reconstrua a imagem:"
echo "  docker-compose -f docker-compose.prod.yml down"
echo "  docker-compose -f docker-compose.prod.yml up --build"
echo "========================================="
echo ""

# Aguardar processos em background
wait $FLASK_PID $STREAMLIT_PID