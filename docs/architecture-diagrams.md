# Diagramas de Arquitetura - Tech Challenge Fase 1

Este documento contém os diagramas visuais da arquitetura completa do sistema, conforme solicitado pelo Tech Challenge.

---

## Índice

1. [Arquitetura Geral do Sistema (Clean/Hexagonal)](#1-arquitetura-geral-do-sistema-cleanhexagonal)
2. [Pipeline Completo de Dados](#2-pipeline-completo-de-dados)
3. [Integração Machine Learning](#3-integração-machine-learning)
4. [Arquitetura de Escalabilidade Futura](#4-arquitetura-de-escalabilidade-futura)
5. [Fluxo de Dados para Data Scientists](#5-fluxo-de-dados-para-data-scientists)
6. [Fluxo de Dados para ML Engineers](#6-fluxo-de-dados-para-ml-engineers)

---

## 1. Arquitetura Geral do Sistema (Clean/Hexagonal)

```mermaid
graph TB
    subgraph "Camada Externa"
        API[API REST<br/>Flask/Flasgger]
        CLI[Scripts CLI<br/>Scraping]
    end

    subgraph "Camada de Controladores"
        BookCtrl[Controladores de Livros]
        MLCtrl[Controladores ML]
        AuthCtrl[Controladores Auth]
        ScrapingCtrl[Controlador Scraping]
    end

    subgraph "Camada de Casos de Uso - Lógica de Negócio"
        BookUC[Casos de Uso de Livros]
        MLUC[Casos de Uso ML<br/>Criar/Executar Predições]
        ScrapingUC[Caso de Uso Scraping]
    end

    subgraph "Camada de Serviços - Serviços de Domínio"
        MLService[Serviço ML<br/>Engenharia de Features]
        MLModelService[Serviço de Modelo ML<br/>Treinamento/Predição]
        ScrapingService[Serviço de Scraping]
        PredictionService[Serviço de Predição]
    end

    subgraph "Portas - Interfaces"
        BookPort[Porta Repositório Livros]
        PredictionPort[Porta Predição]
        CategoryPort[Porta Categoria]
    end

    subgraph "Adaptadores - Infraestrutura"
        BookRepo[Repositório de Livros]
        PredictionRepo[Repositório de Predições]
        BookAdapter[Adaptador de Livros]
        PredictionAdapter[Adaptador de Predições]
    end

    subgraph "Infraestrutura"
        DB[(PostgreSQL<br/>Database)]
        ModelFiles[Arquivos de Modelo<br/>.pkl]
        WebDriver[Selenium<br/>WebDriver]
    end

    API --> BookCtrl
    API --> MLCtrl
    API --> AuthCtrl
    CLI --> ScrapingCtrl

    BookCtrl --> BookUC
    MLCtrl --> MLUC
    ScrapingCtrl --> ScrapingUC

    BookUC --> BookPort
    MLUC --> MLService
    MLUC --> MLModelService
    MLUC --> PredictionService
    ScrapingUC --> ScrapingService

    MLService --> BookAdapter
    MLModelService --> ModelFiles
    PredictionService --> PredictionPort

    BookPort --> BookRepo
    PredictionPort --> PredictionRepo
    BookAdapter --> BookRepo
    PredictionAdapter --> PredictionRepo

    BookRepo --> DB
    PredictionRepo --> DB
    ScrapingService --> WebDriver
    ScrapingService --> BookRepo
```

**Camadas da Arquitetura:**
- **Camada Externa:** Pontos de entrada (REST API, CLI)
- **Controladores:** Recebem requisições e orquestram casos de uso
- **Casos de Uso:** Lógica de negócio pura (independente de framework)
- **Serviços:** Serviços de domínio especializados (ML, Scraping)
- **Portas:** Interfaces que definem contratos
- **Adaptadores:** Implementações concretas das portas
- **Infraestrutura:** Persistência e recursos externos

---

## 2. Pipeline Completo de Dados

```mermaid
graph LR
    subgraph "INGESTÃO"
        WebSite[books.toscrape.com<br/>Website]
        Selenium[Selenium WebDriver<br/>Navegador Automatizado]
        Scraper[Serviço de Scraping<br/>Extração e Transformação]
    end

    subgraph "ARMAZENAMENTO"
        CSV[CSV Local<br/>data/books.csv]
        PostgreSQL[(PostgreSQL<br/>Database)]
        Tables[Tabelas:<br/>books, categories<br/>users, predictions]
    end

    subgraph "PROCESSAMENTO"
        FeatureEng[Engenharia de Features<br/>Serviço ML]
        Transform[Transformações:<br/>- price para float<br/>- availability para binário<br/>- category para codificado]
    end

    subgraph "MACHINE LEARNING"
        Training[Treinamento de Modelo<br/>Random Forest]
        ModelFile[rating_classifier_v1.0.0.pkl]
        Prediction[Serviço de Predição<br/>Inferência em Tempo Real]
    end

    subgraph "API PÚBLICA"
        RestAPI[REST API<br/>Flask + Swagger]
        Endpoints[Endpoints:<br/>/books<br/>/ml/features<br/>/ml/predictions]
    end

    subgraph "CONSUMO"
        DataScientist[Data Scientist<br/>Dados de Treinamento]
        MLEngineer[ML Engineer<br/>Predições]
        Apps[Apps Externos<br/>Recomendações de Livros]
    end

    WebSite -->|Requisições HTTP| Selenium
    Selenium -->|Parse HTML| Scraper
    Scraper -->|Escrever| CSV
    Scraper -->|Inserir| PostgreSQL
    PostgreSQL --> Tables

    Tables -->|Ler Livros| FeatureEng
    FeatureEng -->|Transformar| Transform
    Transform -->|Dataset| Training
    Training -->|Salvar Modelo| ModelFile

    Tables -->|Dados de Livros| RestAPI
    ModelFile -->|Carregar Modelo| Prediction
    Prediction -->|Inferência| RestAPI
    RestAPI --> Endpoints

    Endpoints -->|GET /ml/training-data| DataScientist
    Endpoints -->|POST /ml/predictions| MLEngineer
    Endpoints -->|GET /books| Apps
```

**Fluxo Completo:**
1. **Scraping:** Selenium navega no site, extrai dados, salva em CSV e PostgreSQL
2. **Engenharia de Features:** Transforma dados brutos em features para ML
3. **Treinamento:** Treina modelo Random Forest, salva arquivo .pkl
4. **API:** Expõe dados via endpoints REST
5. **Consumo:** Data Scientists, ML Engineers e Apps consomem a API

---

## 3. Integração Machine Learning

```mermaid
graph TB
    subgraph "Fontes de Dados"
        Books[(Tabela Books<br/>2000+ registros)]
    end

    subgraph "Engenharia de Features"
        MLService[Serviço ML]
        Features[Features Extraídas:<br/>price_num: float<br/>rating: int<br/>availability_flag: 0/1<br/>category: string<br/>image_present: 0/1]
    end

    subgraph "Pipeline de Treinamento"
        TrainScript[ml_training/train_model.py]
        Preprocessing[Pré-processamento:<br/>1. Codificar categorias<br/>2. Codificar disponibilidade<br/>3. Tratar valores ausentes]
        Model[Random Forest<br/>Classifier]
        Evaluation[Avaliação:<br/>Accuracy, Precision<br/>Recall, F1-Score]
    end

    subgraph "Persistência do Modelo"
        PKL[rating_classifier_v1.0.0.pkl<br/>Salvo com joblib]
        Metadata[Metadados do Modelo:<br/>versão, features<br/>accuracy, timestamp]
    end

    subgraph "API de Inferência"
        LoadModel[Carregador de Modelo<br/>Carrega .pkl no startup]
        PredictionEndpoint[POST /api/v1/ml/predictions]
        Cache[Cache de Predições<br/>Em memória]
        SaveDB[(tabela predictions)]
    end

    subgraph "Endpoints ML Prontos"
        EP1[GET /ml/features<br/>Features paginadas]
        EP2[GET /ml/manifest<br/>Schema de features]
        EP3[GET /ml/training-data<br/>Exportação JSON ou CSV]
        EP4[POST /ml/predictions<br/>Inferência em tempo real]
    end

    Books --> MLService
    MLService --> Features
    Features --> TrainScript
    TrainScript --> Preprocessing
    Preprocessing --> Model
    Model --> Evaluation
    Evaluation --> PKL
    PKL --> Metadata

    PKL -->|Auto-carregamento no startup| LoadModel
    LoadModel --> PredictionEndpoint
    PredictionEndpoint --> Cache
    Cache -->|Cache hit| PredictionEndpoint
    Cache -->|Cache miss| Model
    PredictionEndpoint --> SaveDB

    MLService --> EP1
    MLService --> EP2
    MLService --> EP3
    LoadModel --> EP4
```

**Características Principais:**
- **Treinamento Automático:** Modelo treina na primeira inicialização se não estiver presente
- **Engenharia de Features:** 7 features extraídas (id, price_num, rating, availability_flag, category, image_present, title)
- **Modelo:** Random Forest Classifier para predição de rating alto/baixo (>=4 ou <4)
- **Cache:** Predições cacheadas para melhor performance
- **Persistência:** Todas as predições salvas no banco de dados

---

## 4. Arquitetura de Escalabilidade Futura

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[NGINX / AWS ELB<br/>Load Balancer]
    end

    subgraph "Camada de Aplicação - Escalabilidade Horizontal"
        API1[Instância API 1<br/>Flask + Gunicorn]
        API2[Instância API 2<br/>Flask + Gunicorn]
        API3[Instância API N<br/>Flask + Gunicorn]
    end

    subgraph "Camada de Banco de Dados"
        PG_Primary[(PostgreSQL<br/>Primário - Escrita)]
        PG_Replica1[(PostgreSQL<br/>Réplica 1 - Leitura)]
        PG_Replica2[(PostgreSQL<br/>Réplica N - Leitura)]
    end

    subgraph "Camada de Cache"
        Redis[Redis Cluster<br/>Cache de Predições<br/>Armazenamento de Sessões]
    end

    subgraph "Serviços ML - Microserviços"
        MLTrain[Serviço de Treinamento ML<br/>Jobs Assíncronos]
        MLInference[Serviço de Inferência ML<br/>API em Tempo Real]
        MLMonitor[Monitoramento de Modelo<br/>Detecção de Drift]
    end

    subgraph "Registro de Modelos"
        MLflow[MLflow / AWS S3<br/>Versionamento de Modelos]
        Models[Modelos:<br/>v1.0.0, v1.1.0<br/>Metadados, Métricas]
    end

    subgraph "Observabilidade"
        Prometheus[Prometheus<br/>Métricas]
        Grafana[Grafana<br/>Dashboards]
        ELK[ELK Stack<br/>Logs Centralizados]
    end

    subgraph "Fila de Mensagens"
        RabbitMQ[RabbitMQ / Kafka<br/>Tarefas Assíncronas]
        Workers[Workers Celery<br/>Scraping, Treinamento]
    end

    LB --> API1
    LB --> API2
    LB --> API3

    API1 --> Redis
    API2 --> Redis
    API3 --> Redis

    API1 --> PG_Primary
    API2 --> PG_Replica1
    API3 --> PG_Replica2

    PG_Primary -.->|Replicação| PG_Replica1
    PG_Primary -.->|Replicação| PG_Replica2

    API1 --> MLInference
    API2 --> MLInference
    API3 --> MLInference

    MLInference --> MLflow
    MLTrain --> MLflow
    MLTrain --> Models
    MLInference --> Redis

    API1 --> RabbitMQ
    RabbitMQ --> Workers
    Workers --> MLTrain

    API1 --> Prometheus
    API2 --> Prometheus
    API3 --> Prometheus
    Prometheus --> Grafana

    API1 --> ELK
    API2 --> ELK
    MLInference --> ELK
    MLTrain --> ELK

    MLInference --> MLMonitor
    MLMonitor --> Grafana
```

**Estratégias de Escalabilidade:**

### Escalabilidade Horizontal
- **Camada de API:** Múltiplas instâncias Flask + Gunicorn atrás de load balancer
- **Banco de Dados:** Replicação PostgreSQL (1 primário para escrita, N réplicas para leitura)
- **Cache:** Redis Cluster para distribuir carga

### Microserviços ML
- **Treinamento ML:** Serviço separado para retreinamento (assíncrono)
- **Inferência ML:** API dedicada para predições em tempo real
- **Monitoramento de Modelo:** Detecção de drift e degradação

### Processamento Assíncrono
- **Fila de Mensagens:** RabbitMQ/Kafka para tarefas assíncronas
- **Workers:** Celery para scraping e treinamento em background

### Observabilidade
- **Métricas:** Prometheus + Grafana (latência, throughput, erros)
- **Logs:** ELK Stack centralizado
- **Tracing:** Rastreamento distribuído (futuro: Jaeger/Zipkin)

### Registro de Modelos
- **MLflow:** Versionamento de modelos, métricas, experimentos
- **Armazenamento:** S3/MinIO para arquivos .pkl

---

## 5. Fluxo de Dados para Data Scientists

```mermaid
sequenceDiagram
    participant DS as Data Scientist
    participant API as REST API
    participant ML as Serviço ML
    participant DB as PostgreSQL

    Note over DS: Exploração de Features
    DS->>API: GET /api/v1/ml/manifest
    API->>ML: get_feature_manifest()
    ML-->>API: Schema de features (7 features)
    API-->>DS: JSON com definições de features

    Note over DS: Obter Features Paginadas
    DS->>API: GET /api/v1/ml/features?page=1&per_page=100
    API->>ML: get_features(page, per_page)
    ML->>DB: SELECT books + transformar
    DB-->>ML: Dados brutos
    ML-->>API: Features transformadas
    API-->>DS: JSON com features + paginação

    Note over DS: Exportar Dataset Completo
    DS->>API: GET /api/v1/ml/training-data?format=csv&label=rating
    API->>ML: get_training_data(label, format)
    ML->>DB: SELECT * FROM books
    DB-->>ML: Todos os registros
    ML-->>API: Arquivo CSV
    API-->>DS: training_data.csv

    Note over DS: Treinar Modelo Local
    DS->>DS: Carregar CSV no pandas
    DS->>DS: Treinar modelo customizado
    DS->>DS: Avaliar modelo

    Note over DS: Salvar Predição
    DS->>API: POST /api/v1/ml/predictions
    API->>DB: INSERT INTO predictions
    DB-->>API: Salvo
    API-->>DS: 201 Created
```

**Endpoints para Data Scientists:**
1. **GET /ml/manifest** - Entender schema de features
2. **GET /ml/features** - Obter features paginadas
3. **GET /ml/training-data** - Exportar dataset completo (JSON ou CSV)
4. **POST /ml/predictions** - Salvar predições de modelos externos

---

## 6. Fluxo de Dados para ML Engineers

```mermaid
sequenceDiagram
    participant MLE as ML Engineer
    participant API as REST API
    participant ModelService as Serviço de Modelo ML
    participant Cache as Cache de Predições
    participant DB as Database

    Note over MLE: Setup - Treinar Modelo
    MLE->>MLE: Executar: python ml_training/train_model.py
    MLE->>DB: Buscar dados de treinamento
    DB-->>MLE: Dataset de livros
    MLE->>MLE: Engenharia de features
    MLE->>MLE: Treinar Random Forest
    MLE->>MLE: Salvar: models/rating_classifier_v1.0.0.pkl

    Note over API: Auto-carregamento no Startup
    API->>ModelService: load_models()
    ModelService->>ModelService: Carregar arquivo .pkl
    ModelService-->>API: Modelos prontos

    Note over MLE: Predição em Tempo Real
    MLE->>API: POST /ml/predictions
    API->>Cache: Verificar cache(book_id)

    alt Cache Hit
        Cache-->>API: Predição cacheada
        API-->>MLE: predição + from_cache: true
    else Cache Miss
        API->>ModelService: predict(book_id, prediction_type)
        ModelService->>DB: Obter features do livro
        DB-->>ModelService: Dados do livro
        ModelService->>ModelService: Transformar features
        ModelService->>ModelService: model.predict()
        ModelService-->>API: Resultado da predição
        API->>Cache: Armazenar no cache
        API->>DB: INSERT INTO predictions
        API-->>MLE: predição + saved_prediction_id
    end

    Note over MLE: Retreinamento
    MLE->>MLE: Monitorar performance do modelo
    MLE->>API: GET /ml/training-data?format=json
    API-->>MLE: Dataset mais recente
    MLE->>MLE: Retreinar com novos dados
    MLE->>MLE: Salvar nova versão: v1.1.0.pkl
    MLE->>API: Reiniciar API (auto-reload novo modelo)
```

**Fluxo de Trabalho para ML Engineers:**
1. **Treinamento:** Executar script de treinamento, salvar .pkl
2. **Deploy:** Modelo auto-carregado no startup da API
3. **Inferência:** POST /ml/predictions para predição em tempo real
4. **Cache:** Predições cacheadas para performance
5. **Retreinamento:** Buscar novos dados, retreinar, fazer deploy da nova versão
