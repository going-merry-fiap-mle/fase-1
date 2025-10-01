# fase-1

## Descrição do Projeto e Arquitetura

Este projeto tem como objetivo realizar web scraping no site https://books.toscrape.com/, extrair dados dos livros e disponibilizá-los via uma API REST desenvolvida em Flask. O frontend será feito em Streamlit para visualização dos dados. A arquitetura segue o padrão hexagonal, separando domínio, aplicação e infraestrutura, facilitando testes e manutenção.

### Estrutura de Pastas
- **api/**: Backend Flask
- **frontend/**: Streamlit (dashboard)
- **scripts/**: Scripts de scraping e utilitários
- **data/**: Armazenamento dos dados extraídos (CSVs, etc)
- **docs/**: Documentação e diagramas

## Instruções de Instalação e Configuração

1. Clone o repositório:
   ```bash
   git clone git@github.com:going-merry-fiap-mle/fase-1.git
   cd fase-1
   ```
2. Instale o Poetry (gerenciador de dependências Python):
   ```bash
   pip install poetry
   ```
3. Instale as dependências:
   ```bash
   poetry install
   ```
4. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env` e ajuste conforme necessário.

5. Execute o backend Flask:
   ```bash
   poetry run python api/main.py
   ```
6. Execute o frontend Streamlit:
   ```bash
   poetry run streamlit run frontend/app.py
   ```

## Como rodar o projeto com Docker

### Pré-requisitos
- Docker instalado (versão 20.10+)
- Docker Compose instalado (versão 2.0+)

### Arquitetura Docker
O projeto utiliza containers separados para backend e frontend:
- **Backend (Flask API)**: Container isolado com a API REST
- **Frontend (Streamlit)**: Container isolado com o dashboard
- **Comunicação**: Via rede Docker interna

### Configuração Inicial

```bash
# Desenvolvimento
cp .env.dev.example .env.dev

# Produção
cp .env.prod.example .env.prod
# Gerar SECRET_KEY: python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Ambiente de Desenvolvimento
Com hot-reload e debug ativados em ambos os containers:

```bash
# Iniciar ambos os containers
docker-compose -f docker-compose.dev.yml up --build

# Em background
docker-compose -f docker-compose.dev.yml up -d --build

# Parar ambos
docker-compose -f docker-compose.dev.yml down

# Ver logs do backend
docker-compose -f docker-compose.dev.yml logs -f backend-dev

# Ver logs do frontend
docker-compose -f docker-compose.dev.yml logs -f frontend-dev

# Iniciar apenas o backend
docker-compose -f docker-compose.dev.yml up backend-dev

# Iniciar apenas o frontend
docker-compose -f docker-compose.dev.yml up frontend-dev
```

### Ambiente de Produção
Otimizado e seguro com containers separados:

```bash
# Iniciar ambos os containers
docker-compose -f docker-compose.prod.yml up --build

# Em background (recomendado)
docker-compose -f docker-compose.prod.yml up -d --build

# Parar ambos
docker-compose -f docker-compose.prod.yml down

# Ver logs do backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Ver logs do frontend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### URLs dos Serviços

- **Backend API**: http://localhost:5000
- **Frontend Dashboard**: http://localhost:8501
- **API Docs (Swagger)**: http://localhost:5000/apidocs
- **Health Check (Backend)**: http://localhost:5000/api/v1/health

### Comandos Úteis

```bash
# Ver logs de ambos os containers
docker-compose -f docker-compose.prod.yml logs -f

# Ver status dos containers
docker-compose -f docker-compose.prod.yml ps

# Verificar recursos (CPU, RAM)
docker stats

# Rebuild sem cache
docker-compose -f docker-compose.prod.yml build --no-cache

# Limpar containers e volumes
docker-compose -f docker-compose.prod.yml down -v

# Reiniciar apenas o backend
docker-compose -f docker-compose.prod.yml restart backend

# Reiniciar apenas o frontend
docker-compose -f docker-compose.prod.yml restart frontend
```

### Estrutura dos Arquivos Docker

```
.
├── Dockerfile.backend.dev          # Backend dev com hot-reload
├── Dockerfile.backend.prod         # Backend prod multi-stage
├── Dockerfile.frontend.dev         # Frontend dev com hot-reload
├── Dockerfile.frontend.prod        # Frontend prod multi-stage
├── docker-compose.dev.yml          # Compose dev (2 services)
├── docker-compose.prod.yml         # Compose prod (2 services)
├── start-backend-dev.sh            # Script inicialização backend dev
├── start-backend-prod.sh           # Script inicialização backend prod
├── start-frontend-dev.sh           # Script inicialização frontend dev
├── start-frontend-prod.sh          # Script inicialização frontend prod
└── .dockerignore                   # Arquivos ignorados no build
```

### Troubleshooting
**Porta já está em uso:**
```bash
# Verificar containers rodando
docker ps

# Parar todos os containers do projeto
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.dev.yml down
```
**Frontend não conecta ao backend:**
- Verificar se ambos os containers estão na mesma rede
- Verificar logs: `docker-compose logs -f`
- URL do backend no frontend: `http://backend:5000` (prod) ou `http://backend-dev:5000` (dev)

**Rebuild forçado:**
```bash
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

---
Mais instruções e documentação das rotas da API serão adicionadas conforme o desenvolvimento avança.
