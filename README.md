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

### Ambiente de Produção

```bash
# Clone o repositório
git clone git@github.com:going-merry-fiap-mle/fase-1.git
cd fase-1

# Build e execução com Docker Compose
docker-compose up --build

# Ou executar em background
docker-compose up -d --build

# Para parar os serviços
docker-compose down
```

### Ambiente de Desenvolvimento (com hot-reload)

```bash
# Executar com arquivo de desenvolvimento
docker-compose -f docker-compose.dev.yml up --build

# As mudanças nos arquivos Python serão refletidas automaticamente
# Porta 5678 disponível para debug remoto com debugpy
```

### URLs dos Serviços

- **Flask API**: http://localhost:5000
- **Streamlit Dashboard**: http://localhost:8501
- **Swagger API Docs**: http://localhost:5000/apidocs
- **Health Check**: http://localhost:5000/api/v1/health

### Comandos Docker Úteis

```bash
# Ver logs dos containers
docker-compose logs -f

# Executar comandos dentro do container
docker-compose exec app bash

# Verificar status dos serviços
docker-compose ps

# Rebuild sem cache
docker-compose build --no-cache
docker-compose up

# Limpar volumes e containers
docker-compose down -v
```

### Estrutura dos Arquivos Docker

```
.
├── Dockerfile              # Imagem única otimizada
├── docker-compose.yml      # Configuração de produção
├── docker-compose.dev.yml  # Configuração de desenvolvimento
└── .dockerignore          # Arquivos ignorados no build
```

---
Mais instruções e documentação das rotas da API serão adicionadas conforme o desenvolvimento avança.
