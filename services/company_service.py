from sqlalchemy import text
from services.database import engine


def create_company(
    ticker,
    market,
    name_zh,
    name_en,
    industry
):

    sql = text("""
        INSERT INTO companies
        (
            ticker,
            market,
            name_zh,
            name_en,
            industry
        )
        VALUES
        (
            :ticker,
            :market,
            :name_zh,
            :name_en,
            :industry
        )
        ON CONFLICT (ticker, market)
        DO UPDATE SET
            name_zh = EXCLUDED.name_zh,
            industry = EXCLUDED.industry
    """)

    with engine.begin() as conn:
        conn.execute(
            sql,
            {
                "ticker": ticker,
                "market": market,
                "name_zh": name_zh,
                "name_en": name_en,
                "industry": industry
            }
        )