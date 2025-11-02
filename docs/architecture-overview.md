# Arquitetura do Projeto (Hexagonal / Ports & Adapters)

Este projeto segue princípios da Arquitetura Hexagonal (Ports & Adapters), promovendo separação clara de responsabilidades, testabilidade, manutenção e evolução incremental. Abaixo está a visão atualizada e fiel ao código do repositório.

## Índice

1. [Visão Geral das Camadas](#visão-geral-das-camadas)
2. [Mapa de Diretórios](#mapa-de-diretórios-resumo)
3. [Fluxo de Requisição - Web Scraping](#fluxo-de-requisição-ex-web-scraping)
4. [Fluxo de Requisição - Predição ML](#fluxo-de-requisição-ex-predição-ml)
5. [Ports & Adapters - Mapeamento Prático](#ports--adapters-mapeamento-prático)
6. [Decisões e Convenções](#decisões-e-convenções)
7. [Melhorias Implementadas](#melhorias-implementadas)
8. [Dependências Principais](#dependências-principais)
9. [Resumo](#resumo)

---

## Visão Geral das Camadas

- Interface/Entrega (API HTTP)
  - Framework: Flask, documentação com Flasgger/Swagger.
  - Onde fica: app/api
  - Como expõe: Blueprints em app/api/endpoints/v1 e registro central em app/api/register_endpoints.py
  - Entrada da aplicação: app/main.py (classe FlaskApp configura logs, variáveis de ambiente, Swagger e registra endpoints).

- Aplicação (Casos de Uso)
  - Onde fica: app/usecases
  - Responsável por orquestrar ações do domínio/serviços e coordenar o fluxo de dados.
  - Exemplo: ScrapingUseCase (app/usecases/scraping_use_case.py)

- Serviços de Aplicação
  - Onde fica: app/services
  - Implementam lógica de aplicação que interage com portas/adapters (infra) para realizar tarefas.
  - Exemplo: ScraperService (app/services/scraper_service.py) que usa Selenium via um adapter de infraestrutura.

- Domínio (Núcleo de Regras)
  - Onde fica: app/domain
  - Define modelos de domínio puros independentes de tecnologia (Book, Category, Prediction, User, Health).
  - Modelos de domínio não possuem dependências de frameworks ou infraestrutura (sem SQLAlchemy, sem Flask).
  - Objetivo: concentrar regras de negócio puras que podem ser utilizadas por qualquer camada superior.

- Infraestrutura (Adapters)
  - Onde fica: app/infrastructure
  - Implementa detalhes técnicos e integrações externas de acordo com as portas definidas pelo domínio/aplicação.
  - Componentes: WebDriverInfrastructure (Selenium/Firefox), database.py (configuração SQLAlchemy), session_manager.py (gestão de transações).
  - Subpastas: adapters/ (BookAdapter, CategoryAdapter, PredictionAdapter), repository/ (implementações concretas dos repositórios), models/ (modelos SQLAlchemy ORM).

- Esquemas (DTOs/Contratos de Dados)
  - Onde fica: app/schemas
  - Modelos Pydantic para padronizar entrada/saída entre camadas e a API.
  - Exemplos: ScrapingBase, BookBase.

- Controller (Composição/Orquestração)
  - Onde fica: app/controller
  - Responsável por compor dependências (injeção manual) e acionar casos de uso a partir da camada de interface.
  - Exemplo: ScrapingController instancia WebDriverInfrastructure → ScraperService → ScrapingUseCase e executa o fluxo.

- Utilidades
  - Onde fica: app/utils
  - Auxiliares como carregamento de variáveis de ambiente e infraestrutura de logs (EnvironmentLoader, AppLogger/LogManager).

- Testes
  - Onde fica: app/tests e app/unittest
  - Testes organizados por área (API, controller, infrastructure, services, usecases e utils).

## Mapa de Diretórios (resumo)

- app/
  - main.py
  - api/
    - endpoints/v1/
      - books_endpoints.py
      - categories_endpoints.py
      - health_endpoints.py
      - scraper_endpoints.py
      - stats_endpoints.py
      - ml_endpoints.py
    - register_endpoints.py
  - controller/
    - books/ (get_book_controller.py, create_book_controller.py, etc.)
    - categories/ (get_categories_controller.py)
    - health/ (health_controller.py)
    - ml/ (create_prediction_controller.py, execute_prediction_controller.py)
    - scraping_controller.py
  - domain/
    - models/
      - book.py
      - category.py
      - prediction_domain_model.py
  - infrastructure/
    - webdriver_infrastructure.py
    - database.py
    - session_manager.py
    - adapters/
      - book_adapter.py
      - category_adapter.py
      - prediction_adapter.py
    - repository/
      - book_repository.py
      - category_repository.py
      - prediction_repository.py
    - models/ (SQLAlchemy ORM)
      - book.py
      - category.py
      - user.py
      - prediction.py
  - ml/
    - model_loader.py (Singleton para carregar modelos)
    - __init__.py
  - port/
    - book_port.py (IBookRepository)
    - category_port.py (ICategoryRepository)
    - prediction_port.py (IPredictionRepository)
  - schemas/
    - book_schema.py
    - category_schema.py
    - scraping_schema.py
    - ml_schema.py (PredictionBase, MLPredictionResponse, MLExecutionResponse)
    - pagination_schema.py
  - services/
    - book_service.py
    - category_service.py
    - scraper_service.py
    - ml_model_service.py
    - prediction_service.py
  - usecases/
    - books/ (get_book_use_case.py, create_book_use_case.py, etc.)
    - categories/ (get_categories_use_case.py)
    - ml/ (create_prediction_use_case.py, execute_prediction_use_case.py)
    - scraping_use_case.py
  - utils/
    - environment_loader.py
    - logger.py
    - task_manager.py
- docs/
  - api-reference.md
  - architecture-overview.md (este documento)
  - architecture-diagrams.md
  - database-schema.md
  - deployment.md
  - machine-learning.md
- ml_training/
  - train_model.py (script de treinamento)
- models/
  - rating_classifier_v1.pkl (modelo treinado)
  - encoders_v1.pkl (encoders)
  - metadata_v1.pkl (metadata)
- tests e unittest

## Fluxo de Requisição (ex.: Web Scraping)

1. Cliente faz GET /api/v1/scraping (app/api/endpoints/v1/scraper_endpoints.py).
2. Endpoint instancia ScrapingController e chama call_controller().
3. ScrapingController compõe dependências:
   - WebDriverInfrastructure (adapter Selenium/Firefox)
   - ScraperService (usa o WebDriverInfrastructure para extrair dados)
   - ScrapingUseCase (orquestra a execução do serviço)
4. ScraperService navega nas páginas, extrai e transforma os dados em modelos Pydantic (ScrapingBase).
5. Use case retorna a lista de ScrapingBase; o endpoint serializa com model_dump() e responde via jsonify.

Este fluxo exemplifica Ports & Adapters: a lógica de aplicação/uso usa uma "porta" para navegação/extração; a implementação concreta é o adapter Selenium na infraestrutura. Trocar Selenium ou a forma de captura exigiria apenas substituir o adapter, mantendo o contrato.

## Fluxo de Requisição (ex.: Predição ML)

1. Cliente faz POST /api/v1/ml/predictions com `{"book_id": "uuid", "prediction_type": "rating"}` (app/api/endpoints/v1/ml_endpoints.py).
2. Endpoint valida request com Pydantic (PredictionBase) e instancia ExecutePredictionController.
3. ExecutePredictionController compõe dependências:
   - MLModelService (executa predição usando modelo carregado)
   - PredictionService (persiste resultado via IPredictionRepository)
   - ExecutePredictionUseCase (orquestra o fluxo completo)
4. Use case executa:
   - MLModelService.predict(): busca livro no banco, prepara features, executa modelo ML via MLModelLoader (Singleton)
   - PredictionService.create_prediction(): salva resultado via PredictionAdapter → PredictionRepository → PostgreSQL
5. Use case retorna (ml_result, saved_prediction).
6. Controller transforma em MLExecutionResponse com detalhes da predição (book_title, confidence, features_used, from_cache).
7. Endpoint serializa com model_dump() e responde via jsonify com status 200.

**Arquitetura Hexagonal em Ação:**
- **Port:** IPredictionRepository (Protocol) define contrato de persistência
- **Adapter:** PredictionAdapter implementa o Protocol e delega para PredictionRepository
- **Domain:** Prediction (modelo de domínio puro, sem SQLAlchemy)
- **Infrastructure:** Prediction (modelo SQLAlchemy) com métodos to_domain()/from_domain()
- **Service:** MLModelService encapsula lógica de ML, PredictionService usa a Port
- **Singleton:** MLModelLoader carrega modelos uma única vez e mantém cache de predições

## Ports & Adapters (mapeamento prático)

- **Portas (contratos/intenções)**
  - `IBookRepository` (Protocol): contrato para operações com livros
  - `ICategoryRepository` (Protocol): contrato para operações com categorias
  - `IPredictionRepository` (Protocol): contrato para operações com predições
  - Contratos de dados com Pydantic (app/schemas): BookBase, CategoryBase, PredictionBase, MLPredictionResponse

- **Adapters (implementações técnicas)**
  - `BookAdapter`: implementa IBookRepository e delega para BookRepository
  - `CategoryAdapter`: implementa ICategoryRepository e delega para CategoryRepository
  - `PredictionAdapter`: implementa IPredictionRepository e delega para PredictionRepository
  - `WebDriverInfrastructure`: integração com navegador via Selenium/GeckoDriverManager, headless fora de dev
  - `MLModelLoader` (Singleton): carrega modelos ML via joblib e mantém cache em memória

- **Orquestração**
  - Controllers compõem dependências (Adapters, Services, UseCases)
  - UseCases orquestram Services e coordenam fluxo de dados
  - Services contêm lógica de negócio e usam Ports (abstrações)
  - Camada de Interface (API) apenas valida, instancia Controller e serializa resultados

## Decisões e Convenções

- Logs centralizados por LogManager e AppLogger, com formatação consistente e níveis configuráveis via LOG_LEVEL.
- Variáveis de ambiente carregadas por EnvironmentLoader (ex.: HOST, PORT, DEBUG, FLASK_ENV). Em FLASK_ENV ≠ dev, o WebDriver roda em modo headless.
- Swagger/Flasgger para documentação dos endpoints.
- Pydantic como contrato de dados entre camadas e para a API.
- Injeção de dependências manual no Controller para simplicidade; pode ser evoluída para um contêiner de IoC se necessário.
- **Tratamento Centralizado de Erros**: Implementado em `app/main.py` via `@app.errorhandler()` para:
  - `ValidationError` (Pydantic): retorna 400 com detalhes de validação
  - `ValueError`: retorna 400 com mensagem de erro (ex: UUID inválido)
  - `Exception` (genérico): retorna 500 com mensagem de erro interno
  - Endpoints não precisam de try/except, os erros são tratados centralmente

## Melhorias Implementadas

- **Arquitetura Hexagonal Completa**: Implementação de Books e Categories seguindo Ports & Adapters
  - Domain Models: modelos de domínio puros sem dependências de infraestrutura
  - Ports (Protocols): IBookRepository, ICategoryRepository, IScrapingRepository
  - Adapters: BookAdapter, CategoryAdapter → BookRepository, CategoryRepository
  - Use Cases: GetBookUseCase, CreateBookUseCase, GetCategoriesUseCase
  - Controllers: GetBookController, CreateBookController, GetCategoriesController

- **Correção de Import Circular**: UserRole movido de infrastructure para domain, eliminando dependência circular

- **Tipagem Python 3.12+**:
  - Uso de tipagem nativa (`list[T]`, `dict[K,V]`, `X | Y`) em vez de `typing.List`, `typing.Dict`, `typing.Union`
  - Protocol para interfaces sem herança
  - Generator de `collections.abc` em vez de `typing.Generator`
  - Self de `typing` para métodos que retornam instância da própria classe

- **Validação com Pydantic**:
  - PaginationParams com Field validation (ge=1, le=100)
  - PaginationMeta com @computed_field para total_pages
  - Remoção de validações manuais if/else

- **Gestão de Sessão SQLAlchemy**:
  - Context manager `session_scope()` para gerenciamento automático de transações
  - Uso de `session.flush()` em vez de commits manuais
  - Rollback automático em caso de exceções

- **Remoção de Código Legado**: arquivo models.py com modelos SQLAlchemy no domain removido

## Dependências Principais

- Flask, flasgger (API e documentação)
- selenium, webdriver-manager (extração via navegador)
- pydantic (modelagem/validação)
- python-dotenv (variáveis de ambiente)
- SQLAlchemy (ORM para PostgreSQL)
- alembic (migrations de banco de dados)
- scikit-learn, joblib, numpy (Machine Learning)
- psycopg2-binary (driver PostgreSQL)

## Resumo

A arquitetura atual implementa completamente os princípios de Clean Architecture e Hexagonal Architecture:
- **Separação total de responsabilidades**: Interface (API) → Controllers → Use Cases → Services → Ports → Adapters → Infrastructure
- **Domínio puro**: Modelos de domínio sem dependências externas (Book, Category, Prediction, User, Health)
- **Ports implementados**: IBookRepository, ICategoryRepository, IPredictionRepository com Protocol typing
- **Adapters implementados**: BookAdapter, CategoryAdapter, PredictionAdapter delegando para repositories concretos
- **Inversão de dependências**: Services dependem de abstrações (Ports), não de implementações concretas
- **Testabilidade**: 180 testes unitários cobrindo todas as camadas
- **Production-ready**: Todos os endpoints obrigatórios, opcionais e bônus implementados com autenticação JWT, Machine Learning e pipeline completo de dados

O uso de Ports & Adapters permite trocar componentes técnicos (ex.: driver de scraping, banco de dados, framework ML) sem impactar o núcleo do sistema, assegurando testabilidade, manutenibilidade e evolução controlada.