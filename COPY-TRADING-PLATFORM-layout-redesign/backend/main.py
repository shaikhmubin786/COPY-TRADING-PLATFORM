from fastapi import FastAPI
from database import engine, Base

import models

from routers.accounts import router as account_router
from routers.mappings import router as mapping_router
from routers.trades import router as trade_router
from routers.child_trades import router as child_trade_router
from routers.logs import router as log_router
from routers.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Copy Trading Platform"


)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Accounts APIs
app.include_router(account_router)

# Mapping APIs
app.include_router(mapping_router)

# Trade APIs
app.include_router(trade_router)

# Child Trade APIs
app.include_router(child_trade_router)
app.include_router(log_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {
        "message": "API Running"
    }