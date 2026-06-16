from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import (
    Account,
    Mapping,
    Trade,
    ChildTrade
)

from schemas import DashboardResponse

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db)
):

    total_accounts = db.query(Account).count()

    total_mappings = db.query(Mapping).count()

    active_mappings = db.query(Mapping).filter(
        Mapping.is_active == True
    ).count()

    total_trades = db.query(Trade).count()

    total_child_trades = db.query(
        ChildTrade
    ).count()

    return {
        "total_accounts": total_accounts,
        "total_mappings": total_mappings,
        "active_mappings": active_mappings,
        "total_trades": total_trades,
        "total_child_trades": total_child_trades
    }