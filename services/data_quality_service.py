import pandas as pd

from sqlalchemy import text

from services.database import engine



def load_stock_price_data(ticker):

    sql = text("""
        SELECT
            trade_date,
            close_price,
            volume
        FROM stock_prices s

        JOIN companies c
        ON s.company_id = c.company_id

        WHERE c.ticker = :ticker

        ORDER BY trade_date
    """)


    with engine.connect() as conn:

        df = pd.DataFrame(
            conn.execute(
                sql,
                {
                    "ticker": ticker
                }
            ).fetchall(),
            columns=[
                "trade_date",
                "close_price",
                "volume"
            ]
        )


    return df



def check_invalid_price(df):

    issues = []


    invalid_price = df[
        df["close_price"] <= 0
    ]


    for _, row in invalid_price.iterrows():

        issues.append(
            {
                "date": row["trade_date"],
                "type": "INVALID_PRICE",
                "value": row["close_price"]
            }
        )


    return issues



def check_volume(df):

    issues = []


    invalid_volume = df[
        df["volume"] <= 0
    ]


    for _, row in invalid_volume.iterrows():

        issues.append(
            {
                "date": row["trade_date"],
                "type": "WARNING_VOLUME_ZERO",
                "value": row["volume"]
            }
        )


    return issues



def check_price_change(df):

    issues = []


    df = df.copy()


    df["change_pct"] = (
        df["close_price"]
        .pct_change()
        * 100
    )


    abnormal = df[
        abs(df["change_pct"]) > 15
    ]


    for _, row in abnormal.iterrows():

        issues.append(
            {
                "date": row["trade_date"],
                "type": "WARNING_PRICE_CHANGE",
                "value": round(
                    row["change_pct"],
                    2
                )
            }
        )


    return issues



def check_price_quality(ticker):

    print(
        f"Checking data quality: {ticker}"
    )


    df = load_stock_price_data(
        ticker
    )


    issues = []


    # 1. 價格檢查
    issues.extend(
        check_invalid_price(df)
    )


    # 2. 成交量檢查
    issues.extend(
        check_volume(df)
    )


    # 3. 漲跌幅檢查
    issues.extend(
        check_price_change(df)
    )


    return issues