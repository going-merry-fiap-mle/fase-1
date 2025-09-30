FROM python:3.12-slim

WORKDIR /app

# Variáveis de ambiente para otimização do Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH" \
    PYTHONPATH=/app

# Instalar Poetry e curl (para healthcheck)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências primeiro (cache optimization)
COPY pyproject.toml poetry.lock* ./

# Instalar dependências
RUN poetry install --no-interaction --no-ansi --no-root

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p /app/data /app/logs

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expor portas
EXPOSE 5000 8501

# Healthcheck com a URL correta
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/v1/health || exit 1

# Comando direto para iniciar ambos os serviços usando módulos Python
CMD sh -c "python -m api.main & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false & wait"