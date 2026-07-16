import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import pandas as pd

from services.indicator_service import (
    calculate_indicators,
    save_indicators
)
from services.scoring_service import calculate_investment_score
from services.score_service import save_stock_score
from services.exceptions import StockPilotError


def run_one(ticker):

    print(
        f"\n========== {ticker} =========="
    )

    # 1. 計算技術指標
    df = calculate_indicators(ticker)

    # 2. 存指標
    save_indicators(ticker, df)

    # 3. 用最新一筆指標算分數
    latest = df.iloc[-1]

    required = ["MA_5", "MA_20", "MA_60", "RSI_14", "MACD"]

    if latest[required].isna().any():

        raise StockPilotError(
            f"{ticker} 最新一筆資料的技術指標尚不完整"
            "（資料筆數可能不足以計算 MA_60），無法評分"
        )

    score_data = calculate_investment_score(
        float(latest["MA_5"]),
        float(latest["MA_20"]),
        float(latest["MA_60"]),
        float(latest["RSI_14"]),
        float(latest["MACD"])
    )

    print(score_data)

    # 4. 存分數
    save_stock_score(ticker, score_data)


def main(tickers):

    if not tickers:

        print("用法：python scripts/run_score_batch.py 2330 [2317 ...]")
        return

    failed = []

    for ticker in tickers:

        try:

            run_one(ticker)

        except Exception as e:

            print(
                f"❌ {ticker} 評分失敗：{e}"
            )

            failed.append(ticker)

    print(
        f"\n批次完成。成功 {len(tickers) - len(failed)} / {len(tickers)}"
    )

    if failed:

        print(
            f"失敗的 ticker：{failed}"
        )


if __name__ == "__main__":

    main(sys.argv[1:])
