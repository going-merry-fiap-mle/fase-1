from typing import List, Dict, Any


class DummyModel:
    """A simple fallback model used during development.

    Prediction logic (deterministic heuristic):
      - If instance contains 'rating', return it as float.
      - Else if contains 'price_num', predict min(max(round(price_num/10), 1), 5).
      - Else return 3.0

    The model returns a list of dicts: {"prediction": float, "score": float}
    """

    def predict(self, instances: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for inst in instances:
            pred = None
            score = None
            if inst.get('rating') is not None:
                try:
                    pred = float(inst.get('rating'))
                    score = 1.0
                except Exception:
                    pred = 3.0
                    score = 0.0
            elif inst.get('price_num') is not None:
                try:
                    val = float(inst.get('price_num'))
                    pred = float(max(1, min(5, round(val / 10))))
                    score = 0.5
                except Exception:
                    pred = 3.0
                    score = 0.0
            else:
                pred = 3.0
                score = 0.0

            results.append({"prediction": pred, "score": score})
        return results


class ModelStore:
    """Simple model registry/loader.

    For now it returns a DummyModel regardless of version; in future it can load from disk or cloud storage by model_version.
    """

    def __init__(self) -> None:
        # placeholder for registry
        self._models = {}

    def load_model(self, model_version: str | None = None):
        # in prod this should load model artifact by version
        # here we always return DummyModel
        return DummyModel()

