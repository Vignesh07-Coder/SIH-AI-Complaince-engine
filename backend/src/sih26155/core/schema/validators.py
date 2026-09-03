from .models import SecurityBaseline


def validate_baseline(baseline: SecurityBaseline) -> SecurityBaseline:
    if baseline.management.ssh.version is not None:
        if baseline.management.ssh.version not in (1, 2):
            raise ValueError("Unsupported SSH version")

    return baseline