import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)


from services.price_service import save_stock_prices


save_stock_prices("2330")