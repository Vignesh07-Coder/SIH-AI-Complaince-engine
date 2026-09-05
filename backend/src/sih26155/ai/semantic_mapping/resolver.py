from sih26155.core.contracts.ai import CandidateMapping
from sih26155.ai.retrieval.retriever import Retriever
from sih26155.ai.semantic_mapping.candidate_generator import generate_candidates
from sih26155.ai.confidence.scorer import score_candidate


class DefaultSemanticResolver:
    """
    Implements the SemanticResolver protocol from core/contracts/ai.py.
    Orchestrates retrieval, candidate generation, and confidence scoring.
    """

    def __init__(self, retriever: Retriever):
        self._retriever = retriever

    def resolve(self, unknown_text: str, context: str) -> list[CandidateMapping]:
        similar = self._retriever.find_similar(unknown_text)

        candidates = generate_candidates(unknown_text, context, [s[0] for s in similar])

        for c in candidates:
            c.confidence = score_candidate(c, similar)

        return sorted(candidates, key=lambda c: c.confidence, reverse=True)