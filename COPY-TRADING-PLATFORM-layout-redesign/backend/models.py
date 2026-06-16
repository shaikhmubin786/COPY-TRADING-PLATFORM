"""
models.py — SQLAlchemy ORM models for the Copy Trading Platform
"""

import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import (
    String, DateTime, Enum, UniqueConstraint, Text
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class BrokerEnum(str, PyEnum):
    ZERODHA = "Zerodha"
    ALICEBLUE = "AliceBlue"
    ZENAM = "Zenam"


class RoleEnum(str, PyEnum):
    MASTER = "Master"
    CHILD = "Child"


class StatusEnum(str, PyEnum):
    CONNECTED = "Connected"
    WARNING = "Warning"
    DISCONNECTED = "Disconnected"


class Account(Base):
    """
    Represents a broker trading account (master or child).
    API credentials are stored encrypted.
    """

    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    broker: Mapped[BrokerEnum] = mapped_column(
        Enum(BrokerEnum),
        nullable=False
    )

    client_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum),
        nullable=False,
        default=RoleEnum.CHILD
    )

    api_key: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    api_secret: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    access_token: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum),
        nullable=False,
        default=StatusEnum.DISCONNECTED
    )

    connection_info: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        default="Not connected"
    )

    session_status: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        default="Unknown"
    )

    last_sync: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint(
            "broker",
            "client_id",
            name="uq_broker_client_id"
        ),
    )

    def __repr__(self) -> str:
        return f"<Account {self.broker}:{self.client_id} [{self.status}]>"


class Mapping(Base):
    """
    Master ↔ Child mapping for copy trading
    """

    __tablename__ = "mappings"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    master_account_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False
    )

    child_account_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False
    )

    multiplier: Mapped[float] = mapped_column(
        nullable=False,
        default=1.0
    )

    is_active: Mapped[bool] = mapped_column(
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return (
            f"<Mapping Master={self.master_account_id} "
            f"Child={self.child_account_id} "
            f"Multiplier={self.multiplier}>"
        )

class Trade(Base):
    """
    Trade executed by Master Account
    """

    __tablename__ = "trades"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    master_account_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False
    )

    symbol: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    side: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return (
            f"<Trade {self.symbol} "
            f"{self.side} "
            f"Qty={self.quantity}>"
        )


class ChildTrade(Base):
    """
    Trade copied to child account
    """

    __tablename__ = "child_trades"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    trade_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False
    )

    child_account_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False
    )

    symbol: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    side: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    # status: Mapped[str] = mapped_column(
    # String(20),
    # nullable=False,
    # default="EXECUTED"
# )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return (
            f"<ChildTrade {self.symbol} "
            f"{self.side} "
            f"Qty={self.quantity}>"
        )

class TradeLog(Base):
    """
    Trade execution logs
    """

    __tablename__ = "trade_logs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    trade_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<TradeLog {self.trade_id}>"