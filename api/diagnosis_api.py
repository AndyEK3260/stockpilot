from fastapi import APIRouter, HTTPException

from services.diagnosis_service import generate_diagnosis
from services.exceptions import (
    CompanyNotFoundError,
    ScoreNotFoundError
)
from schemas.diagnosis import DiagnosisResponse

router = APIRouter()


@router.get(
    "/stocks/{ticker}/diagnosis",
    response_model=DiagnosisResponse
)
def get_diagnosis(ticker: str):

    try:

        return generate_diagnosis(ticker)

    except (CompanyNotFoundError, ScoreNotFoundError):

        raise HTTPException(
            status_code=404,
            detail=f"{ticker} 尚未有評分資料，請先執行批次評分"
        )
