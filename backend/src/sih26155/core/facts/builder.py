from __future__ import annotations

from typing import Any

from sih26155.core.facts.models import SecurityFact
from sih26155.core.schema.models import SecurityBaseline


def build_security_baseline(
    facts: list[SecurityFact],
) -> SecurityBaseline:
    """
    Build a vendor-neutral SecurityBaseline from canonical SecurityFacts.

    The builder knows nothing about vendor-specific configuration syntax.
    It only consumes canonical SecurityFact field paths.
    """

    baseline = SecurityBaseline()

    for fact in facts:
        _apply_fact(baseline, fact)

    return baseline


def _apply_fact(
    baseline: SecurityBaseline,
    fact: SecurityFact,
) -> None:
    """
    Apply one canonical SecurityFact to the SecurityBaseline.

    Unknown fields are intentionally ignored. This allows the canonical
    schema to evolve without making the builder crash on unfamiliar facts.
    """

    field = fact.field
    value = fact.value

    if field == "device.hostname":
        baseline.device.hostname = value

    elif field == "device.vendor":
        baseline.device.vendor = value

    elif field == "device.model":
        baseline.device.model = value

    elif field == "device.platform":
        baseline.device.platform = value

    elif field == "device.os_version":
        baseline.device.os_version = value

    elif field == "management.ssh.enabled":
        baseline.management.ssh.enabled = value

    elif field == "management.ssh.version":
        baseline.management.ssh.version = value

    elif field == "management.telnet.enabled":
        baseline.management.telnet.enabled = value

    elif field == "management.http.enabled":
        baseline.management.http.enabled = value

    elif field == "authentication.login_protection":
        _apply_login_protection(
            baseline,
            value,
        )

    elif field == "logging.enabled":
        baseline.logging.enabled = value


def _apply_login_protection(
    baseline: SecurityBaseline,
    value: Any,
) -> None:
    """
    Apply the canonical authentication.login_protection object.
    """

    if not isinstance(value, dict):
        return

    login_protection = baseline.authentication.login_protection

    if "enabled" in value:
        login_protection.enabled = value["enabled"]

    if "attempts" in value:
        login_protection.attempts = value["attempts"]

    if "window_seconds" in value:
        login_protection.window_seconds = value["window_seconds"]

    if "block_seconds" in value:
        login_protection.block_seconds = value["block_seconds"]