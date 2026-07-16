import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine
from config.config import DATABASE_URL

engine = create_engine(DATABASE_URL)