from typing import List
from pydantic import BaseModel


class OverallSection(BaseModel):
    score: int
    signal: str
    confidence: int


class TechnicalBreakdown(BaseModel):
    trend_score: int
    momentum_score: int
    macd_score: int
    risk_score: int


class TechnicalSection(BaseModel):
    score: int
    breakdown: TechnicalBreakdown


class NoDataSection(BaseModel):
    status: str = "NO_DATA"


class DiagnosisResponse(BaseModel):
    ticker: str
    name: str
    overall: OverallSection
    technical: TechnicalSection
    financial: NoDataSection
    institutional: NoDataSection
    valuation: NoDataSection
    summary: str
    risks: List[str]
