from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models import User
from sqlalchemy import or_

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()