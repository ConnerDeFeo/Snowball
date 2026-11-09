from pydantic import BaseModel

class Finding(BaseModel):
    field: str
    value: str
    snippet: str
    status: str

class EvidenceResponse(BaseModel):
    findings: list[Finding]
    summary: str
