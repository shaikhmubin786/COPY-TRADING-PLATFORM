"""
schemas.py — Pydantic schemas for request validation and response serialization
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ValidationInfo
from models import BrokerEnum, RoleEnum, StatusEnum


# ─────────────────────────────────────────────────────────────────────────────
#  Request Schemas (what the frontend sends)
# ─────────────────────────────────────────────────────────────────────────────

class AccountCreate(BaseModel):
    """Body for POST /api/accounts — creating a new account."""
    broker:       BrokerEnum = Field(..., description="Broker name: Zerodha | AliceBlue | Zenam")
    client_id:    str        = Field(..., min_length=1, max_length=100)
    name:         str        = Field(..., min_length=1, max_length=200)
    role:         RoleEnum   = Field(default=RoleEnum.CHILD)
    api_key:      Optional[str] = Field(None, description="Broker API key")
    api_secret:   Optional[str] = Field(None, description="Broker API secret")
    access_token: Optional[str] = Field(None, description="Broker access token")


class AccountUpdate(BaseModel):
    """Body for PUT /api/accounts/{id} — partial update (all fields optional)."""
    broker:       Optional[BrokerEnum] = None
    client_id:    Optional[str]        = Field(None, min_length=1, max_length=100)
    name:         Optional[str]        = Field(None, min_length=1, max_length=200)
    role:         Optional[RoleEnum]   = None
    api_key:      Optional[str]        = None
    api_secret:   Optional[str]        = None
    access_token: Optional[str]        = None


class ValidateRequest(BaseModel):
    """Body for POST /api/accounts/validate."""
    broker:       BrokerEnum
    api_key:      str
    api_secret:   str
    access_token: Optional[str] = None


class RefreshSessionRequest(BaseModel):
    """Body for POST /api/accounts/refresh-session."""
    account_ids: Optional[List[UUID]] = Field(
        None,
        description="Specific account IDs to refresh. If omitted, all Warning/Disconnected accounts are refreshed.",
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Response Schemas (what the frontend receives)
# ─────────────────────────────────────────────────────────────────────────────

class AccountResponse(BaseModel):
    """
    Full account record returned to the frontend.
    NOTE: Raw API credentials are NEVER returned — only masked previews.
    """
    id:              UUID
    broker:          BrokerEnum
    client_id:       str
    name:            str
    role:            RoleEnum
    status:          StatusEnum
    connection_info: Optional[str]
    session_status:  Optional[str]
    last_sync:       Optional[datetime]
    created_at:      datetime
    updated_at:      datetime

    # Derived UI helpers
    short:      str = ""   # first letter of broker, e.g. "Z"
    status_class: str = "" # CSS class string for the badge

    @field_validator("short", mode="before")
    @classmethod
    def compute_short(cls, v: str, info: ValidationInfo) -> str:
        broker = info.data.get("broker", "")
        return str(broker)[0].upper() if broker else "?"

    @field_validator("status_class", mode="before")
    @classmethod
    def compute_status_class(cls, v: str, info: ValidationInfo) -> str:
        status = info.data.get("status", "")
        mapping = {
            "Connected":    "connected",
            "Warning":      "warning",
            "Disconnected": "disconnected",
        }
        return mapping.get(str(status), "disconnected")

    model_config = {"from_attributes": True}


class AccountSummaryResponse(BaseModel):
    """Summary counts shown in the 4 top cards."""
    total:        int
    connected:    int
    warning:      int
    disconnected: int


class AccountListResponse(BaseModel):
    """Combined response for GET /api/accounts."""
    summary:  AccountSummaryResponse
    accounts: List[AccountResponse]


class ValidateResponse(BaseModel):
    """Response for credential validation."""
    valid:   bool
    message: str


class ConnectResponse(BaseModel):
    """Response for connect / test connection."""
    success:          bool
    status:           StatusEnum
    connection_info:  str
    session_status:   str
    message:          str


class RefreshSessionResponse(BaseModel):
    """Response for refresh-session."""
    refreshed: List[UUID]
    failed:    List[UUID]
    message:   str


class MessageResponse(BaseModel):
    """Generic success/error message."""
    message: str

# ─────────────────────────────────────────────────────────────────────────────
# Mapping Schemas
# ─────────────────────────────────────────────────────────────────────────────

class MappingCreate(BaseModel):
    master_account_id: str
    child_account_id: str
    multiplier: float = 1.0

class MappingUpdate(BaseModel):
    multiplier: float


class MappingResponse(BaseModel):
    id: str
    master_account_id: str
    child_account_id: str
    multiplier: float
    is_active: bool

    model_config = {"from_attributes": True}


class MappingListResponse(BaseModel):
    mappings: List[MappingResponse]
    # ─────────────────────────────────────────────────────────────────────────────
# Trade Schemas
# ─────────────────────────────────────────────────────────────────────────────

class TradeCreate(BaseModel):
    master_account_id: str
    symbol: str
    side: str
    quantity: int


class TradeResponse(BaseModel):
    id: str
    master_account_id: str
    symbol: str
    side: str
    quantity: int
    status: str = "EXECUTED"

    model_config = {"from_attributes": True}



class TradeListResponse(BaseModel):
    trades: List[TradeResponse]


class ChildTradeResponse(BaseModel):
    id: str
    trade_id: str
    child_account_id: str
    symbol: str
    side: str
    quantity: int

    model_config = {"from_attributes": True}


class ChildTradeListResponse(BaseModel):
    child_trades: List[ChildTradeResponse]

# ─────────────────────────────────────────────────────────────────────────────
# Trade Log Schemas
# ─────────────────────────────────────────────────────────────────────────────

class TradeLogResponse(BaseModel):
    id: str
    trade_id: str
    message: str

    model_config = {"from_attributes": True}


class TradeLogListResponse(BaseModel):
    logs: List[TradeLogResponse]

# Dashboard Schema

class DashboardResponse(BaseModel):
    total_accounts: int
    total_mappings: int
    active_mappings: int
    total_trades: int
    total_child_trades: int