import json
from pathlib import Path
from datetime import datetime, timezone

VERSIONS_DIR = Path("data/mappings/learned/_versions")


def record_version(mapping_id: str, mapping: dict) -> None:
    """Keeps a history entry every time a mapping is created or edited."""
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    version_file = VERSIONS_DIR / f"{mapping_id}_{timestamp}.json"
    version_file.write_text(json.dumps(mapping, indent=2))


def get_version_history(mapping_id: str) -> list[dict]:
    if not VERSIONS_DIR.exists():
        return []
    files = sorted(VERSIONS_DIR.glob(f"{mapping_id}_*.json"))
    return [json.loads(f.read_text()) for f in files]