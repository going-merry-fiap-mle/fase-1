# Arquitetura do Projeto (Hexagonal / Ports & Adapters)

Este projeto segue princípios da Arquitetura Hexagonal (Ports & Adapters), promovendo separação clara de responsabilidades, testabilidade, manutenção e evolução incremental. Abaixo está a visão atualizada e fiel ao código do repositório.

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
  - Define modelos, serviços e contratos (ports) independentes de tecnologia. Atualmente contém módulos base como placeholders para evolução (models.py, services.py, repositories.py).
  - Objetivo: concentrar regras de negócio e interfaces (p. ex., repositórios ou portas de scraping) que podem ser implementadas pela infraestrutura.

- Infraestrutura (Adapters)
  - Onde fica: app/infrastructure
  - Implementa detalhes técnicos e integrações externas de acordo com as portas definidas (explícitas ou implícitas) pelo domínio/aplicação.
  - Exemplo: WebDriverInfrastructure (app/infrastructure/webdriver_infrastructure.py) encapsula Selenium/Firefox e a configuração do driver. database.py é um stub para futura persistência. adapters/ reservado para implementações adicionais.

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
    - register_endpoints.py
  - controller/
    - scraping_controller.py
  - domain/
    - models.py (placeholder)
    - repositories.py (placeholder)
    - services.py (placeholder)
  - infrastructure/
    - webdriver_infrastructure.py
    - database.py (stub)
    - adapters/ (.keep)
  - schemas/
    - book_schema.py
    - category_schema.py (vazio no momento)
    - scraping_schema.py
  - services/
    - scraper_service.py
  - usecases/
    - scraping_use_case.py
  - utils/
    - environment_loader.py
    - logger.py
- docs/
  - api_endpoints.md
  - architecture.md (este documento)
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

Este fluxo exemplifica Ports & Adapters: a lógica de aplicação/uso usa uma “porta” para navegação/extração; a implementação concreta é o adapter Selenium na infraestrutura. Trocar Selenium ou a forma de captura exigiria apenas substituir o adapter, mantendo o contrato.

## Ports & Adapters (mapeamento prático)

- Portas (contratos/intenções)
  - Contratos de repositório e serviços de domínio em app/domain (a serem detalhados conforme a evolução).
  - Contratos de dados com Pydantic (app/schemas).

- Adapters (implementações técnicas)
  - WebDriverInfrastructure: integração com navegador via Selenium/GeckoDriverManager, headless fora de dev.
  - Futuro: implementações de persistência em database.py ou pasta adapters/ (por exemplo, banco relacional, NoSQL, CSV, etc.).

- Orquestração
  - Controllers e UseCases compõem e consomem portas; a camada de Interface apenas inicia o fluxo e serializa resultados.

## Decisões e Convenções

- Logs centralizados por LogManager e AppLogger, com formatação consistente e níveis configuráveis via LOG_LEVEL.
- Variáveis de ambiente carregadas por EnvironmentLoader (ex.: HOST, PORT, DEBUG, FLASK_ENV). Em FLASK_ENV ≠ dev, o WebDriver roda em modo headless.
- Swagger/Flasgger para documentação dos endpoints.
- Pydantic como contrato de dados entre camadas e para a API.
- Injeção de dependências manual no Controller para simplicidade; pode ser evoluída para um contêiner de IoC se necessário.

## Pontos de Evolução

- Domínio: promover os placeholders (models/repositories/services) a contratos explícitos (interfaces/protocolos) e mover regras de negócio específicas para o núcleo do domínio.
- Persistência: implementar repositórios concretos em infrastructure/database.py (ou adapters/) e fazer a aplicação usar apenas portas do domínio.
- Endpoints de Books/Categories: integrar com casos de uso e repositórios reais (hoje retornam dados vazios como placeholder).
- Testes: consolidar estrutura e ampliar cobertura em torno de contratos do domínio e adapters.

## Dependências Principais

- Flask, flasgger (API e documentação)
- selenium, webdriver-manager (extração via navegador)
- pydantic (modelagem/validação)
- python-dotenv (variáveis de ambiente)

## Resumo

A arquitetura atual já separa interface, orquestração (controller/use case), serviços de aplicação e infraestrutura. O domínio está preparado para receber contratos e regras mais ricas. O uso de Ports & Adapters permite trocar componentes técnicos (ex.: driver de scraping, persistência) sem impactar o núcleo do sistema, assegurando testabilidade e evolução controlada.