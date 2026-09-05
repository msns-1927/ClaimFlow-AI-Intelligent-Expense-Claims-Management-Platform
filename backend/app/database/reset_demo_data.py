from sqlalchemy import text

from app.database.session import SessionLocal


def reset_demo_data():
    db = SessionLocal()

    try:
        print("Removing development claim data...")

        db.execute(
            text(
                """
                TRUNCATE TABLE
                    audit_logs,
                    claim_reviews,
                    receipts,
                    claims
                RESTART IDENTITY CASCADE;
                """
            )
        )

        db.commit()

        print("Claim-related data cleared successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    reset_demo_data()