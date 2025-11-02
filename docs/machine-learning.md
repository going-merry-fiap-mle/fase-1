# Documentação Machine Learning

Esta documentação descreve a implementação do pipeline de Machine Learning para predição de ratings de livros.

**Importante:** Este projeto utiliza Docker para todos os processos, incluindo treinamento de modelos ML. O endpoint de predições ML está disponível no ambiente de desenvolvimento (container `fiap-backend-dev`).

**Treinamento Automático:** O modelo é treinado automaticamente na primeira inicialização do container se não existir. Não é necessário executar comandos manuais de treinamento.

---

## 1. Visão Geral

### Sistema de ML
- **Modelo:** Random Forest Classifier (100 árvores)
- **Objetivo:** Predizer se livro terá rating alto (≥4) ou baixo (<4)
- **Features:** price, category, availability
- **Framework:** scikit-learn, joblib, numpy
- **Persistência:** Modelos salvos em `models/`

### Funcionalidades
- Treinamento automatizado via script Python
- Predições em tempo real via API REST
- Cache de predições
- Persistência de resultados no PostgreSQL
- Singleton pattern para carregamento de modelos

---

## 2. Instalação e Dependências

### Instalar pacotes ML
- **Comando:** `poetry install`
- **Pacotes principais:**
  - scikit-learn 1.7.2
  - joblib 1.5.2
  - numpy 2.2.3

### Verificar instalação
```bash
poetry run python -c "import sklearn; import joblib; import numpy; print('OK')"
```

---

## 3. Treinamento do Modelo

### Pré-requisitos
- Docker e docker-compose instalados
- Container backend rodando (`docker-compose -f docker-compose.dev.yml up -d`)
- PostgreSQL com dados de livros (tabelas `books` e `categories` populadas)
- Variável `DATABASE_URL` configurada no arquivo de ambiente de desenvolvimento (`.env.dev`)

### Treinamento Automático

O modelo é treinado **automaticamente** na primeira inicialização do container se não existir.

**Comportamento:**
1. Container inicia
2. Flask App verifica se `models/rating_classifier_v1.pkl` existe
3. Se não existir, executa automaticamente `ml_training/train_model.py`
4. Logs de treinamento aparecem no console
5. Após treinamento, aplicação carrega o modelo e fica disponível

**Logs esperados no startup:**
```
[INFO] ML model not found, initiating automatic training...
[Training] [TRAINING] Iniciando treinamento...
[Training] [DATA] 250 livros carregados
[Training] [TRAINING] Random Forest Classifier (100 trees)
[Training] [METRICS] Accuracy: 0.8600
[Training] [SAVE] Modelo salvo: models/rating_classifier_v1.pkl
[INFO] ML model trained successfully
[INFO] Modelos ML carregados com sucesso
```

### Treinamento Manual (Opcional)

Para retreinar o modelo manualmente (ex: após adicionar mais dados):

**Treinamento manual (desenvolvimento):**
```bash
docker exec fiap-backend-dev poetry run python ml_training/train_model.py
```

Após retreinamento manual, reinicie o container para recarregar o modelo:
```bash
docker-compose -f docker-compose.dev.yml restart backend-dev
```

### Arquivos gerados
- `models/rating_classifier_v1.pkl` - Modelo treinado
- `models/encoders_v1.pkl` - LabelEncoders (category, availability)
- `models/metadata_v1.pkl` - Metadados (accuracy, features, versão)

### Verificar modelos
```bash
# No host (Windows/Linux/Mac)
ls -lh models/

# Dentro do container
docker exec fiap-backend-dev ls -lh /app/models

# Saída esperada:
# rating_classifier_v1.pkl  (~500KB)
# encoders_v1.pkl           (~10KB)
# metadata_v1.pkl           (~5KB)
```

---

## 4. Pipeline de Treinamento

### Processo completo
1. **Conexão:** Conecta ao PostgreSQL via SQLAlchemy
2. **Extração:** Busca livros com `JOIN` em categories
3. **Features:** Prepara `price`, `category_encoded`, `availability_encoded`
4. **Target:** Cria `high_rating` (1 se rating ≥ 4, senão 0)
5. **Split:** 80% treino, 20% teste (stratified)
6. **Treinamento:** Random Forest (100 estimators, max_depth=10)
7. **Avaliação:** Calcula accuracy, precision, recall, F1-score
8. **Persistência:** Salva modelo, encoders e metadata com joblib

### Features utilizadas

| Feature | Tipo | Encoding |
|---------|------|----------|
| price | float | Numérico direto |
| category | string | LabelEncoder |
| availability | string | LabelEncoder |

### Métricas esperadas
```
Accuracy:  0.80 - 0.90
Precision: 0.80 - 0.90
Recall:    0.75 - 0.85
F1-Score:  0.80 - 0.88
```

---

## 5. Model Loader (Singleton)

### Localização
- **Arquivo:** `app/ml/model_loader.py`
- **Classe:** `MLModelLoader`
- **Instância global:** `ml_loader`

### Características
- Singleton: uma única instância global
- Carregamento automático na inicialização
- Cache de predições em memória
- Thread-safe para múltiplas requisições

### Métodos principais
```python
# Obter modelo
model = ml_loader.get_model('rating')

# Verificar se carregado
is_loaded = ml_loader.is_loaded('rating')

# Predição com cache
prediction, confidence, from_cache = ml_loader.predict_with_cache(
    model_type='rating',
    features=features_dict,
    cache_key=f"book_{book_id}"
)

# Limpar cache
ml_loader.clear_cache()
```

### Logs de inicialização
```
[ML] MODEL LOADER - Inicializando...
[OK] Modelo 'rating' carregado: rating_classifier_v1.pkl
[OK] Encoders carregados: encoders_v1.pkl
[OK] Metadata carregado: metadata_v1.pkl
[OK] 1 modelo(s) carregado(s) com sucesso!
```

---

## 6. API Endpoint

### POST /api/v1/ml/predictions

#### Modo 1: Executar ML em Tempo Real
Endpoint executa modelo e salva resultado automaticamente.

**Request:**
```json
{
  "book_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "prediction_type": "rating"
}
```

**Query Parameters:**
- `use_cache=true|false` (default: true)

**Response (200 OK):**
```json
{
  "success": true,
  "prediction": {
    "book_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "book_title": "The Great Gatsby",
    "predicted_value": "5",
    "predicted_label": "high",
    "confidence": 0.85,
    "model_version": "v1.0.0",
    "features_used": {
      "price": 29.99,
      "category": "Fiction",
      "availability": "In stock"
    },
    "from_cache": false
  },
  "saved_prediction_id": "uuid-da-predicao"
}
```

#### Modo 2: Salvar Predição Pré-calculada
Endpoint apenas salva predição já calculada.

**Request:**
```json
{
  "book_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "prediction_type": "rating",
  "predicted_value": "5",
  "confidence": 0.95,
  "model_version": "v1.0.0",
  "metadata": {"source": "external_model"}
}
```

**Response (201 Created):**
```json
{
  "id": "prediction-uuid",
  "book_id": "book-uuid",
  "prediction_type": "rating",
  "predicted_value": "5",
  "confidence": 0.95,
  "model_version": "v1.0.0",
  "metadata": {"source": "external_model"},
  "created_at": "2025-10-30T12:00:00Z"
}
```

#### Erros possíveis

**400 Bad Request - Validação:**
```json
{
  "error": "Invalid parameters",
  "details": [
    {"field": "book_id", "message": "Invalid UUID"}
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
  "message": "ML model 'rating' not loaded",
  "hint": "Run: python ml_training/train_model.py"
}
```

---

## 7. Configuração da Tabela Predictions

### Criar tabela no banco de dados
A tabela `predictions` é criada automaticamente via Alembic migrations.

**Desenvolvimento (Docker):**
```bash
docker exec fiap-backend-dev poetry run alembic upgrade head
```

A migration `add_predictions_ml` cria:
- Tabela `predictions` com constraints e indexes
- Foreign key para `books`
- Check constraint para `confidence` (0.0-1.0)
- Indexes para `book_id`, `prediction_type`, `created_at`

---

## 8. Arquitetura do Sistema ML

### Componentes

```
Training (Offline):
PostgreSQL → ml_training/train_model.py → models/

Inference (Online):
API → Controller → UseCase → MLModelService → Model Loader → Prediction
                                     ↓
                           PredictionService → PostgreSQL
```

### Fluxo de Predição

1. **API Endpoint:** Recebe request, valida com Pydantic
2. **Controller:** Cria instâncias de services e use case
3. **Use Case:** Orquestra MLModelService + PredictionService
4. **MLModelService:**
   - Busca livro no banco
   - Prepara features (encoding)
   - Executa predição via Model Loader
5. **PredictionService:** Salva resultado no banco
6. **Response:** Retorna JSON com predição

---

## 9. Cache de Predições

### Sistema de cache
- **Localização:** `app/ml/model_loader.py` (dicionário `_cache`)
- **Chave:** `{model_type}_{book_id}`
- **Conteúdo:** prediction, confidence, timestamp

### Benefícios
- **Performance:** 10x mais rápido (5ms vs 50ms)
- **Redução de carga:** Menos execuções do modelo
- **Transparente:** Indica `from_cache=true` na resposta

### Uso do cache
```bash
# Primeira requisição (sem cache)
curl -X POST http://localhost:5000/api/v1/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{"book_id": "uuid", "prediction_type": "rating"}'
# Response: from_cache=false, ~50ms

# Segunda requisição (com cache)
curl -X POST http://localhost:5000/api/v1/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{"book_id": "uuid", "prediction_type": "rating"}'
# Response: from_cache=true, ~5ms

# Desabilitar cache
curl -X POST http://localhost:5000/api/v1/ml/predictions?use_cache=false \
  -H "Content-Type: application/json" \
  -d '{"book_id": "uuid", "prediction_type": "rating"}'
# Response: from_cache=false
```

### Limpar cache
```python
from app.ml.model_loader import ml_loader
ml_loader.clear_cache()
```

---

## 10. Exemplos de Uso

### Predição via cURL
```bash
curl -X POST http://localhost:5000/api/v1/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "prediction_type": "rating"
  }'
```

### Salvar predição externa (Modo 2)
```bash
curl -X POST http://localhost:5000/api/v1/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "prediction_type": "rating",
    "predicted_value": "5",
    "confidence": 0.95,
    "model_version": "v1.0.0"
  }'
```

### Workflow completo com Docker

#### Desenvolvimento (Dev)

```bash
# 1. Iniciar ambiente de desenvolvimento
docker-compose -f docker-compose.dev.yml up -d

# Aguardar inicialização e treinamento automático (se necessário)
# Logs indicarão se modelo foi treinado ou carregado

# 2. Verificar logs de inicialização
docker logs fiap-backend-dev

# 3. Testar endpoint de predição
curl -X POST http://localhost:5000/api/v1/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{"book_id": "uuid-do-livro", "prediction_type": "rating"}'

# 4. Verificar modelos gerados (compartilhado via volume)
ls -lh models/

# 5. Monitorar logs em tempo real
docker logs fiap-backend-dev -f
```

#### Retreinamento Manual (Opcional)

Se necessário retreinar após adicionar novos dados:

```bash
# Retreinar em DEV
docker exec fiap-backend-dev poetry run python ml_training/train_model.py

# Reiniciar para recarregar o modelo
docker-compose -f docker-compose.dev.yml restart backend-dev
```

**Volumes configurados:**
- **Dev:** `./models:/app/models` - Modelos compartilhados + hot-reload

---

## 11. Testes

### Executar testes ML
- **Comando:** `poetry run pytest app/tests/api/test_ml_predictions.py -v`

### Testes principais
- Criação de predição com sucesso
- Validação de campos obrigatórios
- Validação de tipos de predição
- Validação de range de confidence (0.0-1.0)
- Tratamento de book_id inválido/inexistente
- Tratamento de erros internos
- Verificação de estrutura de resposta

### Executar todos os testes
```bash
poetry run pytest
# 138 passed in 2.39s
```

### Cobertura de testes
```bash
poetry run pytest --cov=app --cov-report=term-missing
# Total: 90%
```

---

## 12. Troubleshooting

### Modelo não carrega

O treinamento é automático, mas se encontrar problemas:

```bash
# 1. Verificar logs de inicialização
docker logs fiap-backend-dev | grep -i "training\|model"

# 2. Verificar se modelos existem
ls models/
docker exec fiap-backend-dev ls -lh /app/models

# 3. Se logs indicarem erro de treinamento, verificar pré-requisitos:
#    - Banco de dados configurado (DATABASE_URL)
#    - Pelo menos 100 livros no banco
#    - Conexão com PostgreSQL funcionando

# 4. Retreinar manualmente se necessário
docker exec fiap-backend-dev poetry run python ml_training/train_model.py

# 5. Reiniciar container
docker-compose -f docker-compose.dev.yml restart backend-dev
```

### Erro "Model not available" (503)
- **Causa:** Treinamento automático falhou ou não houve dados suficientes
- **Diagnóstico:** Verificar logs do container com `docker logs fiap-backend-dev`
- **Solução:**
  1. Garantir que há dados no banco (mínimo 100 livros)
  2. Verificar variável `DATABASE_URL` no `.env.dev`
  3. Retreinar manualmente se necessário

### Predição sem dados
- **Causa:** Banco de dados sem livros
- **Solução:** Popular banco via scraping ou seeds

### Cache não funcionando
```python
# Limpar e verificar
from app.ml.model_loader import ml_loader
ml_loader.clear_cache()
```

### Encoding error
- **Causa:** Valor desconhecido para category/availability
- **Solução:** Sistema retorna 0 como fallback automaticamente

### Endpoint retorna 201 mas dados não persistem no banco
- **Causa:** Falta `session.commit()` em `app/infrastructure/database.py`
- **Sintoma:** API retorna 201 Created mas `SELECT COUNT(*)` retorna 0
- **Solução:** Adicionar `session.commit()` após `yield session` no método `session_scope()`
- **Arquivo:** `app/infrastructure/database.py:48`
```python
@contextmanager
def session_scope(self) -> Generator[Session, None, None]:
    session: Session = self._session_factory()
    try:
        yield session
        session.commit()  # CRÍTICO: sem isso, dados não persistem
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
```

### Docker dev environment
- **Volumes necessários:** `./models:/app/models` e `./ml_training:/app/ml_training`
- **Rebuild:** `docker-compose -f docker-compose.dev.yml build --no-cache backend-dev`
- **Restart:** `docker-compose -f docker-compose.dev.yml up -d backend-dev`
- **Hot-reload:** Mudanças em Python são aplicadas automaticamente (volume mount)

---

## Observações

- **Docker-first:** Projeto utiliza containers para todos os processos (consistência e reprodutibilidade)
- **Ambiente:** Endpoint ML disponível no container de desenvolvimento (`fiap-backend-dev`)
- **Volumes compartilhados:** Modelos persistem via volume `./models:/app/models`
- **Modelos não versionados:** Arquivos em `models/` não são commitados (`.gitignore`)
- **Requisitos:** Mínimo ~100 livros no banco para treinar modelo com qualidade
- **Cache:** Limpa automaticamente ao reiniciar container
- **Autoload:** Modelo carrega automaticamente na inicialização do Flask
- **Reutilização:** Container backend serve tanto API quanto treinamento ML
