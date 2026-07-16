from fastapi import APIRouter, HTTPException

from sqlalchemy import text

from services.database import engine
from services.score_service import get_stock_score as fetch_stock_score
from services.exceptions import (
    CompanyNotFoundError,
    ScoreNotFoundError
)

router = APIRouter()


@router.get("/stocks/{ticker}")
def get_stock(ticker: str):

    sql = text("""
        SELECT
            c.ticker,
            c.name_zh,
            sp.close_price,
            sp.trade_date

        FROM companies c

        JOIN stock_prices sp
        ON c.company_id = sp.company_id

        WHERE c.ticker = :ticker

        ORDER BY sp.trade_date DESC

        LIMIT 1
    """)

    with engine.connect() as conn:

        result = conn.execute(
            sql,
            {
                "ticker": ticker
            }
        ).fetchone()

    if result is None:

        return {
            "error": "stock not found"
        }

    return {

        "ticker": result[0],

        "name": result[1],

        "latest_price": float(result[2]),

        "date": str(result[3])

    }


@router.get("/stocks/{ticker}/analysis")
def get_stock_analysis(ticker: str):

    sql = text("""
        SELECT
            c.ticker,
            c.name_zh,

            sp.close_price,
            sp.trade_date,

            MAX(
                CASE
                    WHEN d.indicator_code='MA_5'
                    THEN iv.value
                END
            ) AS ma5,

            MAX(
                CASE
                    WHEN d.indicator_code='MA_20'
                    THEN iv.value
                END
            ) AS ma20,

            MAX(
                CASE
                    WHEN d.indicator_code='MA_60'
                    THEN iv.value
                END
            ) AS ma60,

            MAX(
                CASE
                    WHEN d.indicator_code='RSI_14'
                    THEN iv.value
                END
            ) AS rsi,

            MAX(
                CASE
                    WHEN d.indicator_code='MACD'
                    THEN iv.value
                END
            ) AS macd

        FROM companies c

        JOIN stock_prices sp
        ON c.company_id = sp.company_id

        LEFT JOIN indicator_values iv
        ON c.company_id = iv.company_id
        AND iv.trade_date = sp.trade_date

        LEFT JOIN indicator_definitions d
        ON iv.indicator_id = d.indicator_id

        WHERE c.ticker = :ticker

        GROUP BY
            c.ticker,
            c.name_zh,
            sp.close_price,
            sp.trade_date

        ORDER BY sp.trade_date DESC

        LIMIT 1
    """)

    with engine.connect() as conn:

        result = conn.execute(
            sql,
            {
                "ticker": ticker
            }
        ).fetchone()

    if result is None:

        return {
            "error": "stock not found"
        }

    return {

        "ticker": result.ticker,

        "name": result.name_zh,

        "market": {

            "latest_price": float(
                result.close_price
            ),

            "trade_date": str(
                result.trade_date
            )
        },

        "technical": {

            "MA_5": float(result.ma5)
            if result.ma5 else None,

            "MA_20": float(result.ma20)
            if result.ma20 else None,

            "MA_60": float(result.ma60)
            if result.ma60 else None,

            "RSI_14": float(result.rsi)
            if result.rsi else None,

            "MACD": float(result.macd)
            if result.macd else None
        }
    }


@router.get("/stocks/{ticker}/score")
def get_stock_score(ticker: str):
    """
    改成直接讀 stock_scores 資料表（透過 score_service），
    不再即時計算，確保跟 /diagnosis 端點回傳同一份資料。
    如果該股票還沒跑過批次評分（scripts/run_score_batch.py），回 404。
    """

    try:

        score = fetch_stock_score(ticker)

    except (CompanyNotFoundError, ScoreNotFoundError):

        raise HTTPException(
            status_code=404,
            detail=f"{ticker} 尚未有評分資料，請先執行批次評分"
        )

    return score
