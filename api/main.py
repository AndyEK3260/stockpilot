from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.stock_api import router as stock_router
from api.diagnosis_api import router as diagnosis_router


app = FastAPI(
    title="StockPilot API",
    version="1.0"
)


# CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    stock_router,
    prefix="/api"
)

app.include_router(
    diagnosis_router,
    prefix="/api"
)


@app.get("/")
def home():
    return {
        "app": "StockPilot",
        "status": "running"
    }