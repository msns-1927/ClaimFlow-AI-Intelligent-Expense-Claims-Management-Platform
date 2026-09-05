from datetime import datetime
from decimal import Decimal

from app.core.security import hash_password
from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import (
    AuditLog,
    Claim,
    ClaimReview,
    ClaimStatus,
    DuplicateStatus,
    ExpenseCategory,
    Receipt,
    ReviewAction,
    User,
    UserRole,
)
from app.services.duplicate_detector import (
    calculate_text_hash,
    normalize_receipt_text,
)


def seed_users(db):
    existing_users = db.query(User).count()

    if existing_users > 0:
        print("Users already exist. Skipping user seed.")
        return

    # Senior manager
    senior_manager = User(
        name="Anita Rao",
        email="anita.rao@example.com",
        password_hash=hash_password("Anita@123"),
        role=UserRole.MANAGER,
        department="Engineering",
        monthly_limit=Decimal("100000.00"),
    )

    # Managers
    manager1 = User(
        name="Rahul Mehta",
        email="rahul.mehta@example.com",
        password_hash=hash_password("Rahul@123"),
        role=UserRole.MANAGER,
        department="Engineering",
        monthly_limit=Decimal("60000.00"),
    )

    manager2 = User(
        name="Priya Sharma",
        email="priya.sharma@example.com",
        password_hash=hash_password("Priya@123"),
        role=UserRole.MANAGER,
        department="Sales",
        monthly_limit=Decimal("60000.00"),
    )

    db.add_all([
        senior_manager,
        manager1,
        manager2,
    ])

    db.flush()

    # Employees reporting to Rahul
    employees = [
        User(
            name="Arjun Kumar",
            email="arjun.kumar@example.com",
            password_hash=hash_password("Arjun@123"),
            role=UserRole.EMPLOYEE,
            manager_id=manager1.id,
            department="Engineering",
            monthly_limit=Decimal("30000.00"),
        ),
        User(
            name="Neha Reddy",
            email="neha.reddy@example.com",
            password_hash=hash_password("Neha@123"),
            role=UserRole.EMPLOYEE,
            manager_id=manager1.id,
            department="Engineering",
            monthly_limit=Decimal("30000.00"),
        ),
        User(
            name="Vikram Singh",
            email="vikram.singh@example.com",
            password_hash=hash_password("Vikram@123"),
            role=UserRole.EMPLOYEE,
            manager_id=manager1.id,
            department="Engineering",
            monthly_limit=Decimal("30000.00"),
        ),
    ]

    # Employees reporting to Priya
    employees.extend([
        User(
            name="Sneha Patel",
            email="sneha.patel@example.com",
            password_hash=hash_password("Sneha@123"),
            role=UserRole.EMPLOYEE,
            manager_id=manager2.id,
            department="Sales",
            monthly_limit=Decimal("30000.00"),
        ),
        User(
            name="Kiran Das",
            email="kiran.das@example.com",
            password_hash=hash_password("Kiran@123"),
            role=UserRole.EMPLOYEE,
            manager_id=manager2.id,
            department="Sales",
            monthly_limit=Decimal("30000.00"),
        ),
        User(
            name="Meera Iyer",
            email="meera.iyer@example.com",
            password_hash=hash_password("Meera@123"),
            role=UserRole.EMPLOYEE,
            manager_id=manager2.id,
            department="Sales",
            monthly_limit=Decimal("30000.00"),
        ),
    ])

    finance = User(
        name="Rohit Verma",
        email="rohit.verma@example.com",
        password_hash=hash_password("Rohit@123"),
        role=UserRole.FINANCE,
        department="Finance",
        monthly_limit=None,
    )

    db.add_all(employees)
    db.add(finance)

    db.commit()

    print("Users seeded successfully.")


def create_claim(
    db,
    *,
    user,
    merchant,
    expense_date,
    amount,
    category,
    description,
    status,
    raw_receipt=None,
    duplicate_status=DuplicateStatus.NONE,
    duplicate_of_claim_id=None,
    duplicate_score=None,
):
    claim = Claim(
        claim_number="TEMP",
        user_id=user.id,
        merchant=merchant,
        expense_date=expense_date,
        amount=Decimal(str(amount)),
        currency="INR",
        category=category,
        description=description,
        status=status,
        duplicate_status=duplicate_status,
        duplicate_of_claim_id=duplicate_of_claim_id,
        duplicate_score=duplicate_score,
    )

    if status == ClaimStatus.SUBMITTED:
        claim.submitted_at = datetime.utcnow()

    elif status == ClaimStatus.APPROVED:
        claim.submitted_at = datetime.utcnow()
        claim.approved_at = datetime.utcnow()

    elif status == ClaimStatus.PAID:
        claim.submitted_at = datetime.utcnow()
        claim.approved_at = datetime.utcnow()
        claim.paid_at = datetime.utcnow()

    elif status == ClaimStatus.REJECTED:
        claim.submitted_at = datetime.utcnow()
        claim.rejected_at = datetime.utcnow()

    db.add(claim)
    db.flush()

    claim.claim_number = (
        f"CLM-{datetime.utcnow().strftime('%Y%m')}-{claim.id:05d}"
    )

    if raw_receipt is not None:
        normalized_text = normalize_receipt_text(raw_receipt)

        receipt = Receipt(
            claim_id=claim.id,
            raw_text=raw_receipt,
            extracted_data=None,
            extraction_confidence=None,
            normalized_text=normalized_text,
            text_hash=calculate_text_hash(normalized_text),
        )

        db.add(receipt)

    db.flush()

    return claim


def seed_claims(db):
    existing_claims = db.query(Claim).count()

    if existing_claims > 0:
        print("Claims already exist. Skipping claim seed.")
        return

    users = {
        user.email: user
        for user in db.query(User).all()
    }

    arjun = users["arjun.kumar@example.com"]
    neha = users["neha.reddy@example.com"]
    vikram = users["vikram.singh@example.com"]
    sneha = users["sneha.patel@example.com"]
    kiran = users["kiran.das@example.com"]
    meera = users["meera.iyer@example.com"]
    rahul = users["rahul.mehta@example.com"]
    priya = users["priya.sharma@example.com"]
    anita = users["anita.rao@example.com"]

    # 1. Paid travel claim
    create_claim(
        db,
        user=arjun,
        merchant="IndiGo",
        expense_date=datetime(2026, 9, 1),
        amount="8500.00",
        category=ExpenseCategory.TRAVEL,
        description="Flight for client visit",
        status=ClaimStatus.PAID,
        raw_receipt=(
            "INDIGO AIRLINES\n"
            "HYD TO DEL\n"
            "01/09/2026\n"
            "TOTAL INR 8500"
        ),
    )

    # 2. Paid meals claim
    create_claim(
        db,
        user=arjun,
        merchant="Barbeque Nation",
        expense_date=datetime(2026, 9, 2),
        amount="4200.00",
        category=ExpenseCategory.MEALS,
        description="Team dinner",
        status=ClaimStatus.PAID,
        raw_receipt=(
            "BARBEQUE NATION\n"
            "TABLE 12\n"
            "DINNER\n"
            "TOTAL Rs 4,200"
        ),
    )

    # 3. Submitted claim for Rahul to review
    create_claim(
        db,
        user=neha,
        merchant="Uber",
        expense_date=datetime(2026, 9, 3),
        amount="1250.00",
        category=ExpenseCategory.TAXI_LOCAL_TRANSPORT,
        description="Taxi to office",
        status=ClaimStatus.SUBMITTED,
        raw_receipt=(
            "UBER TRIP\n"
            "HYDERABAD\n"
            "03-09-26\n"
            "AMT 1250"
        ),
    )

    # 4. Approved claim waiting for Finance
    create_claim(
        db,
        user=vikram,
        merchant="Amazon Business",
        expense_date=datetime(2026, 9, 4),
        amount="6800.00",
        category=ExpenseCategory.OFFICE_SUPPLIES,
        description="Office equipment",
        status=ClaimStatus.APPROVED,
        raw_receipt=(
            "amazon.in\n"
            "office supplies\n"
            "04/09/26\n"
            "total 6800 rs"
        ),
    )

    # 5. Rejected claim
    rejected_claim = create_claim(
        db,
        user=sneha,
        merchant="Cafe Coffee Day",
        expense_date=datetime(2026, 9, 4),
        amount="950.00",
        category=ExpenseCategory.MEALS,
        description="Coffee meeting",
        status=ClaimStatus.REJECTED,
        raw_receipt=(
            "CCD\n"
            "coffee + snacks\n"
            "04.09.2026\n"
            "950"
        ),
    )

    db.add(
        ClaimReview(
            claim_id=rejected_claim.id,
            reviewer_id=priya.id,
            action=ReviewAction.REJECTED,
            comment="Insufficient business justification.",
        )
    )

    db.add(
        AuditLog(
            claim_id=rejected_claim.id,
            actor_id=priya.id,
            event_type="CLAIM_REJECTED",
            old_value="SUBMITTED",
            new_value="REJECTED",
        )
    )

    # 6. Duplicate receipt example
    original_receipt = (
        "HOTEL TAJ\n"
        "HYDERABAD\n"
        "05/09/2026\n"
        "ROOM CHARGE\n"
        "TOTAL INR 7200"
    )

    original_claim = create_claim(
        db,
        user=kiran,
        merchant="Hotel Taj",
        expense_date=datetime(2026, 9, 5),
        amount="7200.00",
        category=ExpenseCategory.ACCOMMODATION,
        description="Hotel stay",
        status=ClaimStatus.PAID,
        raw_receipt=original_receipt,
    )

    duplicate_receipt = (
        "Taj Hotel Hyderabad\n"
        "Room charge\n"
        "5 Sep 2026\n"
        "Total Rs 7,200"
    )

    create_claim(
        db,
        user=kiran,
        merchant="Taj Hotel Hyderabad",
        expense_date=datetime(2026, 9, 5),
        amount="7200.00",
        category=ExpenseCategory.ACCOMMODATION,
        description="Hotel room charge",
        status=ClaimStatus.SUBMITTED,
        raw_receipt=duplicate_receipt,
        duplicate_status=DuplicateStatus.LIKELY,
        duplicate_of_claim_id=original_claim.id,
        duplicate_score=92.50,
    )

    # 7. Employee close to monthly limit
    create_claim(
        db,
        user=meera,
        merchant="Air India",
        expense_date=datetime(2026, 9, 3),
        amount="14500.00",
        category=ExpenseCategory.TRAVEL,
        description="Business travel",
        status=ClaimStatus.PAID,
        raw_receipt=(
            "AIR INDIA\n"
            "BLR HYD\n"
            "06/09/26\n"
            "TOTAL 14500"
        ),
    )

    create_claim(
        db,
        user=meera,
        merchant="Novotel",
        expense_date=datetime(2026, 9, 4),
        amount="9000.00",
        category=ExpenseCategory.ACCOMMODATION,
        description="Business hotel stay",
        status=ClaimStatus.PAID,
        raw_receipt=(
            "NOVOTEL HYDERABAD\n"
            "06-09-2026\n"
            "ROOM 1 NIGHT\n"
            "TOTAL INR 9000"
        ),
    )

    create_claim(
        db,
        user=meera,
        merchant="Uber",
        expense_date=datetime(2026, 9, 2),
        amount="4800.00",
        category=ExpenseCategory.TAXI_LOCAL_TRANSPORT,
        description="Airport and client transport",
        status=ClaimStatus.PAID,
        raw_receipt=(
            "uber\n"
            "airport trip + client visit\n"
            "7/9/26\n"
            "Rs 4800"
        ),
    )

    # 8. Manager claim — Anita can approve Rahul's claim.
    create_claim(
        db,
        user=rahul,
        merchant="Vistara",
        expense_date=datetime(2026, 9, 1),
        amount="12000.00",
        category=ExpenseCategory.TRAVEL,
        description="Management travel",
        status=ClaimStatus.SUBMITTED,
        raw_receipt=(
            "VISTARA\n"
            "HYD DEL\n"
            "07/09/26\n"
            "TOTAL RS 12000"
        ),
    )

    # 9. Manager claim for Priya
    create_claim(
        db,
        user=priya,
        merchant="Marriott",
        expense_date=datetime(2026, 9, 5),
        amount="10500.00",
        category=ExpenseCategory.ACCOMMODATION,
        description="Sales conference stay",
        status=ClaimStatus.SUBMITTED,
        raw_receipt=(
            "MARRIOTT HYDERABAD\n"
            "08 SEP 2026\n"
            "ROOM\n"
            "TOTAL INR 10500"
        ),
    )

    db.commit()

    print("Realistic claims seeded successfully.")


def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        seed_users(db)
        seed_claims(db)

        print("Database seed completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()