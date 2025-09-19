# Documentação dos Endpoints da API

Esta documentação descreve os endpoints REST disponíveis na API do projeto, conforme implementado até o momento.

---

## 1. Livros

### Listar todos os livros
- **Endpoint:** `GET /api/v1/books`
- **Descrição:** Retorna uma lista de livros disponíveis.
- **Resposta de exemplo:**
```json
{
  "books": []
}
```

### Buscar livro por ID
- **Endpoint:** `GET /api/v1/books/<int:book_id>`
- **Descrição:** Retorna os detalhes de um livro específico pelo seu ID.
- **Resposta de exemplo:**
```json
{
  "id": 1,
  "book": null
}
```

### Buscar livros por título e/ou categoria
- **Endpoint:** `GET /api/v1/books/search?title={title}&category={category}`
- **Descrição:** Busca livros pelo título e/ou categoria informados.
- **Resposta de exemplo:**
```json
{
  "results": []
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
  "categories": []
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

## 4. Documentação Swagger

### Acessar documentação interativa da API
- **Endpoint:** `GET /apidocs/`
- **Descrição:** Exibe a documentação automática dos endpoints da API, gerada via Swagger/Flasgger. Permite testar e visualizar exemplos de requisições e respostas.
- **Resposta:** Interface web interativa.

---

## Observações
- Todos os endpoints retornam respostas no formato JSON, exceto `/apidocs/`, que retorna uma interface web.
- Os endpoints de livros e categorias ainda retornam listas vazias ou valores nulos, pois a lógica de persistência e busca será implementada nas próximas etapas.
- Parâmetros de busca (title, category) devem ser passados via query string em `/api/v1/books/search`.
- Para mais detalhes sobre a arquitetura e funcionamento, consulte o arquivo `docs/architecture.md`.
