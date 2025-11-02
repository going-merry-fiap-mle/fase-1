# Documentação Docker

Esta documentação descreve como configurar e executar a aplicação usando Docker — foco em desenvolvimento local.

---

## Pré-requisitos
- Docker 20.10+ e Docker Compose 2.0+
- Sistema operacional: Windows, Linux ou macOS
- Memória recomendada: 4GB RAM disponível

## Preparar variáveis de ambiente
- Copie o template de desenvolvimento e ajuste:

```bash
cp .env.dev.example .env.dev
```

- Gerar SECRET_KEY (opcional):

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

> Observação: o arquivo `.env.dev` nunca deve ser commitado.

---

## Subir o ambiente de desenvolvimento (padrão)

```bash
# Subir todos os serviços em modo desenvolvimento (hot-reload)
docker-compose -f docker-compose.dev.yml up -d --build

# Verificar status
docker-compose -f docker-compose.dev.yml ps

# Parar e remover containers
docker-compose -f docker-compose.dev.yml down
```

### Logs

```bash
docker-compose -f docker-compose.dev.yml logs -f
# Logs específicos do backend
docker logs fiap-backend-dev -f
```

---

## Banco de dados (Heroku/Postgres)
Configure a variável `DATABASE_URL` no arquivo `.env.dev`:

```bash
DATABASE_URL=postgres://user:password@host:5432/database
```

Verifique a conexão dentro do container de desenvolvimento:

```bash
docker exec fiap-backend-dev python -c "import psycopg2, os; conn = psycopg2.connect(os.getenv('DATABASE_URL')); print('✅ Conectado'); conn.close()"
```

---

## Firefox / Selenium (desenvolvimento)
Os containers usados em desenvolvimento já incluem Firefox/Gecko e Selenium configurados para uso headless quando necessário.

---

## Arquivos principais
- `Dockerfile.backend.dev` - Backend com hot-reload para desenvolvimento
- `docker-compose.dev.yml` - Orquestração para desenvolvimento (padrão)
- `start-backend-dev.sh` - Script auxiliar para iniciar o backend em dev

---

## Troubleshooting rápido

- Porta 5000 ocupada (Windows):

```bash
netstat -ano | findstr :5000
```

- Rebuild forçado (desenvolvimento):

```bash
docker-compose -f docker-compose.dev.yml build --no-cache
```

- Down completo e limpeza de volumes:

```bash
docker-compose -f docker-compose.dev.yml down -v
```

---

## Observações
- Fluxo padrão do repositório: desenvolvimento local via `docker-compose.dev.yml` e `.env.dev`.
- Não comitar `.env.dev` ou chaves sensíveis.
