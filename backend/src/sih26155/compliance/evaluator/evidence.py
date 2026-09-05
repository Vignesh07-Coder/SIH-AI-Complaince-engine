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
    """
    Supports both:

    {
        "management.http.enabled": True
    }

    and nested:

    {
        "management": {
            "http": {
                "enabled": True
            }
        }
    }
    """

    if isinstance(sbm, dict):
        if semantic_field in sbm:
            return sbm[semantic_field]

    current = sbm

    for part in semantic_field.split("."):
        current = _get_member(current, part)

        if current is MISSING:
            break
    else:
        return current

    facts = _get_member(sbm, "facts")

    if facts is not MISSING:
        for fact in facts:
            field = _get_member(fact, "field")

            if field == semantic_field:
                value = _get_member(fact, "value")

                if value is not MISSING:
                    return value

    return MISSING


def get_evidence(
    sbm: Any,
    semantic_field: str,
) -> list[Any]:
    evidence = _get_member(sbm, "evidence")

    if isinstance(evidence, dict):
        result = evidence.get(semantic_field, [])
        return result if isinstance(result, list) else [result]

    facts = _get_member(sbm, "facts")

    if facts is not MISSING:
        result = []

        for fact in facts:
            field = _get_member(fact, "field")

            if field == semantic_field:
                fact_evidence = _get_member(
                    fact,
                    "evidence",
                )

                if fact_evidence is not MISSING:
                    if isinstance(fact_evidence, list):
                        result.extend(fact_evidence)
                    else:
                        result.append(fact_evidence)

        return result

    return []