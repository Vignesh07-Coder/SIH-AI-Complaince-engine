from typing import Any

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    config: str = Field(min_length=1)
    source_file: str = Field(default="uploaded-config.cfg")


class AnalysisResponse(BaseModel):
    vendor: dict[str, Any]
    facts: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    baseline: dict[str, Any]
    findings: list[dict[str, Any]]
    remediations: list[dict[str, Any]]


class ReportRequest(BaseModel):
    source_file: str = Field(default="uploaded-config.cfg")
    analysis: AnalysisResponse
