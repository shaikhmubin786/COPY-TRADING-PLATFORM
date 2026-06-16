from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import ChildTrade
from schemas import (
    ChildTradeResponse,
    ChildTradeListResponse
)

router = APIRouter(
    prefix="/api/child-trades",
    tags=["Child Trades"]
)


@router.get("", response_model=ChildTradeListResponse)
def get_child_trades(
    db: Session = Depends(get_db)
):
    trades = db.query(ChildTrade).all()

    return {
        "child_trades": trades
    }