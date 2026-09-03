from pydantic import BaseModel


class Evidence(BaseModel):
    source_file: str
    raw_text: str
    line_number: int | None = None

    source_type: str = "configuration"
    parser: str | None = None
    confidence: float = 1.0