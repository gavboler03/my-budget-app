from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserBase
from database import get_db
from crud import get_all_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserBase])
async def get_users(
    db: AsyncSession = Depends(get_db), 
):
    return await get_all_users(db)