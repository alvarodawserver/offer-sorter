from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registers the tables in Base.metadata)
from app.database import Base, engine
from app.routers import offers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    Base.metadata.create_all(engine)
    yield
    # anything here runs once on shutdown (nothing needed for now)


app = FastAPI(lifespan=lifespan)
app.include_router(offers.router)
