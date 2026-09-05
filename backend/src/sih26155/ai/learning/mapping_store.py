import json
from pathlib import Path
from datetime import datetime, timezone

LEARNED_DIR = Path("data/mappings/learned")


def save_approved_mapping(mapping: dict) -> None:
    LEARNED_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    safe_field = mapping["field"].replace(".", "_")
    filename = LEARNED_DIR / f"{safe_field}_{timestamp}.json"
    filename.write_text(json.dumps(mapping, indent=2))


def load_all_learned() -> list[dict]:
    if not LEARNED_DIR.exists():
        return []
    return [json.loads(f.read_text()) for f in LEARNED_DIR.glob("*.json")]