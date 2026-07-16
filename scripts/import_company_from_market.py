import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent)
)

from services.symbol_service import get_symbol_info
from services.market_data_service import get_company_info
from services.company_service import create_company


ticker_input = "2330"

symbol = get_symbol_info(ticker_input)

company = get_company_info(
    ticker_input + ".TW"
)

create_company(
    ticker=company["ticker"],
    market=symbol["market"],
    name_zh=symbol["name_zh"],
    name_en=company["name"],
    industry=company["industry"]
)

print("完成")
