def score_candidate(candidate: dict, similar_examples: list[dict]) -> float:
    if not similar_examples:
        return 0.2

    confidence = 0.5 + (0.1 * min(len(similar_examples), 4))

    return min(confidence, 0.9)