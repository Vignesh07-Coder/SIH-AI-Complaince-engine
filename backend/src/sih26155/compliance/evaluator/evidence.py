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
    Resolve a semantic field from the Security Baseline Model.

    Supports nested object access such as:

        management.http.enabled

    and dictionary input such as:

        {
            "management": {
                "http": {
                    "enabled": True
                }
            }
        }

    A dictionary may also contain the complete semantic path
    as a key.
    """

    if isinstance(sbm, dict):
        if semantic_field in sbm:
            return sbm[semantic_field]

    current = sbm

    for part in semantic_field.split("."):
        current = _get_member(current, part)

        if current is MISSING:
            return MISSING

    return current


def get_evidence(
    sbm: Any,
    semantic_field: str,
) -> list[Any]:
    """
    Return evidence associated with a semantic field when the
    supplied object exposes evidence information.

    The canonical SecurityBaseline currently does not contain
    evidence fields, so an ordinary SecurityBaseline returns
    an empty list rather than fabricating evidence.

    If an integration layer supplies evidence as a dictionary,
    this function supports:

        {
            "evidence": {
                "management.http.enabled": [...]
            }
        }

    It also supports fact-style objects containing:

        field
        evidence
    """

    evidence = _get_member(sbm, "evidence")

    if isinstance(evidence, dict):
        result = evidence.get(semantic_field, [])

        if isinstance(result, list):
            return result

        if result is not MISSING and result is not None:
            return [result]

        return []

    facts = _get_member(sbm, "facts")

    if facts is MISSING or facts is None:
        return []

    result: list[Any] = []

    try:
        iterator = iter(facts)
    except TypeError:
        return []

    for fact in iterator:
        field = _get_member(fact, "field")

        if field != semantic_field:
            continue

        fact_evidence = _get_member(
            fact,
            "evidence",
        )

        if fact_evidence is MISSING or fact_evidence is None:
            continue

        if isinstance(fact_evidence, list):
            result.extend(fact_evidence)
        else:
            result.append(fact_evidence)

    return result