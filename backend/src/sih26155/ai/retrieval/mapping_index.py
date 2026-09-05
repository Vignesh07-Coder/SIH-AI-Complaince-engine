import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


class MappingIndex:
    """
    Loads all known mappings (vendor + learned) and computes real
    sentence embeddings for semantic similarity search.
    """

    def __init__(self, vendor_dir: str, learned_dir: str):
        self._entries: list[dict] = []
        self._load(vendor_dir)
        self._load(learned_dir)
        self._embeddings = self._compute_embeddings()

    def _load(self, directory: str):
        path = Path(directory)
        if not path.exists():
            return
        for file in path.glob("*.json"):
            try:
                data = json.loads(file.read_text())
            except json.JSONDecodeError:
                continue
            self._entries.extend(data if isinstance(data, list) else [data])

    def _compute_embeddings(self):
        if not self._entries:
            return np.zeros((0, 384))
        texts = [e.get("source_text", "") for e in self._entries]
        model = _get_model()
        return model.encode(texts, convert_to_numpy=True)

    def all_entries(self) -> list[dict]:
        return self._entries

    def embeddings(self):
        return self._embeddings

    def reload(self, vendor_dir: str, learned_dir: str):
        self._entries = []
        self._load(vendor_dir)
        self._load(learned_dir)
        self._embeddings = self._compute_embeddings()