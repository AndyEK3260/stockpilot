import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)


from services.data_quality_service import check_price_quality


issues = check_price_quality(
    "2330"
)


print(
    issues
)