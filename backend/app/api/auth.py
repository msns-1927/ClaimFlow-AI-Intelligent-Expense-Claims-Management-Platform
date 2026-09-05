from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_role
from app.core.security import create_access_token, verify_password
from app.database.session import get_db
from app.models import User, UserRole
from app.schemas.auth import (
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    statement = select(User).where(User.email == data.email)
    user = db.execute(statement).scalar_one_or_none()

    if user is None or not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.id)

    return LoginResponse(
        access_token=token,
    )


@router.get("/me", response_model=CurrentUserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return CurrentUserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role.value,
        department=current_user.department,
        monthly_limit=float(current_user.monthly_limit)
        if current_user.monthly_limit is not None
        else None,
    )

@router.get("/manager-test")
def manager_test(
    current_user: User = Depends(
        require_role(UserRole.MANAGER)
    ),
):
    return {
        "message": "Manager access granted",
        "user": current_user.name,
        "role": current_user.role.value,
    }