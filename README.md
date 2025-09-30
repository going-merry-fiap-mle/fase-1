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

1. Construa a imagem Docker:
   ```bash
   docker build -t fase-1 .
   ```
2. Execute o container:
   ```bash
   docker run --name fase-1 -p 5000:5000 -p 8501:8501 fase-1
   ```

- O backend Flask estará disponível em http://localhost:5000
- O frontend Streamlit estará disponível em http://localhost:8501
