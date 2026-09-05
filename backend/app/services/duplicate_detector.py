import hashlib
import re
from difflib import SequenceMatcher

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Claim, ClaimStatus, Receipt


def normalize_receipt_text(text: str) -> str:
    """
    Normalize receipt text so formatting, punctuation,
    currency symbols, and whitespace differences do not
    prevent duplicate detection.
    """

    text = text.lower()

    # Normalize common currency representations.
    text = text.replace("₹", " rs ")
    text = text.replace("inr", " rs ")
    text = text.replace("rupees", " rs ")

    # Remove punctuation.
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def calculate_text_hash(normalized_text: str) -> str:
    return hashlib.sha256(
        normalized_text.encode("utf-8")
    ).hexdigest()


def calculate_similarity(text_a: str, text_b: str) -> float:
    return SequenceMatcher(
        None,
        text_a,
        text_b,
    ).ratio()


def detect_duplicate(
    db: Session,
    merchant: str,
    expense_date,
    amount,
    normalized_text: str,
    current_claim_id: int | None = None,
):
    """
    Detect possible duplicate expenses.

    Signals:
    - exact normalized receipt text
    - merchant
    - amount
    - expense date
    - fuzzy text similarity

    Returns NONE, POSSIBLE, or LIKELY.
    """

    new_hash = calculate_text_hash(normalized_text)

    # Get previous claims and receipts.
    rows = db.execute(
        select(Claim, Receipt)
        .join(Receipt, Receipt.claim_id == Claim.id)
        .where(Claim.status != ClaimStatus.REJECTED)
    ).all()

    best_claim_id = None
    best_score = 0.0

    normalized_merchant = merchant.strip().lower()

    for claim, receipt in rows:

        # Never compare the claim against itself.
        if current_claim_id is not None:
            if claim.id == current_claim_id:
                continue

        # Always calculate normalization from raw_text as a fallback.
        existing_text = receipt.normalized_text

        if not existing_text:
            existing_text = normalize_receipt_text(
                receipt.raw_text
            )

        existing_hash = receipt.text_hash

        if not existing_hash:
            existing_hash = calculate_text_hash(
                existing_text
            )

        # 1. Exact receipt match

        if existing_hash == new_hash:
            return {
                "status": "LIKELY",
                "claim_id": claim.id,
                "score": 100.0,
            }

        # 2. Business-field comparison

        same_merchant = (
            normalized_merchant
            == claim.merchant.strip().lower()
        )

        same_amount = (
            float(amount) == float(claim.amount)
        )

        same_date = (
            expense_date.date()
            == claim.expense_date.date()
        )

        # 3. Fuzzy receipt-text similarity

        text_similarity = calculate_similarity(
            normalized_text,
            existing_text,
        )

        # Convert similarity to percentage.
        text_score = text_similarity * 100


        # 4. Calculate combined score

        score = text_score * 0.70

        if same_merchant:
            score += 15

        if same_amount:
            score += 10

        if same_date:
            score += 5

        score = min(score, 100.0)

        if score > best_score:
            best_score = score
            best_claim_id = claim.id


    # Determine duplicate level

    if best_score >= 85:
        duplicate_status = "LIKELY"

    elif best_score >= 60:
        duplicate_status = "POSSIBLE"

    else:
        duplicate_status = "NONE"

    return {
        "status": duplicate_status,
        "claim_id": best_claim_id,
        "score": round(best_score, 2),
    }