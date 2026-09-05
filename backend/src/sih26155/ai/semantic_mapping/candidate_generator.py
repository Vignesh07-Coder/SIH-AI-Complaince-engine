from sih26155.core.contracts.ai import CandidateMapping


def generate_candidates(
    unknown_text: str,
    context: str,
    similar_examples: list[dict],
) -> list[CandidateMapping]:
    """
    Produces raw candidate mappings for an unrecognized config line,
    using similar past examples as evidence. Confidence is left at 0
    here — ai/confidence/scorer.py fills in the real value.
    """
    if similar_examples:
        best = similar_examples[0]
        return [CandidateMapping(
            field=best["field"],
            value=best["value"],
            confidence=0.0,
            reason=f"Resembles a known pattern: '{best['source_text']}'",
        )]

    return [CandidateMapping(
        field="unknown_field",
        value=None,
        confidence=0.0,
        reason="No similar pattern found in vendor or learned mappings.",
    )]