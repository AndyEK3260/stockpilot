import pandas as pd
import ta
from config.indicator_mapping import INDICATOR_MAPPING
from sqlalchemy import text
from services.database import engine
from config.indicator_mapping import INDICATOR_MAPPING



def get_price_data(ticker):

    sql = text("""
        SELECT
            s.trade_date,
            s.close_price,
            s.volume
        FROM stock_prices s

        JOIN companies c
        ON s.company_id = c.company_id

        WHERE c.ticker = :ticker

        ORDER BY s.trade_date
    """)


    with engine.connect() as conn:

        result = conn.execute(
            sql,
            {
                "ticker": ticker
            }
        )


        df = pd.DataFrame(
            result.fetchall(),
            columns=result.keys()
        )


    return df



def calculate_indicators(ticker):


    df = get_price_data(ticker)


    if df.empty:

        raise Exception(
            "沒有股票資料"
        )


    print(
        f"讀取 {len(df)} 筆價格"
    )


    # MA

    df["MA_5"] = (
        df["close_price"]
        .rolling(5)
        .mean()
    )


    df["MA_20"] = (
        df["close_price"]
        .rolling(20)
        .mean()
    )


    df["MA_60"] = (
        df["close_price"]
        .rolling(60)
        .mean()
    )


    # RSI

    df["RSI_14"] = (
        ta.momentum
        .RSIIndicator(
            df["close_price"],
            window=14
        )
        .rsi()
    )


    # MACD

    macd = ta.trend.MACD(
        df["close_price"]
    )


    df["MACD"] = (
        macd.macd()
    )


    return df

def save_indicators(ticker, df):

    company_sql = text("""
        SELECT company_id
        FROM companies
        WHERE ticker = :ticker
    """)


    with engine.connect() as conn:

        company_id = conn.execute(
            company_sql,
            {
                "ticker": ticker
            }
        ).scalar()


    if not company_id:
        raise Exception(
            f"{ticker} 不存在"
        )


    indicator_columns = {

        "RSI_14": "RSI_14",

        "MACD": "MACD",

        "MA_5": "MA_5",

        "MA_20": "MA_20",

        "MA_60": "MA_60"
    }


    insert_sql = text("""
        INSERT INTO indicator_values
        (
            indicator_id,
            company_id,
            trade_date,
            value
        )

        VALUES
        (
            :indicator_id,
            :company_id,
            :trade_date,
            :value
        )


        ON CONFLICT
        (
            indicator_id,
            company_id,
            trade_date
        )

        DO UPDATE SET

        value = EXCLUDED.value

    """)



    total = 0


    with engine.begin() as conn:


        for indicator_code, column in indicator_columns.items():


            indicator_id = INDICATOR_MAPPING[indicator_code]


            for _, row in df.iterrows():


                value = row[column]


                if pd.isna(value):
                    continue


                conn.execute(
                    insert_sql,
                    {

                        "indicator_id":
                            indicator_id,


                        "company_id":
                            company_id,


                        "trade_date":
                            row["trade_date"],


                        "value":
                            float(value)

                    }
                )


                total += 1


    print(
        f"✅ 寫入 {total} 筆 indicator values"
    )