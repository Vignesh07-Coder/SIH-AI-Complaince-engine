import json
from pathlib import Path
from datetime import datetime, timezone

LEARNED_DIR = Path("data/mappings/learned")


def save_approved_mapping(mapping: dict) -> None:
    """
    Saves an approved mapping. Expects at minimum:
    source_text, field, value, confidence, status, approved_by,
    context, created_at.
    """
    LEARNED_DIR.mkdir(parents=True, exist_ok=True)
    mapping.setdefault("created_at", datetime.now(timezone.utc).isoformat())

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    safe_field = str(mapping.get("field", "unknown")).replace(".", "_")
    filename = LEARNED_DIR / f"{safe_field}_{timestamp}.json"
    filename.write_text(json.dumps(mapping, indent=2))


def load_all_learned() -> list[dict]:
    if not LEARNED_DIR.exists():
        return []
    return [json.loads(f.read_text()) for f in LEARNED_DIR.glob("*.json")]
