import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)


from services.indicator_service import (
    calculate_indicators,
    save_indicators
)


df = calculate_indicators(
    "2330"
)


save_indicators(
    "2330",
    df
)


print(df.tail())