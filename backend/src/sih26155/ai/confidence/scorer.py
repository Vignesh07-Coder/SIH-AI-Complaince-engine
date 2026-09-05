from sih26155.core.contracts.ai import CandidateMapping


def score_candidate(
    candidate: CandidateMapping,
    similar_examples: list[tuple[dict, float]],
) -> float:
    """
    Converts retrieval evidence into a confidence score.
    Never returns 1.0 — the system should never claim total certainty.
    """
    if not similar_examples:
        return 0.2

    _, top_similarity = similar_examples[0]
    return round(min(top_similarity, 0.98), 2)