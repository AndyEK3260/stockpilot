import sys
from pathlib import Path

# 加入專案根目錄
sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.company_service import create_company


create_company(
    ticker="2330",
    market="TWSE",
    name_zh="台積電",
    name_en="TSMC",
    industry="Semiconductor"
)

print("完成")