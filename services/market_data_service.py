import yfinance as yf


def get_company_info(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "ticker": ticker.split(".")[0],
        "name": info.get("longName"),
        "industry": info.get("industry")
    }


if __name__ == "__main__":

    company = get_company_info("2330.TW")

    print(company)