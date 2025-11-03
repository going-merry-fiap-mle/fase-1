# fase-1

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-3.0-green?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-15-blue?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-enabled-blue?logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/tests-180%20passed-brightgreen)
![Architecture](https://img.shields.io/badge/architecture-clean%20%2B%20hexagonal-orange)
![ML](https://img.shields.io/badge/ML-ready-purple)
![License](https://img.shields.io/badge/license-MIT-blue)

## Links Importantes

- **Vídeo de Apresentação:**: [ADICIONAR LINK DO VÍDEO AQUI]
- **Repositório GitHub:**: https://github.com/going-merry-fiap-mle/fase-1
- **Link do ambiente produtivo**: https://fase-1-backend-dev-602c0b3ce639.herokuapp.com/apidocs/

---

## Descrição do Projeto e Arquitetura

Este projeto tem como objetivo realizar web scraping no site https://books.toscrape.com/, extrair dados dos livros e disponibilizá-los via uma API REST desenvolvida em Flask.

### Arquitetura Visual

O projeto segue **Clean Architecture / Hexagonal Architecture** com separação clara de responsabilidades.

**Diagramas completos:** [docs/architecture-diagrams.md](docs/architecture-diagrams.md)

#### Pipeline de Dados

```mermaid
graph LR
    A[Web Site<br/>toscrape.com] --> B[Selenium<br/>Scraping]
    B --> C[(PostgreSQL<br/>Database)]
    C --> D[REST API<br/>Flask]
    C --> E[ML Training<br/>Random Forest]
    E --> F[Models<br/>*.pkl]
    F --> D
    D --> G[Data Scientists<br/>GET /ml/training-data]
    D --> H[ML Engineers<br/>POST /ml/predictions]
```

**Ver diagramas detalhados:**
- [Arquitetura Geral (Clean Architecture)](docs/architecture-diagrams.md#1-arquitetura-geral-do-sistema-cleanhexagonal)
- [Pipeline Completo de Dados](docs/architecture-diagrams.md#2-pipeline-completo-de-dados)
- [Integração Machine Learning](docs/architecture-diagrams.md#3-integração-machine-learning)
- [Escalabilidade Futura](docs/architecture-diagrams.md#4-arquitetura-de-escalabilidade-futura)
- [Fluxo de Dados para Data Scientists](docs/architecture-diagrams.md#5-fluxo-de-dados-para-data-scientists)
- [Fluxo de Dados para ML Engineers](docs/architecture-diagrams.md#6-fluxo-de-dados-para-ml-engineers)

### Estrutura de Pastas
- **app/**: Backend Flask com Clean Architecture
- **scripts/**: Scripts de scraping e utilitários
- **data/**: Armazenamento dos dados extraídos (CSVs, etc)
- **docs/**: Documentação e diagramas
- **ml_training/**: Scripts de treinamento de modelos ML
- **models/**: Modelos treinados (não versionados)

### Tecnologias e Versões

| Categoria | Tecnologia | Versão | Justificativa |
|-----------|-----------|---------|---------------|
| **Backend** | Python | 3.12 | Tipagem moderna, performance melhorada |
| **Framework** | Flask | 3.0 | Leveza e flexibilidade para APIs REST |
| **ORM** | SQLAlchemy | 2.0 | Migrations com Alembic, suporte robusto |
| **Banco de Dados** | PostgreSQL | 15 | ACID, JSON support, escalabilidade |
| **Validação** | Pydantic | 2.x | Validação de schemas, type safety |
| **Autenticação** | JWT | - | Stateless, escalável, seguro |
| **Web Scraping** | Selenium | 4.x | Automação de browser, suporte JavaScript |
| **Machine Learning** | scikit-learn | 1.7.2 | Random Forest, encoders, pipelines |
| **Serialização ML** | joblib | 1.5.2 | Persistência eficiente de modelos |
| **Containers** | Docker | 20.10+ | Ambientes dev/prod idênticos |
| **Documentação** | Swagger/Flasgger | 0.9.x | Auto-documentação interativa de API |
| **Testes** | pytest | 7.x | 180 testes unitários implementados |
| **Logs** | Python logging | stdlib | Logs estruturados em JSON |

---

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

## Como rodar o projeto com Docker

### Quick Start
```bash
# Configurar ambiente
cp .env.example .env

# Subir backend com hot-reload
docker-compose up -d --build

# Acessar aplicação
# Backend: http://localhost:5000
```

**Para documentação completa de deployment, incluindo Docker, configurações avançadas e troubleshooting, consulte: [docs/deployment.md](docs/deployment.md)**

## Machine Learning

O projeto inclui um sistema de predição de ratings usando Random Forest Classifier com **treinamento automático**.

**Para documentação completa sobre Machine Learning (arquitetura, endpoints, retreinamento, troubleshooting), consulte: [docs/machine-learning.md](docs/machine-learning.md)**

### Quick Start ML

```bash
# 1. Subir o ambiente
docker-compose up -d

# O modelo treina automaticamente na primeira inicialização se não existir

# 2. Testar endpoint de predição
curl -X POST http://localhost:5000/api/v1/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{"book_id": "uuid-do-livro", "prediction_type": "rating"}'
```

**Nota:** O treinamento é automático. Não é necessário executar comandos manuais.

## Autenticação JWT

A API utiliza autenticação JWT (JSON Web Token) para proteger rotas sensíveis.

### Login
**Endpoint:** `POST /api/v1/auth/login`

**Credenciais padrão:**
- **Username:** `admin`
- **Password:** `admin123`

**Exemplo de requisição:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Refresh Token
**Endpoint:** `POST /api/v1/auth/refresh`

### Endpoints Protegidos

#### Requer Token JWT (qualquer usuário autenticado):
- `GET /api/v1/scraping/status/{task_id}` - Consultar status do scraping

#### Requer Permissão de Admin:
- `GET /api/v1/scraping` - Iniciar web scraping
- `GET /api/v1/books` - Listar livros
- `GET /api/v1/books/{book_id}` - Buscar livro por ID

### Como usar o token

Incluir o token no header `Authorization` das requisições:

```bash
curl -X GET http://localhost:5000/api/v1/scraping \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

### Swagger UI

Acesse `http://localhost:5000/apidocs/` para testar os endpoints via interface web. Use o botão "Authorize" para inserir o token JWT.

---

## Documentação das Rotas da API

### Endpoints Implementados

A API possui 20+ endpoints divididos em categorias:

#### Endpoints Obrigatórios (Core)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/books` | Lista todos os livros (paginado) |
| GET | `/api/v1/books/{id}` | Retorna detalhes de um livro específico |
| GET | `/api/v1/books/search` | Busca livros por título e/ou categoria |
| GET | `/api/v1/categories` | Lista todas as categorias disponíveis |
| GET | `/api/v1/health` | Verifica status da API e conectividade com dados |

#### Endpoints Opcionais (Insights)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/stats/overview` | Estatísticas gerais da coleção |
| GET | `/api/v1/stats/categories` | Estatísticas detalhadas por categoria |
| GET | `/api/v1/books/top-rated` | Lista livros com melhor avaliação |
| GET | `/api/v1/books/price-range` | Filtra livros por faixa de preço |

#### Endpoints Bônus (Autenticação)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/auth/login` | Obter token JWT |
| POST | `/api/v1/auth/refresh` | Renovar token JWT |

#### Endpoints Bônus (Pipeline ML-Ready)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/ml/features` | Dados formatados para features ML |
| GET | `/api/v1/ml/manifest` | Schema das features |
| GET | `/api/v1/ml/training-data` | Dataset para treinamento (JSON/CSV) |
| POST | `/api/v1/ml/predictions` | Criar/executar predições ML |

### Exemplos de Uso

#### 1. Listar todos os livros (paginado)

```bash
curl -X GET "http://localhost:5000/api/v1/books?page=1&per_page=10"
```

**Resposta:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "A Light in the Attic",
      "price": "51.77",
      "rating": 3,
      "availability": "In stock",
      "category": "Poetry",
      "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 100,
    "total_pages": 10
  }
}
```

#### 2. Buscar livros por título

```bash
curl -X GET "http://localhost:5000/api/v1/books/search?title=Light&page=1&per_page=5"
```

**Resposta:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "A Light in the Attic",
      "price": "51.77",
      "rating": 3,
      "availability": "In stock",
      "category": "Poetry"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 5,
    "total_items": 1,
    "total_pages": 1
  }
}
```

#### 3. Obter estatísticas gerais

```bash
curl -X GET "http://localhost:5000/api/v1/stats/overview"
```

**Resposta:**
```json
{
  "total_books": 1000,
  "avg_price": 35.67,
  "rating_distribution": {
    "1": 50,
    "2": 100,
    "3": 250,
    "4": 350,
    "5": 200,
    "unknown": 50
  }
}
```

#### 4. Exportar dataset para treinamento ML (CSV)

```bash
curl -X GET "http://localhost:5000/api/v1/ml/training-data?format=csv&label=rating" \
  --output training_data.csv
```

#### 5. Executar predição ML em tempo real

```bash
curl -X POST "http://localhost:5000/api/v1/ml/predictions" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "550e8400-e29b-41d4-a716-446655440000",
    "prediction_type": "rating"
  }'
```

**Resposta:**
```json
{
  "prediction": {
    "book_id": "550e8400-e29b-41d4-a716-446655440000",
    "book_title": "A Light in the Attic",
    "predicted_value": "0",
    "predicted_label": "Low Rating (<4)",
    "confidence": 0.62,
    "features_used": {
      "price": 51.77,
      "category": "Poetry",
      "availability": "In stock"
    },
    "model_version": "v1.0.0",
    "from_cache": false
  },
  "saved_prediction_id": "uuid-da-predicao"
}
```

### Documentação Completa

Para documentação detalhada de todos os endpoints, parâmetros, respostas de erro e exemplos adicionais, consulte:

- **Referência completa da API:** [docs/api-reference.md](docs/api-reference.md)
- **Machine Learning:** [docs/machine-learning.md](docs/machine-learning.md)
- **Swagger UI (Interativa):** http://localhost:5000/apidocs/

---