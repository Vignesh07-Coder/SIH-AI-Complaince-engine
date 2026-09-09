from typing import Any


SUPPORTED_OPERATORS = {
    "eq",
    "neq",
    "gt",
    "gte",
    "lt",
    "lte",
    "in",
    "not_in",
    "truthy",
    "falsy",
}


def evaluate_operator(
    observed: Any,
    operator: str,
    expected: Any,
) -> bool:
    if operator not in SUPPORTED_OPERATORS:
        raise ValueError(
            f"Unsupported compliance operator: {operator}"
        )

    if operator == "eq":
        return observed == expected

    if operator == "neq":
        return observed != expected

    if operator == "gt":
        return observed > expected

    if operator == "gte":
        return observed >= expected

    if operator == "lt":
        return observed < expected

    if operator == "lte":
        return observed <= expected

    if operator == "in":
        if not isinstance(expected, list):
            raise ValueError(
                "'in' operator requires expected to be a list."
            )
        return observed in expected

    if operator == "not_in":
        if not isinstance(expected, list):
            raise ValueError(
                "'not_in' operator requires expected to be a list."
            )
        return observed not in expected

    if operator == "truthy":
        return bool(observed)

    if operator == "falsy":
        return not bool(observed)

    raise ValueError(
        f"Unsupported compliance operator: {operator}"
    )