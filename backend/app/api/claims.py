from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.dependencies import get_current_user, require_role
from app.database.session import get_db
from app.models import (
    AuditLog,
    Claim,
    ClaimReview,
    ClaimStatus,
    DuplicateStatus,
    Receipt,
    ReviewAction,
    User,
    UserRole,
)
from app.schemas.claim import (
    ClaimCreate,
    ClaimResponse,
    ClaimUpdate,
    CategorySpend,
    ReceiptTextRequest,
    ClaimReviewRequest,
    FinanceDashboardResponse,
    ManagerClaimResponse,
    EmployeeSpend,
)
from app.services.duplicate_detector import (
    calculate_text_hash,
    detect_duplicate,
    normalize_receipt_text,
)
from app.services.receipt_extractor import extract_receipt_data


router = APIRouter(
    prefix="/api/claims",
    tags=["Claims"],
)


def generate_claim_number(claim_id: int) -> str:
    return f"CLM-{datetime.utcnow().strftime('%Y%m')}-{claim_id:05d}"


@router.post(
    "",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_claim(
    data: ClaimCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    claim = Claim(
        claim_number="TEMP",
        user_id=current_user.id,
        merchant=data.merchant,
        expense_date=data.expense_date,
        amount=data.amount,
        currency=data.currency.upper(),
        category=data.category,
        description=data.description,
        status=ClaimStatus.DRAFT,
        duplicate_status=DuplicateStatus.NONE,
    )

    db.add(claim)
    db.flush()

    claim.claim_number = generate_claim_number(claim.id)

    db.commit()
    db.refresh(claim)

    return claim


@router.post(
    "/from-receipt",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_claim_from_receipt(
    data: ReceiptTextRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    extracted = extract_receipt_data(data.raw_text)

    expense_date = datetime.fromisoformat(
        extracted["expense_date"]
    )

    normalized_text = normalize_receipt_text(
        data.raw_text
    )

    text_hash = calculate_text_hash(
        normalized_text
    )

    duplicate = detect_duplicate(
        db=db,
        merchant=extracted["merchant"],
        expense_date=expense_date,
        amount=extracted["amount"],
        normalized_text=normalized_text,
        current_claim_id=None,
    )

    claim = Claim(
        claim_number="TEMP",
        user_id=current_user.id,
        merchant=extracted["merchant"],
        expense_date=expense_date,
        amount=extracted["amount"],
        currency=extracted.get("currency", "INR").upper(),
        category=extracted["category"],
        description=extracted["description"],
        status=ClaimStatus.DRAFT,
        duplicate_status=duplicate["status"],
        duplicate_of_claim_id=duplicate["claim_id"],
        duplicate_score=duplicate["score"],
    )

    db.add(claim)
    db.flush()

    claim.claim_number = generate_claim_number(claim.id)

    receipt = Receipt(
        claim_id=claim.id,
        raw_text=data.raw_text,
        extracted_data=extracted,
        extraction_confidence=extracted.get("confidence"),
        normalized_text=normalized_text,
        text_hash=text_hash,
    )

    db.add(receipt)

    db.commit()
    db.refresh(claim)

    return claim

# Get my claims
@router.get(
    "/my",
    response_model=list[ClaimResponse],
)
def get_my_claims(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    claims = (
        db.query(Claim)
        .filter(Claim.user_id == current_user.id)
        .order_by(Claim.created_at.desc())
        .all()
    )

    return claims

# Update a draft
@router.put(
    "/{claim_id}",
    response_model=ClaimResponse,
)
def update_claim(
    claim_id: int,
    data: ClaimUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    claim = db.get(Claim, claim_id)

    if claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )

    if claim.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own claims",
        )

    if claim.status != ClaimStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft claims can be edited",
        )

    claim.merchant = data.merchant
    claim.expense_date = data.expense_date
    claim.amount = data.amount
    claim.currency = data.currency.upper()
    claim.category = data.category
    claim.description = data.description

    db.commit()
    db.refresh(claim)

    return claim


# Submit a claim
@router.post(
    "/{claim_id}/submit",
    response_model=ClaimResponse,
)
def submit_claim(
    claim_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    claim = db.get(Claim, claim_id)

    if claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )

    if claim.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only submit your own claims",
        )

    if claim.status != ClaimStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft claims can be submitted",
        )

    claim.status = ClaimStatus.SUBMITTED
    claim.submitted_at = datetime.utcnow()

    db.commit()
    db.refresh(claim)

    return claim


# Team endpoint
@router.get(
    "/team",
    response_model=list[ManagerClaimResponse],
)
def get_team_claims(
    current_user: User = Depends(
        require_role(UserRole.MANAGER)
    ),
    db: Session = Depends(get_db),
):
    results = (
        db.query(Claim, User.name)
        .join(User, Claim.user_id == User.id)
        .filter(
            User.manager_id == current_user.id,
            Claim.status == ClaimStatus.SUBMITTED,
        )
        .order_by(Claim.submitted_at.asc())
        .all()
    )

    response = []

    for claim, employee_name in results:
        response.append(
            ManagerClaimResponse(
                id=claim.id,
                claim_number=claim.claim_number,
                user_id=claim.user_id,
                merchant=claim.merchant,
                expense_date=claim.expense_date,
                amount=claim.amount,
                currency=claim.currency,
                category=claim.category,
                description=claim.description,
                status=claim.status,
                duplicate_status=claim.duplicate_status,
                duplicate_of_claim_id=claim.duplicate_of_claim_id,
                duplicate_score=claim.duplicate_score,
                submitted_at=claim.submitted_at,
                approved_at=claim.approved_at,
                rejected_at=claim.rejected_at,
                paid_at=claim.paid_at,
                created_at=claim.created_at,
                updated_at=claim.updated_at,
                employee_name=employee_name,
            )
        )

    return response


# Approve endpoint
@router.post(
    "/{claim_id}/approve",
    response_model=ClaimResponse,
)
def approve_claim(
    claim_id: int,
    data: ClaimReviewRequest,
    current_user: User = Depends(
        require_role(UserRole.MANAGER)
    ),
    db: Session = Depends(get_db),
):
    claim = db.get(Claim, claim_id)

    if claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )

    # Manager cannot approve their own claim.
    if claim.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot approve your own claim",
        )

    # Find the employee who submitted the claim.
    employee = db.get(User, claim.user_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim owner not found",
        )

    # Manager can only review their direct team's claims.
    if employee.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only review claims from your team",
        )

    if claim.status != ClaimStatus.SUBMITTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only submitted claims can be approved",
        )

    old_status = claim.status.value

    claim.status = ClaimStatus.APPROVED
    claim.approved_at = datetime.utcnow()

    review = ClaimReview(
        claim_id=claim.id,
        reviewer_id=current_user.id,
        action=ReviewAction.APPROVED,
        comment=data.comment,
    )

    audit = AuditLog(
        claim_id=claim.id,
        actor_id=current_user.id,
        event_type="CLAIM_APPROVED",
        old_value=old_status,
        new_value=ClaimStatus.APPROVED.value,
    )

    db.add(review)
    db.add(audit)

    db.commit()
    db.refresh(claim)

    return claim


# Reject endpoint
@router.post(
    "/{claim_id}/reject",
    response_model=ClaimResponse,
)
def reject_claim(
    claim_id: int,
    data: ClaimReviewRequest,
    current_user: User = Depends(
        require_role(UserRole.MANAGER)
    ),
    db: Session = Depends(get_db),
):
    claim = db.get(Claim, claim_id)

    if claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )

    # Manager cannot review their own claim.
    if claim.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot reject your own claim",
        )

    employee = db.get(User, claim.user_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim owner not found",
        )

    # Manager can only review their direct team's claims.
    if employee.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only review claims from your team",
        )

    if claim.status != ClaimStatus.SUBMITTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only submitted claims can be rejected",
        )

    old_status = claim.status.value

    claim.status = ClaimStatus.REJECTED
    claim.rejected_at = datetime.utcnow()

    review = ClaimReview(
        claim_id=claim.id,
        reviewer_id=current_user.id,
        action=ReviewAction.REJECTED,
        comment=data.comment,
    )

    audit = AuditLog(
        claim_id=claim.id,
        actor_id=current_user.id,
        event_type="CLAIM_REJECTED",
        old_value=old_status,
        new_value=ClaimStatus.REJECTED.value,
    )

    db.add(review)
    db.add(audit)

    db.commit()
    db.refresh(claim)

    return claim

# Finanace endpoint
@router.get(
    "/finance/pending",
    response_model=list[ClaimResponse],
)
def get_finance_pending_claims(
    current_user: User = Depends(
        require_role(UserRole.FINANCE)
    ),
    db: Session = Depends(get_db),
):
    claims = (
        db.query(Claim)
        .filter(Claim.status == ClaimStatus.APPROVED)
        .order_by(Claim.approved_at.asc())
        .all()
    )

    return claims


# Finance dashboard
@router.get(
    "/finance/dashboard",
    response_model=FinanceDashboardResponse,
)
def get_finance_dashboard(
    current_user: User = Depends(
        require_role(UserRole.FINANCE)
    ),
    db: Session = Depends(get_db),
):
    now = datetime.utcnow()

    month_start = datetime(
        now.year,
        now.month,
        1,
    )

    last_day = monthrange(
        now.year,
        now.month,
    )[1]

    month_end = datetime(
        now.year,
        now.month,
        last_day,
        23,
        59,
        59,
    )

    # Only PAID claims count toward actual monthly spend.
    claims = (
        db.query(Claim)
        .filter(
            Claim.status == ClaimStatus.PAID,
            Claim.expense_date >= month_start,
            Claim.expense_date <= month_end,
        )
        .all()
    )

    total_spend = sum(
        (claim.amount for claim in claims),
        Decimal("0"),
    )

    category_totals: dict[str, Decimal] = {}

    employee_totals: dict[int, Decimal] = {}

    for claim in claims:
        category = claim.category.value

        category_totals[category] = (
            category_totals.get(category, Decimal("0"))
            + claim.amount
        )

        employee_totals[claim.user_id] = (
            employee_totals.get(
                claim.user_id,
                Decimal("0"),
            )
            + claim.amount
        )

    category_spend = [
        CategorySpend(
            category=category,
            amount=amount,
        )
        for category, amount in sorted(
            category_totals.items()
        )
    ]

    users = (
        db.query(User)
        .filter(User.role != UserRole.FINANCE)
        .order_by(User.name.asc())
        .all()
    )

    employee_spend = []

    for user in users:
        total = employee_totals.get(
            user.id,
            Decimal("0"),
        )

        monthly_limit = (
            Decimal(str(user.monthly_limit))
            if user.monthly_limit is not None
            else None
        )

        remaining_limit = None

        if monthly_limit is not None:
            remaining_limit = (
                monthly_limit - total
            )

            if total > monthly_limit:
                limit_status = "EXCEEDED"
            elif total >= monthly_limit * Decimal("0.80"):
                limit_status = "NEAR_LIMIT"
            else:
                limit_status = "WITHIN_LIMIT"
        else:
            limit_status = "NO_LIMIT"

        employee_spend.append(
            EmployeeSpend(
                user_id=user.id,
                employee_name=user.name,
                monthly_limit=monthly_limit,
                total_spent=total,
                remaining_limit=remaining_limit,
                limit_status=limit_status,
            )
        )

    return FinanceDashboardResponse(
        month=f"{now.year}-{now.month:02d}",
        total_spend=total_spend,
        category_spend=category_spend,
        employee_spend=employee_spend,
    )


# Payment endpoint
@router.post(
    "/{claim_id}/pay",
    response_model=ClaimResponse,
)
def pay_claim(
    claim_id: int,
    current_user: User = Depends(
        require_role(UserRole.FINANCE)
    ),
    db: Session = Depends(get_db),
):
    claim = db.get(Claim, claim_id)

    if claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )

    if claim.status != ClaimStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only approved claims can be paid",
        )

    old_status = claim.status.value

    claim.status = ClaimStatus.PAID
    claim.paid_at = datetime.utcnow()

    audit = AuditLog(
        claim_id=claim.id,
        actor_id=current_user.id,
        event_type="CLAIM_PAID",
        old_value=old_status,
        new_value=ClaimStatus.PAID.value,
    )

    db.add(audit)

    db.commit()
    db.refresh(claim)

    return claim