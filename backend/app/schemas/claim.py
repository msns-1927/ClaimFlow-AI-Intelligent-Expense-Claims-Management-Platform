from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import ExpenseCategory


class ClaimCreate(BaseModel):
    merchant: str = Field(min_length=1, max_length=150)
    expense_date: datetime
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    category: ExpenseCategory
    description: str = Field(min_length=1)


class ClaimUpdate(BaseModel):
    merchant: str = Field(min_length=1, max_length=150)
    expense_date: datetime
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    category: ExpenseCategory
    description: str = Field(min_length=1)


class ClaimResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    claim_number: str
    user_id: int
    merchant: str
    expense_date: datetime
    amount: Decimal
    currency: str
    category: ExpenseCategory
    description: str
    status: str
    duplicate_status: str
    duplicate_of_claim_id: int | None
    duplicate_score: Decimal | None
    submitted_at: datetime | None
    approved_at: datetime | None
    rejected_at: datetime | None
    paid_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ReceiptTextRequest(BaseModel):
    raw_text: str = Field(min_length=3)


class ClaimReviewRequest(BaseModel):
    comment: str | None = Field(
        default=None,
        max_length=1000,
    )

class CategorySpend(BaseModel):
    category: str
    amount: Decimal


class EmployeeSpend(BaseModel):
    user_id: int
    employee_name: str
    monthly_limit: Decimal | None
    total_spent: Decimal
    remaining_limit: Decimal | None
    limit_status: str


class FinanceDashboardResponse(BaseModel):
    month: str
    total_spend: Decimal
    category_spend: list[CategorySpend]
    employee_spend: list[EmployeeSpend]


class ManagerClaimResponse(ClaimResponse):
    employee_name: str