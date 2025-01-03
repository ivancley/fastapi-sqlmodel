from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from decouple import config as decouple_config
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from typing import AsyncGenerator


# DB = "postgresql+psycopg2://fastapi:password123@localhost:5432/fastapi_db"

DB_URL = "postgresql+asyncpg://fastapi:password123@localhost:5432/fastapi_db"

engine: AsyncEngine = create_async_engine(DB_URL, echo=True)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
