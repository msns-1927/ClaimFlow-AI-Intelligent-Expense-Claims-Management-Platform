from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ReviewAction(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ClaimReview(Base):
    __tablename__ = "claim_reviews"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    claim_id: Mapped[int] = mapped_column(
        ForeignKey("claims.id"),
        nullable=False,
        index=True,
    )

    reviewer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    action: Mapped[ReviewAction] = mapped_column(
        SQLEnum(ReviewAction),
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    claim: Mapped["Claim"] = relationship(
        "Claim",
        backref="reviews",
    )

    reviewer: Mapped["User"] = relationship(
        "User",
        backref="claim_reviews",
    )