from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.utils.jwt import decode_access_token
from app.models.user import User, UserRole
from app.utils.database import SessionLocal
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def require_ops_user(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ops:
        raise HTTPException(status_code=403, detail="Only ops users can perform this action.")
    return current_user

def require_client_user(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.client:
        raise HTTPException(status_code=403, detail="Only client users can perform this action.")
    return current_user 