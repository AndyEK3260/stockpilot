import yfinance as yf
import pandas as pd

from sqlalchemy import text

from services.database import engine



def get_company_id(ticker):

    sql = text("""
        SELECT company_id
        FROM companies
        WHERE ticker = :ticker
        AND market = 'TWSE'
    """)

    with engine.connect() as conn:

        result = conn.execute(
            sql,
            {
                "ticker": ticker
            }
        ).fetchone()


    if result:
        return result[0]

    return None



def download_price(
    ticker,
    start_date="2020-01-01",
    end_date=None
):

    yf_symbol = f"{ticker}.TW"


    print(
        f"下載 {yf_symbol} 股價資料..."
    )


    df = yf.download(
        yf_symbol,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False
    )


    if df.empty:

        raise Exception(
            f"{ticker} 無股價資料"
        )


    # yfinance 新版 MultiIndex
    if isinstance(
        df.columns,
        pd.MultiIndex
    ):

        df.columns = (
            df.columns
            .droplevel(1)
        )


    df = df.reset_index()


    return df



def clean_price_data(df):


    required_columns = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Adj Close"
    ]


    for col in required_columns:

        if col not in df.columns:

            raise Exception(
                f"缺少欄位 {col}"
            )


    # 移除空值

    df = df.dropna()


    # 價格不能 <=0

    df = df[
        df["Close"] > 0
    ]


    return df



def save_stock_prices(
    ticker,
    start_date="2020-01-01"
):


    company_id = get_company_id(
        ticker
    )


    if company_id is None:

        raise Exception(
            f"{ticker} 不存在 companies"
        )


    df = download_price(
        ticker,
        start_date
    )


    df = clean_price_data(
        df
    )


    print(
        f"準備寫入 {len(df)} 筆資料"
    )


    sql = text("""
        INSERT INTO stock_prices
        (
            company_id,
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
            adjusted_close,
            adjustment_factor
        )

        VALUES

        (
            :company_id,
            :trade_date,
            :open_price,
            :high_price,
            :low_price,
            :close_price,
            :volume,
            :adjusted_close,
            1.0
        )


        ON CONFLICT
        (
            company_id,
            trade_date
        )

        DO UPDATE SET

        open_price = EXCLUDED.open_price,
        high_price = EXCLUDED.high_price,
        low_price = EXCLUDED.low_price,
        close_price = EXCLUDED.close_price,
        volume = EXCLUDED.volume,
        adjusted_close = EXCLUDED.adjusted_close

    """)


    with engine.begin() as conn:


        for _, row in df.iterrows():


            conn.execute(
                sql,
                {

                    "company_id":
                        company_id,


                    "trade_date":
                        row["Date"].date(),


                    "open_price":
                        float(row["Open"]),


                    "high_price":
                        float(row["High"]),


                    "low_price":
                        float(row["Low"]),


                    "close_price":
                        float(row["Close"]),


                    "volume":
                        int(row["Volume"]),


                    "adjusted_close":
                        float(row["Adj Close"])

                }
            )


    print(
        "✅ 股價資料寫入完成"
    )