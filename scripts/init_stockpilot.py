import sys
from pathlib import Path

# 將專案根目錄加入 Python 搜尋路徑
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, text
from config import DATABASE_URL

print("========== StockPilot ==========")
print("Connecting to PostgreSQL...")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    version = conn.execute(text("SELECT version();")).scalar()

print("✅ Connected!")
print(version)