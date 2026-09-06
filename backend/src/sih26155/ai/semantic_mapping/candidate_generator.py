from sih26155.core.contracts.ai import CandidateMapping

# The known, valid SBM semantic fields. Extend this list as the
# Security Baseline Model grows — do not invent fields outside it.
VALID_SBM_FIELDS = {
    "management.ssh.enabled",
    "management.ssh.version",
    "management.http.enabled",
    "management.telnet.enabled",
    "authentication.login_protection.enabled",
    "logging.enabled",
}


def generate_candidates(
    unknown_text: str,
    context: str,
    similar_examples: list[dict],
) -> list[CandidateMapping]:
    """
    Produces raw candidate mappings for an unrecognized config line,
    using similar past examples as evidence. Confidence is left at 0
    here — ai/confidence/scorer.py fills in the real value.

    Never returns a field outside the known SBM vocabulary. If the
    best match's field is not valid, returns UNKNOWN instead of
    inventing or guessing a field name.
    """
    if similar_examples:
        best = similar_examples[0]
        field = best.get("field")

        if field in VALID_SBM_FIELDS:
            return [CandidateMapping(
                field=field,
                value=best.get("value"),
                confidence=0.0,
                reason=f"Resembles a known pattern: '{best.get('source_text', '')}'",
            )]

        return [CandidateMapping(
            field="UNKNOWN",
            value=None,
            confidence=0.0,
            reason=(
                f"Closest match found ('{best.get('source_text', '')}') maps to "
                f"'{field}', which is not a recognized SBM field. Flagged as UNKNOWN "
                "rather than inventing a mapping."
            ),
        )]

    return [CandidateMapping(
        field="UNKNOWN",
        value=None,
        confidence=0.0,
        reason="No similar pattern found in vendor or learned mappings.",
    )]