# Documentação Docker

Esta documentação descreve como configurar e executar a aplicação usando Docker.

---

## Pré-requisitos
- Docker 20.10+ e Docker Compose 2.0+
- Sistema operacional: Windows, Linux ou macOS
- Memória recomendada: 4GB RAM disponível

## Preparar variáveis de ambiente
- Copie o template e ajuste:

```bash
cp .env.example .env
```

- Gerar SECRET_KEY (opcional):

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

> Observação: o arquivo `.env` nunca deve ser commitado.

---

## Subir o ambiente

```bash
# Subir todos os serviços com hot-reload
docker-compose up -d --build

# Verificar status
docker-compose ps

# Parar e remover containers
docker-compose down
```

### Logs

```bash
docker-compose logs -f
# Logs específicos do backend
docker logs fiap-backend -f
```

---

## Banco de dados (Heroku/Postgres)
Configure a variável `DATABASE_URL` no arquivo `.env`:

```bash
DATABASE_URL=postgres://user:password@host:5432/database
```

Verifique a conexão dentro do container:

```bash
docker exec fiap-backend python -c "import psycopg2, os; conn = psycopg2.connect(os.getenv('DATABASE_URL')); print('✅ Conectado'); conn.close()"
```

---

## Firefox / Selenium
Os containers já incluem Firefox/Gecko e Selenium configurados para uso headless quando necessário.

---

## Arquivos principais
- `Dockerfile.backend` - Backend Flask API
- `docker-compose.yml` - Orquestração de serviços
- `start-backend.sh` - Script auxiliar para iniciar o backend

---

## Troubleshooting rápido

- Porta 5000 ocupada (Windows):

```bash
netstat -ano | findstr :5000
```

- Rebuild forçado:

```bash
docker-compose build --no-cache
```

- Down completo e limpeza de volumes:

```bash
docker-compose down -v
```

---

## Observações
- Fluxo padrão do repositório: configuração local via `docker-compose.yml` e `.env`.
- Não comitar `.env` ou chaves sensíveis.
