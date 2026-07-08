from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import LoginRequest, RegisterRequest
from models import User
from auth import verify_password, create_access_token, hash_password
from database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = select(User).where(User.username == credentials.username)
    user = (await db.execute(result)).scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail= "Invalid username or password")
    
    token = create_access_token(user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
async def register(credentials: RegisterRequest, db:AsyncSession = Depends(get_db)):
    result = select(User).where(User.email == credentials.email)
    existing = (await db.execute(result)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(username = credentials.username, email = credentials.email, hashed_password = hash_password(credentials.password))

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "Successfully registered"}