from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ClaimStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PAID = "PAID"


class ExpenseCategory(str, Enum):
    TRAVEL = "TRAVEL"
    MEALS = "MEALS"
    ACCOMMODATION = "ACCOMMODATION"
    OFFICE_SUPPLIES = "OFFICE_SUPPLIES"
    TAXI_LOCAL_TRANSPORT = "TAXI_LOCAL_TRANSPORT"
    CLIENT_EXPENSE = "CLIENT_EXPENSE"
    OTHER = "OTHER"


class DuplicateStatus(str, Enum):
    NONE = "NONE"
    POSSIBLE = "POSSIBLE"
    LIKELY = "LIKELY"


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    claim_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    merchant: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    expense_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="INR",
    )

    category: Mapped[ExpenseCategory] = mapped_column(
        SQLEnum(ExpenseCategory),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[ClaimStatus] = mapped_column(
        SQLEnum(ClaimStatus),
        nullable=False,
        default=ClaimStatus.DRAFT,
        index=True,
    )

    duplicate_status: Mapped[DuplicateStatus] = mapped_column(
        SQLEnum(DuplicateStatus),
        nullable=False,
        default=DuplicateStatus.NONE,
    )

    duplicate_of_claim_id: Mapped[int | None] = mapped_column(
        ForeignKey("claims.id"),
        nullable=True,
    )

    duplicate_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    rejected_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        backref="claims",
    )

    duplicate_of: Mapped["Claim | None"] = relationship(
        "Claim",
        remote_side=[id],
    )