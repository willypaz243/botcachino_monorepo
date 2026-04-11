from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes.info_router import info_router
from src.api.routes.news_router import news_router
from src.db.database import async_engine, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(news_router)
app.include_router(info_router)


@app.get("/")
async def root():
    return {"message": "API running successfully!"}
