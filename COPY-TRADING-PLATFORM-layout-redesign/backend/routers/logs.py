from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import TradeLog
from schemas import (
    TradeLogResponse,
    TradeLogListResponse
)

router = APIRouter(
    prefix="/api/logs",
    tags=["Logs"]
)


@router.get("", response_model=TradeLogListResponse)
def get_logs(
    db: Session = Depends(get_db)
):
    logs = db.query(TradeLog).all()

    return {
        "logs": logs
    }