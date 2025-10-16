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
- **Descrição:** Inicia backend com hot-reload ativado
- **URLs de acesso:**
  - Backend: http://localhost:5000

### Subir serviços individualmente
- **Backend apenas:** `docker-compose -f docker-compose.dev.yml up -d backend-dev`
- **Observação:** Serviços são independentes e podem rodar separadamente

### Monitorar logs
- **Comando:** `docker-compose -f docker-compose.dev.yml logs -f`
- **Descrição:** Acompanha logs em tempo real do backend
- **Logs específicos:** Adicione `backend-dev` ao comando

### Parar serviços
- **Comando:** `docker-compose -f docker-compose.dev.yml down`
- **Descrição:** Para e remove todos os containers
- **Com volumes:** Adicione `-v` para limpar volumes também

---

## 3. Ambiente de Produção

### Deploy completo
- **Comando:** `docker-compose -f docker-compose.prod.yml up -d --build`
- **Descrição:** Inicia backend (Gunicorn) otimizado
- **Verificação:** `docker-compose -f docker-compose.prod.yml ps`

### Deploy individual
- **Backend:** `docker-compose -f docker-compose.prod.yml up -d --build backend`
- **Observação:** Cada serviço roda independentemente

### Comandos de gerenciamento
- **Ver status:** `docker-compose -f docker-compose.prod.yml ps`
- **Reiniciar serviço:** `docker-compose -f docker-compose.prod.yml restart backend`
- **Parar serviço:** `docker-compose -f docker-compose.prod.yml stop backend`
- **Ver logs:** `docker-compose -f docker-compose.prod.yml logs -f backend`

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
```
- **Via linha de comando:**
```bash
BACKEND_PORT=8080 docker-compose -f docker-compose.prod.yml up -d
```

### Monitoramento de recursos
- **Comando:** `docker stats`
- **Descrição:** Exibe uso de CPU e memória em tempo real
- **Específico:** `docker stats fiap-backend-prod`

### Comandos de debug
- **Entrar no container backend:** `docker exec -it fiap-backend-prod /bin/sh`
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

### Docker Compose
- **docker-compose.dev.yml** - Orquestração para desenvolvimento
- **docker-compose.prod.yml** - Orquestração para produção

### Scripts de inicialização
- **start-backend-dev.sh** - Inicia Flask em modo desenvolvimento
- **start-backend-prod.sh** - Inicia Gunicorn em produção

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
---

## Observações

- Arquivos `.env.dev` e `.env.prod` **nunca** devem ser commitados
- Hot-reload disponível apenas em desenvolvimento
- Gunicorn obrigatório para produção
- Firefox/Selenium já configurados em modo headless
- PostgreSQL requer `psycopg2-binary` (já incluído)