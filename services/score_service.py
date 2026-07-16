import json

from sqlalchemy import text

from services.database import engine
from services.exceptions import (
    CompanyNotFoundError,
    ScoreNotFoundError
)


def save_stock_score(
    ticker,
    score_data
):

    # 找 company_id

    company_sql = text("""
        SELECT company_id
        FROM companies
        WHERE ticker = :ticker
    """)

    with engine.connect() as conn:

        company = conn.execute(
            company_sql,
            {
                "ticker": ticker
            }
        ).fetchone()

    if company is None:

        raise CompanyNotFoundError(
            f"{ticker} 不存在 companies"
        )

    company_id = company[0]

    insert_sql = text("""
        INSERT INTO stock_scores
        (
            company_id,
            trade_date,
            total_score,
            signal,
            trend_score,
            momentum_score,
            macd_score,
            risk_score,
            reasons
        )

        VALUES
        (
            :company_id,
            CURRENT_DATE,
            :total_score,
            :signal,
            :trend_score,
            :momentum_score,
            :macd_score,
            :risk_score,
            CAST(:reasons AS jsonb)
        )

        ON CONFLICT(company_id, trade_date)

        DO UPDATE SET

            total_score = EXCLUDED.total_score,
            signal = EXCLUDED.signal,
            trend_score = EXCLUDED.trend_score,
            momentum_score = EXCLUDED.momentum_score,
            macd_score = EXCLUDED.macd_score,
            risk_score = EXCLUDED.risk_score,
            reasons = EXCLUDED.reasons

    """)

    with engine.begin() as conn:

        conn.execute(
            insert_sql,
            {
                "company_id": company_id,
                "total_score": score_data["score"],
                "signal": score_data["signal"],
                "trend_score": score_data["breakdown"]["trend_score"],
                "momentum_score": score_data["breakdown"]["momentum_score"],
                "macd_score": score_data["breakdown"]["macd_score"],
                "risk_score": score_data["breakdown"]["risk_score"],
                "reasons": json.dumps(score_data["reasons"], ensure_ascii=False)
            }
        )

    print(
        f"✅ {ticker} Score saved"
    )


def get_stock_score(ticker):
    """
    評分資料唯一讀取入口。
    /stocks/{ticker}/score 和 /stocks/{ticker}/diagnosis
    都應該呼叫這支函式，確保兩邊看到同一份資料。
    """

    sql = text("""
        SELECT
            c.ticker,
            c.name_zh,
            s.total_score,
            s.signal,
            s.trend_score,
            s.momentum_score,
            s.macd_score,
            s.risk_score,
            s.reasons
        FROM stock_scores s
        JOIN companies c
            ON s.company_id = c.company_id
        WHERE c.ticker = :ticker
        ORDER BY s.trade_date DESC
        LIMIT 1
    """)

    with engine.connect() as conn:

        row = conn.execute(
            sql,
            {
                "ticker": ticker
            }
        ).mappings().fetchone()

    if row is None:
        raise ScoreNotFoundError(
            f"{ticker} 沒有 Score 資料"
        )

    return {
        "ticker": row["ticker"],
        "name": row["name_zh"],
        "score": row["total_score"],
        "signal": row["signal"],
        "breakdown": {
            "trend_score": row["trend_score"],
            "momentum_score": row["momentum_score"],
            "macd_score": row["macd_score"],
            "risk_score": row["risk_score"]
        },
        "reasons": row["reasons"]
    }