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

## **Como rodar o projeto com Docker**

### **Pré-requisitos**
- Docker instalado (versão 20.10+)
- Docker Compose instalado (versão 2.0+)

### **Arquitetura Docker**
O projeto utiliza containers separados para backend e frontend:
- **Backend (Flask API)**: Container isolado com a API REST
- **Frontend (Streamlit)**: Container isolado com o dashboard
- **Comunicação**: Via rede Docker interna

### **Configuração Inicial**

```bash
# Para desenvolvimento
cp .env.dev.example .env.dev

# Para produção
cp .env.prod.example .env.prod

# IMPORTANTE: Em produção, gere uma SECRET_KEY segura
python3 -c "import secrets; print(secrets.token_hex(32))"
# Adicione a chave gerada no arquivo .env.prod
```

### **Ambiente de Desenvolvimento**

```bash
# Subir backend e frontend juntos
docker-compose -f docker-compose.dev.yml up -d --build

# Subir apenas o backend
docker-compose -f docker-compose.dev.yml up -d --build backend-dev

# Subir apenas o frontend
docker-compose -f docker-compose.dev.yml up -d --build frontend-dev

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Parar tudo
docker-compose -f docker-compose.dev.yml down
```

### **Ambiente de Produção**

⚠️ **IMPORTANTE: Preparação para Produção**

**Antes de fazer deploy em produção, instale o Gunicorn:**

```bash
# Adicionar Gunicorn ao projeto (OBRIGATÓRIO para produção)
poetry add gunicorn
poetry lock

# Isso garante que o servidor WSGI estará disponível para produção
# O Gunicorn é necessário tanto para Docker quanto para Heroku
```

**Deploy Completo (Backend + Frontend)**

```bash
# Subir ambos os serviços
docker-compose -f docker-compose.prod.yml up -d --build

# Ver status
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Parar tudo
docker-compose -f docker-compose.prod.yml down
```

**Deploy Individual de Serviços**

```bash
# Subir APENAS o backend
docker-compose -f docker-compose.prod.yml up -d --build backend

# Subir APENAS o frontend
docker-compose -f docker-compose.prod.yml up -d --build frontend

# Ver logs de um serviço específico
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Reiniciar um serviço específico
docker-compose -f docker-compose.prod.yml restart backend
docker-compose -f docker-compose.prod.yml restart frontend

# Parar um serviço específico
docker-compose -f docker-compose.prod.yml stop backend
docker-compose -f docker-compose.prod.yml stop frontend

# Atualizar apenas um serviço (rebuild)
docker-compose -f docker-compose.prod.yml up -d --build backend
docker-compose -f docker-compose.prod.yml up -d --build frontend
```

### **URLs dos Serviços**

- **Backend API**: http://localhost:5000
- **Frontend Dashboard**: http://localhost:8501
- **API Docs (Swagger)**: http://localhost:5000/apidocs
- **Health Check (Backend)**: http://localhost:5000/api/v1/health

### **Comandos Úteis**

**Monitoramento**

```bash
# Ver status dos serviços
docker-compose -f docker-compose.prod.yml ps

# Ver logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f

# Ver uso de recursos
docker stats
```

**Manutenção**

```bash
# Rebuild sem cache (força reconstrução)
docker-compose -f docker-compose.prod.yml build --no-cache

# Parar e remover tudo (containers, redes, volumes)
docker-compose -f docker-compose.prod.yml down -v

# Remover imagens também
docker-compose -f docker-compose.prod.yml down -v --rmi all
```

### **Estrutura dos Arquivos Docker**

```
projeto/
├── Dockerfile.backend.dev       # Backend desenvolvimento (hot-reload)
├── Dockerfile.backend.prod      # Backend produção (Gunicorn)
├── Dockerfile.frontend.dev      # Frontend desenvolvimento (hot-reload)
├── Dockerfile.frontend.prod     # Frontend produção (otimizado)
├── docker-compose.dev.yml       # Orquestração desenvolvimento
├── docker-compose.prod.yml      # Orquestração produção
├── start-backend-dev.sh         # Script inicialização backend dev
├── start-backend-prod.sh        # Script inicialização backend prod (Gunicorn)
├── start-frontend-dev.sh        # Script inicialização frontend dev
├── start-frontend-prod.sh       # Script inicialização frontend prod
├── .dockerignore               # Arquivos ignorados no build
├── .env.dev.example            # Exemplo configuração dev
├── .env.prod.example           # Exemplo configuração prod
├── .env.dev                    # Configuração dev (não versionado)
└── .env.prod                   # Configuração prod (não versionado)
```

### **Troubleshooting**

**No Windows PowerShell**

Use comandos em uma linha ou Docker Compose:

```bash
# Recomendado no Windows
docker-compose -f docker-compose.prod.yml up -d --build
```

**Porta já em uso**

```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000

# Parar todos containers do projeto
docker-compose -f docker-compose.prod.yml down
```

**Frontend não conecta ao backend**

```bash
# Verificar se ambos estão rodando
docker-compose -f docker-compose.prod.yml ps

# Ver logs para identificar erros
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
```

**Container não inicia**

```bash
# Ver logs detalhados
docker-compose -f docker-compose.prod.yml logs

# Rebuild forçado
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

**"Image not found"**

```bash
# Sempre use --build na primeira vez
docker-compose -f docker-compose.prod.yml up -d --build
```

**Erro "Gunicorn not found"**

```bash
# Se aparecer erro de Gunicorn não encontrado, execute:
poetry add gunicorn
poetry lock

# Depois rebuild a imagem
docker-compose -f docker-compose.prod.yml build --no-cache backend
```

### **Notas Importantes**

---
Mais instruções e documentação das rotas da API serão adicionadas conforme o desenvolvimento avança.
