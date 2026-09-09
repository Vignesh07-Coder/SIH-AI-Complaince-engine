from fastapi import APIRouter

from sih26155.api.schemas import AnalysisRequest, AnalysisResponse
from sih26155.core.pipeline.analyze import analyze_config


router = APIRouter(
    prefix="/api",
    tags=["analysis"],
)


@router.post(
    "/analysis",
    response_model=AnalysisResponse,
)
def analyze(request: AnalysisRequest) -> AnalysisResponse:
    result = analyze_config(
        config=request.config,
        source_file=request.source_file,
    )

    return AnalysisResponse(
        **result.to_dict()
    )
