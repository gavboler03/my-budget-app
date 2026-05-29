from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
import models
from routers import users
from sqlalchemy import text
from database import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API is Running"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "ok", "db": result.scalar()}
    except Exception as e:
        return {"status": "db-error", "error": str(e)}