import numpy as np
from sih26155.ai.retrieval.mapping_index import MappingIndex, _get_model


def _cosine_similarity(a, b) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


class Retriever:
    """
    Uses real sentence embeddings (not word matching) to find
    semantically similar past mappings for an unknown config line.
    """

    def __init__(self, index: MappingIndex):
        self._index = index

    def find_similar(self, unknown_text: str, top_k: int = 3) -> list[tuple[dict, float]]:
        entries = self._index.all_entries()
        embeddings = self._index.embeddings()
        if not entries or embeddings.shape[0] == 0:
            return []

        model = _get_model()
        query_vec = model.encode([unknown_text], convert_to_numpy=True)[0]

        scored = [
            (entries[i], _cosine_similarity(query_vec, embeddings[i]))
            for i in range(len(entries))
        ]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return scored[:top_k]