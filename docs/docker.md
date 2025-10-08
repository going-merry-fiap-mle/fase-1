# Documentação Docker

Esta documentação descreve como configurar, executar e gerenciar a aplicação usando Docker, tanto para desenvolvimento quanto para produção.

---

## 1. Configuração Inicial

### Pré-requisitos
- **Versão mínima:** Docker 20.10+ e Docker Compose 2.0+
- **Sistema operacional:** Windows, Linux ou macOS
- **Memória recomendada:** 4GB RAM disponível

### Preparar variáveis de ambiente
- **Desenvolvimento:** `cp .env.dev.example .env.dev`
- **Produção:** `cp .env.prod.example .env.prod`
- **Gerar SECRET_KEY:** `python3 -c "import secrets; print(secrets.token_hex(32))"`

### Configurar Banco de Dados
- **Biblioteca necessária:** `psycopg2-binary` (já incluída no pyproject.toml)
- **DATABASE_URL:** Configure nos arquivos `.env.dev` e `.env.prod`
- **Formato PostgreSQL:** `postgres://user:password@host:port/database`
- **Exemplo Heroku:** As credenciais do Heroku devem ser copiadas do dashboard
- **Observação:** Nunca commite os arquivos `.env.dev` e `.env.prod` (já estão no .gitignore)

### Instalar Gunicorn (produção)
- **Comando:** `poetry add gunicorn && poetry lock`
- **Descrição:** Servidor WSGI necessário para ambiente de produção
- **Observação:** Obrigatório antes do deploy em produção

---

## 2. Ambiente de Desenvolvimento

### Subir todos os serviços
- **Comando:** `docker-compose -f docker-compose.dev.yml up -d --build`
- **Descrição:** Inicia backend e frontend com hot-reload ativado
- **URLs de acesso:**
  - Backend: http://localhost:5000
  - Frontend: http://localhost:8501

### Subir serviços individualmente
- **Backend apenas:** `docker-compose -f docker-compose.dev.yml up -d backend-dev`
- **Frontend apenas:** `docker-compose -f docker-compose.dev.yml up -d frontend-dev`
- **Observação:** Serviços são independentes e podem rodar separadamente

### Monitorar logs
- **Comando:** `docker-compose -f docker-compose.dev.yml logs -f`
- **Descrição:** Acompanha logs em tempo real de ambos os serviços
- **Logs específicos:** Adicione `backend-dev` ou `frontend-dev` ao comando

### Parar serviços
- **Comando:** `docker-compose -f docker-compose.dev.yml down`
- **Descrição:** Para e remove todos os containers
- **Com volumes:** Adicione `-v` para limpar volumes também

---

## 3. Ambiente de Produção

### Deploy completo
- **Comando:** `docker-compose -f docker-compose.prod.yml up -d --build`
- **Descrição:** Inicia backend (Gunicorn) e frontend otimizados
- **Verificação:** `docker-compose -f docker-compose.prod.yml ps`

### Deploy individual
- **Backend:** `docker-compose -f docker-compose.prod.yml up -d --build backend`
- **Frontend:** `docker-compose -f docker-compose.prod.yml up -d --build frontend`
- **Observação:** Cada serviço roda independentemente

### Comandos de gerenciamento
- **Ver status:** `docker-compose -f docker-compose.prod.yml ps`
- **Reiniciar serviço:** `docker-compose -f docker-compose.prod.yml restart [backend|frontend]`
- **Parar serviço:** `docker-compose -f docker-compose.prod.yml stop [backend|frontend]`
- **Ver logs:** `docker-compose -f docker-compose.prod.yml logs -f [backend|frontend]`

### Atualizar serviço específico
```bash
# Exemplo para backend
docker-compose -f docker-compose.prod.yml stop backend
docker-compose -f docker-compose.prod.yml up -d --build backend
```

---

## 4. Configurações Avançadas

### Portas customizadas
- **Via arquivo .env.prod:**
```bash
BACKEND_PORT=8080    # Backend na porta 8080
FRONTEND_PORT=3000   # Frontend na porta 3000
```
- **Via linha de comando:**
```bash
BACKEND_PORT=8080 FRONTEND_PORT=3000 docker-compose -f docker-compose.prod.yml up -d
```

### Monitoramento de recursos
- **Comando:** `docker stats`
- **Descrição:** Exibe uso de CPU e memória em tempo real
- **Específico:** `docker stats fiap-backend-prod fiap-frontend-prod`

### Comandos de debug
- **Entrar no container backend:** `docker exec -it fiap-backend-prod /bin/sh`
- **Entrar no container frontend:** `docker exec -it fiap-frontend-prod /bin/sh`
- **Ver logs detalhados:** `docker logs --details [container-name]`

---

## 5. Heroku PostgreSQL

### Configuração
Configure a variável `DATABASE_URL` nos arquivos `.env.dev` e `.env.prod`:
```bash
DATABASE_URL=postgres://user:password@host.amazonaws.com:5432/database
```

Obtenha as credenciais em: https://dashboard.heroku.com/apps → Resources → Database

### Verificar conexão
```bash
docker exec fiap-backend-dev python -c "import psycopg2; import os; conn = psycopg2.connect(os.getenv('DATABASE_URL')); print('✅ Conectado'); conn.close()"
```

---

## 6. Firefox/Selenium

Os containers já incluem Firefox ESR e Selenium configurados em modo headless.

---

## 7. Estrutura de Arquivos

### Dockerfiles
- **Dockerfile.backend.dev** - Backend com hot-reload para desenvolvimento
- **Dockerfile.backend.prod** - Backend otimizado com Gunicorn
- **Dockerfile.frontend.dev** - Frontend com hot-reload para desenvolvimento
- **Dockerfile.frontend.prod** - Frontend otimizado para produção

### Docker Compose
- **docker-compose.dev.yml** - Orquestração para desenvolvimento
- **docker-compose.prod.yml** - Orquestração para produção

### Scripts de inicialização
- **start-backend-dev.sh** - Inicia Flask em modo desenvolvimento
- **start-backend-prod.sh** - Inicia Gunicorn em produção
- **start-frontend-dev.sh** - Inicia Streamlit desenvolvimento
- **start-frontend-prod.sh** - Inicia Streamlit produção

---

## 8. Troubleshooting

### Porta já em uso
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000

# Solução
docker-compose -f docker-compose.prod.yml down
```

### Container não inicia
```bash
# Ver logs detalhados
docker-compose -f docker-compose.prod.yml logs

# Rebuild forçado
docker-compose -f docker-compose.prod.yml build --no-cache
```

### Erro "Gunicorn not found"
```bash
# Instalar Gunicorn
poetry add gunicorn
poetry lock

# Rebuild backend
docker-compose -f docker-compose.prod.yml build --no-cache backend
```

### Frontend não conecta ao backend
```bash
# Verificar status dos serviços
docker-compose -f docker-compose.prod.yml ps

# Verificar logs
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
```

---

## Observações

- Backend e Frontend rodam de forma independente
- Arquivos `.env.dev` e `.env.prod` **nunca** devem ser commitados
- Hot-reload disponível apenas em desenvolvimento
- Gunicorn obrigatório para produção
- Firefox/Selenium já configurados em modo headless
- PostgreSQL requer `psycopg2-binary` (já incluído)