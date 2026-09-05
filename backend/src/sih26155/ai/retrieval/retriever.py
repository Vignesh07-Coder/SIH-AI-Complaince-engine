from .mapping_index import MappingIndex


class Retriever:
    def __init__(self, mapping_index: MappingIndex):
        self._mapping_index = mapping_index

    def find_similar(
        self,
        unknown_text: str,
        top_k: int = 3,
    ) -> list[dict]:
        return self._mapping_index.find_similar(
            unknown_text,
            top_k=top_k,
        )