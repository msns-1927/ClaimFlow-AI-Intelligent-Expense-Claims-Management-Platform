from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.base import Base
from app.database.session import engine, get_db
from app.models import AuditLog, ClaimReview, Receipt, User
from app.api.auth import router as auth_router
from app.api.claims import router as claims_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Expense Claims API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+|https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(claims_router)


@app.get("/")
def root():
    return {
        "message": "Expense Claims API is running"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1"))
        result.scalar()

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }