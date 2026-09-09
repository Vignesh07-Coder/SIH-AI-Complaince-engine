from typing import Any


MISSING = object()


def _get_member(obj: Any, key: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, MISSING)

    return getattr(obj, key, MISSING)


def get_semantic_value(
    sbm: Any,
    semantic_field: str,
) -> Any:
    if isinstance(sbm, dict) and semantic_field in sbm:
        return sbm[semantic_field]

    current = sbm

    for part in semantic_field.split("."):
        current = _get_member(current, part)

        if current is MISSING:
            return MISSING

    return current