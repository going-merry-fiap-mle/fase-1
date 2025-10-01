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

### Configuração Inicial

```bash
# Desenvolvimento
cp .env.dev.example .env.dev

# Produção
cp .env.prod.example .env.prod
# Gerar SECRET_KEY: python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Ambiente de Desenvolvimento
#### Com hot-reload e debug ativados:

```bash
# Iniciar
docker-compose -f docker-compose.dev.yml up --build

# Em background
docker-compose -f docker-compose.dev.yml up -d --build

# Parar
docker-compose -f docker-compose.dev.yml down
```

### Ambiente de Produção
#### Otimizado e seguro:

```bash
# Iniciar
docker-compose -f docker-compose.prod.yml up --build

# Em background (recomendado)
docker-compose -f docker-compose.prod.yml up -d --build

# Parar
docker-compose -f docker-compose.prod.yml down
```

### URLs dos Serviços

- **Flask API**: http://localhost:5000
- **Streamlit Dashboard**: http://localhost:8501
- **Swagger API Docs**: http://localhost:5000/apidocs
- **Health Check**: http://localhost:5000/api/v1/health

### Comandos Úteis

```bash
# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Ver status
docker-compose -f docker-compose.prod.yml ps

# Verificar recursos
docker stats

# Rebuild sem cache
docker-compose -f docker-compose.prod.yml build --no-cache

# Limpar tudo
docker-compose -f docker-compose.prod.yml down -v
```

### Estrutura dos Arquivos Docker

```
.
├── Dockerfile.dev              # Dev com hot-reload
├── Dockerfile.prod             # Prod multi-stage otimizado
├── docker-compose.dev.yml      # Compose dev
├── docker-compose.prod.yml     # Compose prod
├── .dockerignore              # Arquivos ignorados
├── start-dev.sh               # Script dev
└── start-prod.sh              # Script prod
```

---
Mais instruções e documentação das rotas da API serão adicionadas conforme o desenvolvimento avança.
