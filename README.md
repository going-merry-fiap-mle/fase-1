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

### Quick Start - Desenvolvimento
```bash
# Configurar ambiente
cp .env.dev.example .env.dev

# Subir backend e frontend com hot-reload
docker-compose -f docker-compose.dev.yml up -d --build

# Acessar aplicações
# Backend: http://localhost:5000
# Frontend: http://localhost:8501
```

### Quick Start - Produção
```bash
# Instalar Gunicorn (obrigatório para produção)
poetry add gunicorn
poetry lock

# Configurar ambiente
cp .env.prod.example .env.prod

# Subir aplicações otimizadas
docker-compose -f docker-compose.prod.yml up -d --build

# Acessar aplicações
# Backend: http://localhost:5000
# Frontend: http://localhost:8501
```

**Para documentação completa do Docker, incluindo deploy individual, configurações avançadas e troubleshooting, consulte: [docs/docker.md](docs/docker.md)**

---
Mais instruções e documentação das rotas da API serão adicionadas conforme o desenvolvimento avança.