from flask import Blueprint, jsonify, request, Response
from flask.wrappers import Response as WrResponse

from app.controller.ml_controller import MLController
import io
import csv

ml_bp = Blueprint("ml", __name__, url_prefix="/api/v1/ml")


@ml_bp.route("/features", methods=["GET"])
def get_features() -> WrResponse | tuple[WrResponse, int]:
    """
    Listar features geradas a partir dos livros (paginado)
    ---
    tags:
      - ML
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: category
        in: query
        type: string
        required: false
    responses:
      200:
        description: Lista paginada de features
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category', None)

    controller = MLController()
    result = controller.call_controller(page=page, per_page=per_page, category=category)

    return jsonify(result.model_dump())


@ml_bp.route("/manifest", methods=["GET"])
def get_manifest() -> WrResponse | tuple[WrResponse, int]:
    """
    Retornar manifesto das features (nomes, tipos, nullable)
    ---
    tags:
      - ML
    responses:
      200:
        description: Manifesto das features
    """
    controller = MLController()
    result = controller.call_manifest()
    return jsonify(result)


@ml_bp.route("/training-data", methods=["GET"])
def get_training_data() -> WrResponse | tuple[WrResponse, int]:
    """
    Retornar dataset para treinamento formatado (JSON ou CSV)
    ---
    tags:
      - ML
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 100
      - name: label
        in: query
        type: string
        default: rating
        description: Nome do atributo que será usado como label
      - name: sample
        in: query
        type: number
        required: false
        description: Se fração entre 0 e 1, faz amostragem; se >=1, trata como número de linhas
      - name: format
        in: query
        type: string
        default: json
        description: json ou csv
    responses:
      200:
        description: Dataset para treinamento
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 100, type=int)
    label = request.args.get('label', 'rating')
    sample_raw = request.args.get('sample', None)
    seed_raw = request.args.get('seed', None)
    fmt = (request.args.get('format', 'json') or 'json').lower()

    # parse sample param: may be float or int
    sample = None
    if sample_raw is not None:
        try:
            # try float first
            sample_val = float(sample_raw)
            sample = sample_val
        except Exception:
            sample = None
    # parse seed param: may be int
    seed = None
    if seed_raw is not None:
        try:
            seed = int(seed_raw)
        except Exception:
            seed = None

    controller = MLController()

    try:
        rows, total = controller.call_training_data(page=page, per_page=per_page, label=label, sample=sample, seed=seed)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # JSON format
    if fmt == 'json':
        return jsonify({"rows": rows, "rows_count": len(rows), "total": total, "format": "json"})

    # CSV format
    elif fmt == 'csv':
        # prefer canonical order from manifest to ensure stability
        manifest = controller.call_manifest()
        manifest_cols = [f['name'] for f in manifest['features']]
        # final header order: manifest features (in order) plus the label if not already present
        headers = manifest_cols.copy()
        if label not in headers:
            headers.append(label)
        # rows may include only a subset; ensure all headers exist when writing

        # if rows exist, we keep the manifest order for CSV columns; missing values will be empty

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            # ensure all keys present and respect order
            writer.writerow({k: ('' if r.get(k) is None else r.get(k)) for k in headers})

        csv_data = output.getvalue()
        return Response(csv_data, mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=training_data.csv"})

    else:
        return jsonify({"error": "Invalid format param, use 'json' or 'csv'"}), 400


@ml_bp.route("/predictions", methods=["POST"])
def post_predictions() -> WrResponse | tuple[WrResponse, int]:
    """
    Fazer predições com um modelo (batch ou single)
    ---
    tags:
      - ML
    parameters:
      - name: model_version
        in: query
        type: string
        required: false
        description: Versão do modelo a ser usada
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              model_version:
                type: string
              instances:
                type: array
                items:
                  type: object
    responses:
      200:
        description: Predições geradas
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    # payload can be {"instances": [...], "model_version": "v1"} or directly a list of instances
    instances = None
    model_version = request.args.get('model_version', None)

    if isinstance(payload, list):
        instances = payload
    elif isinstance(payload, dict):
        instances = payload.get('instances')
        # model_version may be provided in body
        model_version = payload.get('model_version') or model_version
    else:
        return jsonify({"error": "Payload must be a list of instances or an object with 'instances' key"}), 400

    if not isinstance(instances, list):
        return jsonify({"error": "'instances' must be a list"}), 400

    controller = MLController()

    try:
        preds = controller.call_predict(instances=instances, model_version=model_version)
    except Exception as e:
        return jsonify({"error": "Prediction error", "message": str(e)}), 500

    return jsonify({"predictions": preds}), 200
