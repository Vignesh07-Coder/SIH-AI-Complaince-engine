from fastapi import APIRouter
from fastapi.responses import Response

from sih26155.api.schemas import ReportRequest
from sih26155.reporting.pdf.generator import build_report_filename, generate_pdf_report


router = APIRouter(
    prefix="/api",
    tags=["reports"],
)


@router.post("/reports")
def generate_report(request: ReportRequest) -> Response:
    report = generate_pdf_report(
        analysis=request.analysis.model_dump(),
        source_file=request.source_file,
    )
    filename = build_report_filename(request.source_file)

    return Response(
        content=report,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )
