from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.models.email_verification_token import EmailVerificationToken
from app.utils.token import generate_token
from app.utils.email import send_email
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/auth", tags=["auth"])

BASE_URL = os.getenv("BASE_URL", None)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, password_hash=hashed_pw, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # If client user, generate verification token and send email
    if user.role == UserRole.client:
        token = generate_token()
        expiry = datetime.utcnow() + timedelta(hours=1)
        db_token = EmailVerificationToken(user_id=new_user.id, token=token, expiry=expiry)
        db.add(db_token)
        db.commit()
        # Build verification URL
        base_url = BASE_URL or str(request.base_url).rstrip("/")
        verify_url = f"{base_url}/auth/verify-email?token={token}"
        send_email(
            to_email=new_user.email,
            subject="Verify your email",
            body=f"Click the link to verify your email: {verify_url}"
        )
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not db_user.is_verified and db_user.role == UserRole.client:
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = create_access_token({"sub": db_user.email, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    db_token = db.query(EmailVerificationToken).filter(EmailVerificationToken.token == token).first()
    if not db_token or db_token.expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.delete(db_token)
    db.commit()
    return {"message": "Email verified successfully"} 