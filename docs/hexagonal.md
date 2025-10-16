## Arquitetura Hexagonal - Camadas

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (Driving Adapter)          │
│              books_endpoints.py (Flask Endpoint)        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                      │
│              GetBookController                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Use Case Layer                        │
│                GetBookUseCase                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Domain Layer (Core)                   │
│        Service: BookService                             │
│        Port: IBookRepository (Protocol)                 │
│        Model: Book (Domain Model)                       │
│        Enum: UserRole (Domain Enum)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────────────────┐
│            Infrastructure Layer (Driven Adapter)              │
│   Adapter: BookAdapter → Repository: BookRepository           │
│   ORM Models: Book, Category, User (SQLAlchemy)              │
└───────────────────────────────────────────────────────────────┘

```

### ✅ Separação de Responsabilidades

- Endpoint: Recebe requisição HTTP
- Controller: Orquestra o fluxo
- Use Case: Executa lógica de aplicação
- Service: Contém regras de negócio
- Repository: Faz acesso a dados

### ✅ Testabilidade

- É possível mockar qualquer dependência
- O domínio pode ser testado sem banco nem Flask

### ✅ Flexibilidade

- Fácil trocar implementações (ex: mudar de SQLAlchemy para outro ORM)
