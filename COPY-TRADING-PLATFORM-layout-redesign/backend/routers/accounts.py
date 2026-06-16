"""
accounts.py — API routes for managing broker accounts
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone

from database import get_db
from models import Account, StatusEnum
from schemas import (
    AccountCreate, AccountUpdate, AccountResponse, AccountListResponse,
    AccountSummaryResponse, ValidateRequest, ValidateResponse,
    ConnectResponse, RefreshSessionRequest, RefreshSessionResponse, MessageResponse
)
from services import broker_service

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


@router.get("", response_model=AccountListResponse)
def get_all_accounts(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    status_filter: Optional[StatusEnum] = Query(None, alias="status")
):
    """Fetch all accounts and summary counts."""
    # Summary counts should reflect all accounts
    all_accounts = db.query(Account).all()
    
    total = len(all_accounts)
    connected = sum(1 for a in all_accounts if a.status == StatusEnum.CONNECTED)
    warning = sum(1 for a in all_accounts if a.status == StatusEnum.WARNING)
    disconnected = sum(1 for a in all_accounts if a.status == StatusEnum.DISCONNECTED)
    
    summary = AccountSummaryResponse(
        total=total,
        connected=connected,
        warning=warning,
        disconnected=disconnected
    )

    query = db.query(Account)
    if search:
        query = query.filter(
            or_(
                Account.client_id.ilike(f"%{search}%"),
                Account.name.ilike(f"%{search}%")
            )
        )
    if status_filter:
        query = query.filter(Account.status == status_filter)
        
    accounts = query.all()
    
    return {"summary": summary, "accounts": accounts}


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account_in: AccountCreate, db: Session = Depends(get_db)):
    """Create a new broker account."""
    # Check for duplicate client ID for this broker
    existing = db.query(Account).filter(
        Account.broker == account_in.broker,
        Account.client_id == account_in.client_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account with Client ID {account_in.client_id} already exists for {account_in.broker.value}."
        )

    # Encrypt credentials before saving
    db_account = Account(
        broker=account_in.broker,
        client_id=account_in.client_id,
        name=account_in.name,
        role=account_in.role,
        api_key=broker_service.encrypt_secret(account_in.api_key),
        api_secret=broker_service.encrypt_secret(account_in.api_secret),
        access_token=broker_service.encrypt_secret(account_in.access_token),
    )
    
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.put("/{account_id}")
def update_account(account_id: str, account_in: AccountUpdate, db: Session = Depends(get_db)):
    """Update an existing account."""
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Update fields if provided
    update_data = account_in.model_dump(exclude_unset=True)
    
    # Check uniqueness if broker or client_id are being changed
    new_broker = update_data.get("broker", db_account.broker)
    new_client_id = update_data.get("client_id", db_account.client_id)
    if new_broker != db_account.broker or new_client_id != db_account.client_id:
        existing = db.query(Account).filter(
            Account.broker == new_broker,
            Account.client_id == new_client_id,
            Account.id != account_id
        ).first()
        if existing:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Another account with Client ID {new_client_id} already exists for {new_broker.value}."
            )

    for field, value in update_data.items():
        if field in ["api_key", "api_secret", "access_token"] and value is not None:
             setattr(db_account, field, broker_service.encrypt_secret(value))
        else:
             setattr(db_account, field, value)

    db.commit()
    db.refresh(db_account)
    return db_account


@router.delete("/{account_id}")
def delete_account(account_id: str, db: Session = Depends(get_db)):
    """Delete an account."""
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    db.delete(db_account)
    db.commit()
    return MessageResponse(message="Account deleted successfully")


@router.post("/validate", response_model=ValidateResponse)
async def validate_credentials(req: ValidateRequest):
    """Validate credentials without saving."""
    is_valid, msg = await broker_service.validate_credentials(
        req.broker, req.api_key, req.api_secret, req.access_token
    )
    return ValidateResponse(valid=is_valid, message=msg)


@router.post("/{account_id}/connect", response_model=ConnectResponse)
async def connect_account(account_id: UUID, db: Session = Depends(get_db)):
    """Test connection for a saved account."""
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    api_key = broker_service.decrypt_secret(db_account.api_key)
    api_secret = broker_service.decrypt_secret(db_account.api_secret)
    access_token = broker_service.decrypt_secret(db_account.access_token)
    
    # In a real app, you'd handle missing keys before passing to service
    if not api_key or not api_secret:
         raise HTTPException(status_code=400, detail="Missing API credentials")

    success, conn_info, session_status, msg = await broker_service.test_connection(
         db_account.broker, api_key, api_secret, access_token
    )
    
    # Update DB state
    db_account.status = StatusEnum.CONNECTED if success else StatusEnum.DISCONNECTED
    # Just an example logic for warning
    if "Warning" in msg or session_status == "Refresh Needed":
        db_account.status = StatusEnum.WARNING
        
    db_account.connection_info = conn_info
    db_account.session_status = session_status
    if success:
         db_account.last_sync = datetime.now(timezone.utc)
         
    db.commit()
    
    return ConnectResponse(
        success=success,
        status=db_account.status,
        connection_info=conn_info,
        session_status=session_status,
        message=msg
    )


@router.post("/refresh-session", response_model=RefreshSessionResponse)
async def refresh_session(req: RefreshSessionRequest, db: Session = Depends(get_db)):
    """Refresh session tokens."""
    query = db.query(Account)
    if req.account_ids:
        query = query.filter(Account.id.in_(req.account_ids))
    else:
        # If no specific IDs provided, refresh all that aren't fully connected
        query = query.filter(Account.status != StatusEnum.CONNECTED)
        
    accounts_to_refresh = query.all()
    
    refreshed_ids = []
    failed_ids = []
    
    for account in accounts_to_refresh:
        api_key = broker_service.decrypt_secret(account.api_key)
        api_secret = broker_service.decrypt_secret(account.api_secret)
        access_token = broker_service.decrypt_secret(account.access_token)
        
        if not api_key or not api_secret:
             failed_ids.append(account.id)
             continue
             
        success, msg, new_token = await broker_service.refresh_session(
             account.broker, api_key, api_secret, access_token
        )
        
        if success:
            if new_token:
                account.access_token = broker_service.encrypt_secret(new_token)
            account.session_status = "Valid"
            # we might want to automatically run the connection test here too
            account.status = StatusEnum.CONNECTED # Optimistic update
            refreshed_ids.append(account.id)
        else:
            account.session_status = "Refresh Failed"
            account.status = StatusEnum.DISCONNECTED
            failed_ids.append(account.id)
            
    db.commit()
    
    return {
        "refreshed": [a.id for a in accounts_to_refresh if a.id in refreshed_ids],
        "failed": [a.id for a in accounts_to_refresh if a.id in failed_ids],
        "message": f"Refreshed {len(refreshed_ids)}, Failed {len(failed_ids)}"
    }
