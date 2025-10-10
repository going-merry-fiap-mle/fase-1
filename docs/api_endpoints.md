# Documentação dos Endpoints da API

Esta documentação descreve todos os endpoints REST disponíveis na API do projeto, incluindo obrigatórios, opcionais e de bônus.

---

## 1. Livros

### Listar todos os livros
- **Endpoint:** `GET /api/v1/books`
- **Descrição:** Retorna uma lista de livros disponíveis.
- **Resposta de exemplo:**
```json
{
  "books": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "A Light in the Attic",
      "price": 51.77,
      "rating": 3,
      "availability": "In stock",
      "category": "Poetry",
      "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
    }
  ]
}
```

### Buscar livro por ID
- **Endpoint:** `GET /api/v1/books/{id}`
- **Descrição:** Retorna os detalhes de um livro específico pelo seu ID (UUID).
- **Parâmetros:**
  - `id` (path, UUID): Identificador do livro.
- **Resposta de exemplo:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": 3,
  "availability": "In stock",
  "category": "Poetry",
  "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
}
```

### Buscar livros por título e/ou categoria
- **Endpoint:** `GET /api/v1/books/search?title={title}&category={category}`
- **Descrição:** Busca livros pelo título e/ou categoria informados.
- **Parâmetros:**
  - `title` (query, string, opcional)
  - `category` (query, string, opcional)
- **Resposta de exemplo:**
```json
{
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "A Light in the Attic",
      "price": 51.77,
      "rating": 3,
      "availability": "In stock",
      "category": "Poetry",
      "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
    }
  ]
}
```

---

## 2. Categorias

### Listar todas as categorias
- **Endpoint:** `GET /api/v1/categories`
- **Descrição:** Retorna uma lista de categorias disponíveis.
- **Resposta de exemplo:**
```json
{
  "categories": [
    {
      "id": "c1e1e1e1-e29b-41d4-a716-446655440000",
      "name": "Poetry"
    },
    {
      "id": "c1e1e1e1-e29b-41d4-a716-446655440001",
      "name": "Historical Fiction"
    },
    {
      "id": "c1e1e1e1-e29b-41d4-a716-446655440002",
      "name": "Fiction"
    }
  ]
}
```

---

## 3. Saúde da API

### Verificar status da API
- **Endpoint:** `GET /api/v1/health`
- **Descrição:** Verifica se a API está operacional e se há conectividade com os dados.
- **Resposta de exemplo:**
```json
{
  "status": "ok",
  "message": "API operacional",
  "data_connectivity": true
}
```

---

## 4. Estatísticas (Opcionais)


---

## 5. Autenticação (Bônus)

### Login
- **Endpoint:** `POST /api/v1/auth/login`
- **Descrição:** Autentica usuário e retorna token JWT.
- **Request de exemplo:**
```json
{
  "username": "admin",
  "password": "senha"
}
```
- **Resposta de exemplo:**
```json
{
  "access_token": "...",
  "refresh_token": "..."
}
```

### Refresh Token
- **Endpoint:** `POST /api/v1/auth/refresh`
- **Descrição:** Renova o token JWT.
- **Request de exemplo:**
```json
{
  "refresh_token": "..."
}
```
- **Resposta de exemplo:**
```json
{
  "access_token": "..."
}
```

---

## 6. Endpoints para ML (Bônus)

### Dados formatados para features
- **Endpoint:** `GET /api/v1/ml/features`
- **Descrição:** Retorna dados prontos para uso como features em modelos ML.
- **Resposta de exemplo:**
```json
{
  "features": [
    {"title": "...", "price": 20.0, "rating": 4, "category": "..."}
  ]
}
```

### Dataset para treinamento
- **Endpoint:** `GET /api/v1/ml/training-data`
- **Descrição:** Retorna o dataset completo para treinamento de modelos.
- **Resposta de exemplo:**
```json
{
  "data": [
    {"title": "...", "price": 20.0, "rating": 4, "category": "..."}
  ]
}
```

### Receber predições
- **Endpoint:** `POST /api/v1/ml/predictions`
- **Descrição:** Recebe dados e retorna predições do modelo.
- **Request de exemplo:**
```json
{
  "features": [
    {"title": "...", "price": 20.0, "rating": 4, "category": "..."}
  ]
}
```
- **Resposta de exemplo:**
```json
{
  "predictions": [0, 1]
}
```

---

## 7. Documentação Swagger

### Acessar documentação interativa da API
- **Endpoint:** `GET /apidocs/`
- **Descrição:** Exibe a documentação automática dos endpoints da API, gerada via Swagger/Flasgger. Permite testar e visualizar exemplos de requisições e respostas.
- **Resposta:** Interface web interativa.

---

## Observações
- Todos os endpoints retornam respostas no formato JSON, exceto `/apidocs/`, que retorna uma interface web.
- IDs são UUIDs (ex: `550e8400-e29b-41d4-a716-446655440000`).
- Parâmetros de busca devem ser passados via query string.
- Endpoints de autenticação e ML são opcionais/bônus.
- Para mais detalhes sobre a arquitetura e funcionamento, consulte o arquivo `docs/architecture.md`.
