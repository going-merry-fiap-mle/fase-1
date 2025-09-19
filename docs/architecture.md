# Arquitetura Hexagonal do Projeto

Este projeto segue o padrão de arquitetura hexagonal (Ports & Adapters), visando separação clara de responsabilidades, facilidade de testes, manutenção e escalabilidade.

## Estrutura de Pastas

```
api/
  main.py
  controllers/
  schemas/
application/
domain/
infrastructure/
data/
docs/
scripts/
tests/
```

## Descrição dos Diretórios

### api/
Interface de entrada do sistema. Responsável por expor a API HTTP (Flask) e definir os endpoints.
- **main.py**: Inicialização da aplicação Flask e registro dos blueprints.
- **controllers/**: Implementação das rotas/endpoints da API. Cada recurso (livros, categorias, health) possui seu próprio arquivo.
- **schemas/**: Schemas para validação e serialização dos dados de entrada/saída dos endpoints.

### application/
Camada de orquestração dos casos de uso do sistema. Aqui ficam as regras de negócio que coordenam as ações entre domínio e infraestrutura.
- **use_cases.py**: Implementação dos casos de uso (ex: listar livros, buscar por categoria, etc).

### domain/
Camada de domínio, onde reside o núcleo da lógica de negócio.
- **models.py**: Definição das entidades principais (Livro, Categoria, etc).
- **services.py**: Serviços de negócio que operam sobre as entidades.
- **repositories.py**: Interfaces para persistência e recuperação dos dados do domínio.

### infrastructure/
Implementações técnicas e adaptação para o mundo externo.
- **database.py**: Implementação da persistência de dados (ex: leitura/escrita em CSV ou banco de dados).
- **scraper.py**: Lógica de web scraping para extração dos dados dos livros.
- **adapters/**: Adapters para conectar interfaces do domínio com implementações concretas (ex: repositórios, APIs externas).

### data/
Armazenamento dos dados extraídos (ex: arquivos CSV).

### docs/
Documentação do projeto, incluindo arquitetura, instruções e diagramas.
- **architecture.md**: Este documento, explicando a arquitetura hexagonal e a função de cada diretório.

### scripts/
Scripts utilitários, como o scraper executável.

### tests/
Testes automatizados do projeto.
- **test_api.py**: Testes dos endpoints da API.

## Fluxo de Dados
1. **Usuário** faz requisição HTTP para a API (camada api/controllers).
2. O controller chama um **caso de uso** na camada application.
3. O caso de uso orquestra as operações, utilizando entidades e serviços do **domínio**.
4. Para persistência ou integração externa, o domínio utiliza interfaces de **repositório**, que são implementadas na **infraestrutura**.
5. Dados são retornados ao usuário via API, utilizando os **schemas** para validação/serialização.

## Vantagens da Arquitetura
- Separação clara entre regras de negócio e detalhes técnicos.
- Facilidade para testar o núcleo do sistema sem dependências externas.
- Flexibilidade para trocar implementações (ex: trocar CSV por banco de dados) sem afetar o domínio.
- Organização modular, facilitando manutenção e evolução.

---

Para dúvidas ou sugestões sobre a arquitetura, consulte este documento ou entre em contato com os mantenedores do projeto.

