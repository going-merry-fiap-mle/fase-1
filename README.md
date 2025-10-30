# fase-1

## Descrição do Projeto e Arquitetura

Este projeto tem como objetivo realizar web scraping no site https://books.toscrape.com/, extrair dados dos livros e disponibilizá-los via uma API REST desenvolvida em Flask.

### Estrutura de Pastas
- **app/**: Backend Flask com Clean Architecture
- **scripts/**: Scripts de scraping e utilitários
- **data/**: Armazenamento dos dados extraídos (CSVs, etc)
- **docs/**: Documentação e diagramas
- **ml_training/**: Scripts de treinamento de modelos ML
- **models/**: Modelos treinados (não versionados)

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

### Quick Start - Desenvolvimento
```bash
# Configurar ambiente
cp .env.dev.example .env.dev

# Subir backend com hot-reload
docker-compose -f docker-compose.dev.yml up -d --build

# Acessar aplicação
# Backend: http://localhost:5000
```

### Quick Start - Produção
```bash
# Instalar Gunicorn (obrigatório para produção)
poetry add gunicorn
poetry lock

# Configurar ambiente
cp .env.prod.example .env.prod

# Subir backend otimizado
docker-compose -f docker-compose.prod.yml up -d --build

# Acessar aplicação
# Backend: http://localhost:5000
```

**Para documentação completa do Docker, incluindo deploy individual, configurações avançadas e troubleshooting, consulte: [docs/docker.md](docs/docker.md)**

## Machine Learning

O projeto inclui um sistema de predição de ratings usando Random Forest Classifier com **treinamento automático**.

**Para documentação completa sobre Machine Learning (arquitetura, endpoints, retreinamento, troubleshooting), consulte: [docs/ml_implementation.md](docs/ml_implementation.md)**

### Quick Start ML

```bash
# 1. Subir o ambiente
docker-compose -f docker-compose.dev.yml up -d

# O modelo treina automaticamente na primeira inicialização se não existir

# 2. Testar endpoint de predição
curl -X POST http://localhost:5000/api/v1/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{"book_id": "uuid-do-livro", "prediction_type": "rating"}'
```

**Nota:** O treinamento é automático. Não é necessário executar comandos manuais.

---
Mais instruções e documentação das rotas da API serão adicionadas conforme o desenvolvimento avança.