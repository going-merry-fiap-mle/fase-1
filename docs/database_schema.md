# Documentação do Banco de Dados

Este documento descreve o modelo de dados utilizado pela API de Livros, incluindo tabelas, campos, tipos e relacionamentos.

---

## books
- **id**: UUID (PK)
- **title**: string
- **price**: decimal(10,2)
- **rating**: integer (1-5)
- **availability**: string
- **category_id**: UUID (FK para categories.id)
- **image_url**: string
- **created_at**: datetime
- **updated_at**: datetime

## categories
- **id**: UUID (PK)
- **name**: string (único)

## users *(opcional, para autenticação)*
- **id**: UUID (PK)
- **username**: string (único)
- **password_hash**: string
- **role**: string (admin, user)
- **created_at**: datetime

---

### Observações
- Todos os IDs são do tipo UUID (ex: `550e8400-e29b-41d4-a716-446655440000`).
- As tabelas opcionais são recomendadas para desafios de autenticação e monitoramento.
- Relacionamento: `books.category_id` referencia `categories.id`.
- Datas em UTC.

