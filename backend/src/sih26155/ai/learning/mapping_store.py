from pathlib import Path
import json


class MappingStore:
    def __init__(self, storage_dir: str = "data/mappings/learned"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_mapping(self, mapping: dict, mapping_id: str) -> None:
        file_path = self.storage_dir / f"{mapping_id}.json"

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(mapping, file, indent=2)

    def load_mapping(self, mapping_id: str) -> dict | None:
        file_path = self.storage_dir / f"{mapping_id}.json"

        if not file_path.exists():
            return None

        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)