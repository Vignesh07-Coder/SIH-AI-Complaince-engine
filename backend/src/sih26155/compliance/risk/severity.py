SEVERITY_WEIGHTS = {
    "critical": 10,
    "high": 8,
    "medium": 5,
    "low": 2,
    "info": 0,
}


def normalize_severity(severity: str) -> str:
    normalized = severity.lower().strip()

    if normalized not in SEVERITY_WEIGHTS:
        raise ValueError(
            f"Unsupported severity: {severity}"
        )

    return normalized


def severity_weight(severity: str) -> int:
    return SEVERITY_WEIGHTS[
        normalize_severity(severity)
    ]