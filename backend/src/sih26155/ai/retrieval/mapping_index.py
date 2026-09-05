class MappingIndex:
    def __init__(self):
        self._mappings: list[dict] = []

    def add_mapping(self, mapping: dict) -> None:
        self._mappings.append(mapping)

    def find_similar(
        self,
        unknown_text: str,
        top_k: int = 3,
    ) -> list[dict]:
        if not self._mappings:
            return []

        matches = []
        unknown_words = set(unknown_text.lower().split())

        for mapping in self._mappings:
            known_text = mapping.get("unknown_text", "")
            known_words = set(known_text.lower().split())

            score = len(unknown_words & known_words)

            if score > 0:
                matches.append((score, mapping))

        matches.sort(key=lambda item: item[0], reverse=True)

        return [mapping for _, mapping in matches[:top_k]]