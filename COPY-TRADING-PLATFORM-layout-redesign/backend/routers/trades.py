from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Trade, Mapping, ChildTrade, TradeLog
from schemas import (
    TradeCreate,
    TradeResponse,
    TradeListResponse
)

router = APIRouter(
    prefix="/api/trades",
    tags=["Trades"]
)


# Get All Trades
@router.get("", response_model=TradeListResponse)
def get_trades(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()
    return {"trades": trades}


# Get Trade By ID
@router.get("/{trade_id}", response_model=TradeResponse)
def get_trade_by_id(
    trade_id: str,
    db: Session = Depends(get_db)
):
    trade = db.query(Trade).filter(
        Trade.id == trade_id
    ).first()

    if not trade:
        raise HTTPException(
            status_code=404,
            detail="Trade not found"
        )

    return trade


# Create Trade
@router.post("", response_model=TradeResponse)
def create_trade(
    trade: TradeCreate,
    db: Session = Depends(get_db)
):
    # Save Master Trade
    db_trade = Trade(
        master_account_id=trade.master_account_id,
        symbol=trade.symbol,
        side=trade.side,
        quantity=trade.quantity,
        
    )

    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)

    # Log Master Trade
    master_log = TradeLog(
        trade_id=db_trade.id,
        message=f"Master Trade Created: {trade.symbol} {trade.side} Qty={trade.quantity}"
    )

    db.add(master_log)

    # Find Active Mappings
    mappings = db.query(Mapping).filter(
        Mapping.master_account_id == trade.master_account_id,
        Mapping.is_active == True
    ).all()

    # No Active Mapping
    if not mappings:
        skip_log = TradeLog(
            trade_id=db_trade.id,
            message="Copy Trading Skipped - No Active Mapping"
        )

        db.add(skip_log)

    # Create Child Trades
    for mapping in mappings:

        child_quantity = int(
            trade.quantity * mapping.multiplier
        )

        child_trade = ChildTrade(
            trade_id=db_trade.id,
            child_account_id=mapping.child_account_id,
            symbol=trade.symbol,
            side=trade.side,
            quantity=child_quantity
        )

        db.add(child_trade)

        child_log = TradeLog(
            trade_id=db_trade.id,
            message=f"Child Trade Created: {trade.symbol} {trade.side} Qty={child_quantity}"
        )

        db.add(child_log)

    db.commit()

    return db_trade


# Delete Trade
@router.delete("/{trade_id}")
def delete_trade(
    trade_id: str,
    db: Session = Depends(get_db)
):
    trade = db.query(Trade).filter(
        Trade.id == trade_id
    ).first()

    if not trade:
        raise HTTPException(
            status_code=404,
            detail="Trade not found"
        )

    db.delete(trade)
    db.commit()

    return {
        "message": "Trade deleted successfully"
    }