from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

from app.database.config import settings

# Create a database engine to connect with database
engine = create_async_engine(
    # database type/dialect and file name
    url=settings.POSTGRES_URL,
    # Log sql queries
    echo=True,
)


async def create_db_tables():
    async with engine.begin() as connection:
        # from app.database.models import Shipment  # noqa: F401
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


# Session Dependency Annotation
# Annotated[AsyncSession, Depends(get_session)] is a type alias that says:
# "This parameter is an AsyncSession, and FastAPI should get it by calling get_session()."
SessionDep = Annotated[AsyncSession, Depends(get_session)]

