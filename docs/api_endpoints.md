# Documentação dos Endpoints da API

Esta documentação descreve todos os endpoints REST disponíveis na API do projeto, incluindo obrigatórios, opcionais e de bônus.

---

## 1. Livros

### Listar todos os livros
- **Endpoint:** `GET /api/v1/books`
- **Descrição:** Retorna uma lista paginada de livros disponíveis.
- **Parâmetros:**
  - `page` (query, integer, opcional, padrão: 1): Número da página
  - `per_page` (query, integer, opcional, padrão: 10): Itens por página
- **Resposta de exemplo:**
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
- **Descrição:** Busca livros pelo título e/ou categoria informados (busca parcial, case-insensitive).
- **Importante:** Pelo menos um parâmetro de busca (title ou category) deve ser fornecido.
- **Comportamento:**
  - Se apenas `title` for fornecido: busca livros cujo título contenha o valor informado
  - Se apenas `category` for fornecido: busca livros cuja categoria contenha o valor informado
  - Se ambos forem fornecidos: busca livros que satisfaçam **ambas** as condições (AND)
- **Parâmetros:**
  - `title` (query, string, opcional*): Título do livro para buscar
  - `category` (query, string, opcional*): Categoria do livro para buscar
  - `page` (query, integer, opcional, padrão: 1): Número da página
  - `per_page` (query, integer, opcional, padrão: 10): Itens por página
  - *Pelo menos um parâmetro de busca é obrigatório
- **Resposta de sucesso (200):**
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
    "total_items": 15,
    "total_pages": 2
  }
}
```
- **Nota:** A resposta usa `items` (não `results`) para manter consistência com os outros endpoints paginados da API.
- **Resposta de erro (400) - Nenhum parâmetro fornecido:**
```json
{
  "error": "Invalid parameters",
  "message": "At least one search parameter (title or category) must be provided"
}
```

### Buscar livros com maiores avaliações
- **Endpoint:** `GET /api/v1/books/top-rated`
- **Descrição:** Retorna livros ordenados por rating (maior para menor).
- **Comportamento:**
  - Livros são ordenados por rating em ordem decrescente (5, 4, 3, 2, 1)
  - Em caso de empate no rating, são ordenados por título alfabeticamente
  - Suporta paginação
- **Parâmetros:**
  - `page` (query, integer, opcional, padrão: 1): Número da página
  - `per_page` (query, integer, opcional, padrão: 10): Itens por página
- **Resposta de sucesso (200):**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "title": "Advanced Python",
      "price": "49.99",
      "rating": 5,
      "availability": "In stock",
      "category": "Programming",
      "image_url": "https://books.toscrape.com/media/cache/xx/yy/xxyy.jpg"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "title": "Data Science Guide",
      "price": "39.99",
      "rating": 5,
      "availability": "In stock",
      "category": "Data Science",
      "image_url": "https://books.toscrape.com/media/cache/aa/bb/aabb.jpg"
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
- **Resposta de erro (400) - Paginação inválida:**
```json
{
  "error": "Invalid parameters",
  "details": [
    {
      "type": "value_error",
      "loc": ["page"],
      "msg": "Value must be greater than or equal to 1"
    }
  ]
}
```

---

## 2. Categorias

### Listar todas as categorias
- **Endpoint:** `GET /api/v1/categories`
- **Descrição:** Retorna uma lista paginada de categorias disponíveis.
- **Parâmetros:**
  - `page` (query, integer, opcional, padrão: 1): Número da página (mínimo: 1)
  - `per_page` (query, integer, opcional, padrão: 10): Itens por página (mínimo: 1, máximo: 100)
- **Resposta de sucesso (200):**
```json
{
  "items": [
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
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 50,
    "total_pages": 5
  }
}
```
- **Resposta de erro (400) - Paginação inválida:**
```json
{
  "error": "Invalid parameters",
  "details": [
    {
      "type": "value_error",
      "loc": ["page"],
      "msg": "Value must be greater than or equal to 1"
    }
  ]
}
```

---

## 3. Saúde da API

### Verificar status da API
- **Endpoint:** `GET /api/v1/health`
- **Descrição:** Verifica se a API está operacional e testa a conectividade real com o banco de dados através de um `SELECT 1`.
- **Validação:**
  - Executa `SELECT 1` no banco de dados para verificar conectividade
  - Retorna `status: "ok"` se tudo estiver funcionando
  - Retorna `status: "error"` se houver problemas de conexão com o banco
- **Resposta de sucesso:**
```json
{
  "status": "ok",
  "message": "API operacional",
  "data_connectivity": true
}
```
- **Resposta de erro (conexão com banco falhou):**
```json
{
  "status": "error",
  "message": "Erro ao conectar com o banco: Connection refused",
  "data_connectivity": false
}
```

---

## 4. Estatísticas (Opcionais)

### Overview (Estatísticas gerais)
- **Endpoint:** `GET /api/v1/stats/overview`
- **Descrição:** Retorna estatísticas gerais sobre o acervo: total de livros, preço médio e distribuição de ratings (contagem por nota).
- **Resposta de exemplo:**
```json
{
  "total_books": 10,
  "avg_price": 12.34,
  "rating_distribution": {"1": 1, "2": 2, "3": 0, "4": 3, "5": 4, "unknown": 0}
}
```

### Categories (Estatísticas por categoria)
- **Endpoint:** `GET /api/v1/stats/categories`
- **Descrição:** Retorna estatísticas paginadas por categoria: quantidade de livros, preço mínimo, máximo e preço médio por categoria.
- **Parâmetros:**
  - `page` (query, integer, opcional, padrão: 1)
  - `per_page` (query, integer, opcional, padrão: 10)
- **Resposta de exemplo:**
```json
{
  "items": [
    {"name": "Ficcao", "book_count": 2, "min_price": 10.0, "max_price": 20.0, "avg_price": 15.0},
    {"name": "Ciencia", "book_count": 1, "min_price": 5.0, "max_price": 5.0, "avg_price": 5.0}
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 2,
    "total_pages": 1
  }
}
```

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

### Criar ou executar predições de Machine Learning
- **Endpoint:** `POST /api/v1/ml/predictions`
- **Descrição:** Cria uma nova predição ou executa o modelo de ML para gerar uma predição automaticamente. Este endpoint tem dois comportamentos distintos baseados nos parâmetros fornecidos.
- **Disponibilidade:** Este endpoint está disponível em ambos os ambientes Docker (desenvolvimento e produção). Ambos os containers montam o volume `./models` e carregam os modelos ML na inicialização.
- **Documentação completa:** Ver `docs/ml_implementation.md` para detalhes completos sobre treinamento, cache, e troubleshooting.

#### Modo 1: Executar ML em Tempo Real
Endpoint executa o modelo ML e salva o resultado automaticamente no banco de dados.

- **Request:**
```json
{
  "book_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "prediction_type": "rating"
}
```

- **Query Parameters:**
  - `use_cache` (opcional, boolean, default: true): Se deve usar cache de predições

- **Response (200 OK):**
```json
{
  "prediction": {
    "book_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "book_title": "The Great Gatsby",
    "predicted_value": "1",
    "predicted_label": "High Rating (>=4)",
    "confidence": 0.85,
    "features_used": {
      "price": 29.99,
      "category": "Fiction",
      "availability": "In stock",
      "category_encoded": 0,
      "availability_encoded": 1
    },
    "model_version": "v1.0.0",
    "from_cache": false
  },
  "saved_prediction_id": "uuid-da-predicao-salva"
}
```

#### Modo 2: Salvar Predição Pré-calculada
Endpoint apenas salva uma predição que foi calculada externamente.

- **Request:**
```json
{
  "book_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "prediction_type": "rating",
  "predicted_value": "5",
  "confidence": 0.95,
  "model_version": "v1.0.0",
  "metadata": {
    "source": "external_model",
    "algorithm": "custom"
  }
}
```

- **Response (201 Created):**
```json
{
  "id": "prediction-uuid",
  "book_id": "book-uuid",
  "prediction_type": "rating",
  "predicted_value": "5",
  "confidence": 0.95,
  "model_version": "v1.0.0",
  "metadata": {
    "source": "external_model",
    "algorithm": "custom"
  },
  "created_at": "2025-10-30T12:00:00Z"
}
```

#### Tipos de Predição Válidos
- `rating` - Predição de rating alto/baixo (>=4 ou <4)
- `category` - Predição de categoria
- `price` - Predição de preço
- `recommendation` - Predição de recomendação

#### Erros Possíveis

**400 Bad Request - Validação:**
```json
{
  "error": "Invalid parameters",
  "details": [
    {
      "field": "book_id",
      "message": "Input should be a valid string",
      "type": "string_type"
    }
  ]
}
```

**404 Not Found - Livro inexistente:**
```json
{
  "error": "Book not found",
  "message": "Book with id xxx not found"
}
```

**503 Service Unavailable - Modelo não carregado:**
```json
{
  "error": "Model not available",
  "message": "Model for 'rating' is not loaded. Please train the model first.",
  "hint": "Run: python ml_training/train_model.py"
}
```

#### Observações
- **Ambientes:** Endpoint disponível em ambos os containers Docker (fiap-backend-dev e fiap-backend-prod)
- **Volume compartilhado:** Ambos os containers montam `./models:/app/models` do host, compartilhando modelos treinados
- **Treinamento automático:** Modelo é treinado automaticamente na primeira inicialização se não existir
- **Cache:** Predições são cacheadas automaticamente para melhor performance
- **Validação:** `confidence` deve estar entre 0.0 e 1.0
- **Validação:** `model_version` é obrigatório quando `predicted_value` é fornecido
- **Persistência:** Todas as predições (executadas ou salvas) são armazenadas na tabela `predictions`
- **Documentação técnica:** Ver `docs/ml_implementation.md` para detalhes sobre arquitetura, treinamento e troubleshooting

---

## 7. Documentação Swagger

### Acessar documentação interativa da API
- **Endpoint:** `GET /apidocs/`
- **Descrição:** Exibe a documentação automática dos endpoints da API, gerada via Swagger/Flasgger. Permite testar e visualizar exemplos de requisições e respostas.
- **Resposta:** Interface web interativa.

---

## Respostas de Erro

A API possui tratamento centralizado de erros que retorna respostas padronizadas:

### Erro de Validação (400)
Retornado quando parâmetros inválidos são fornecidos (ex: paginação fora dos limites).
```json
{
  "error": "Invalid parameters",
  "details": [
    {
      "type": "value_error",
      "loc": ["page"],
      "msg": "Value must be greater than or equal to 1"
    }
  ]
}
```

### Erro de Valor (400)
Retornado quando um valor inválido é fornecido (ex: UUID mal formatado).
```json
{
  "error": "Invalid value",
  "message": "badly formed hexadecimal UUID string"
}
```

### Erro Interno do Servidor (500)
Retornado quando ocorre um erro inesperado no servidor.
```json
{
  "error": "Internal server error",
  "message": "Descrição do erro"
}
```

---

## Observações
- Todos os endpoints retornam respostas no formato JSON, exceto `/apidocs/`, que retorna uma interface web.
- IDs são UUIDs (ex: `550e8400-e29b-41d4-a716-446655440000`).
- Parâmetros de busca devem ser passados via query string.
- **Paginação:** Todos os endpoints paginados validam `page >= 1` e `per_page` entre 1 e 100.
- **Consistência:** Todos os endpoints paginados usam a chave `items` (não `results`) para a lista de resultados.
- Endpoints de autenticação e ML são opcionais/bônus.
- Para mais detalhes sobre a arquitetura e funcionamento, consulte o arquivo `docs/architecture.md`.
