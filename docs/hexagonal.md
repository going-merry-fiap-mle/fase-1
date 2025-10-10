## Arquitetura Hexagonal - Camadas

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (Driving Adapter)          │
│              books_route.py (Flask Endpoint)            │
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
│        Port: IBookRepository                            │
│        Model: Book                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────────────────┐
│            Infrastructure Layer (Driven Adapter)              │
│   Adapter: BookRepositoryAdapter → Repository: BookRepository │
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
