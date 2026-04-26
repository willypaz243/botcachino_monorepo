from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from src.api.routes import api_router
from src.config import settings
from src.db.database import async_engine, create_db_and_tables


async def health_check():
    return {"status": "ok"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_api_route("/api/health", health_check, methods=["GET"])


@app.middleware("http")
async def validate_api_key(request: Request, call_next):
    if request.url.path.startswith("/api/") and request.url.path != "/api/health":
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key != settings.api.key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized"},
            )
    response = await call_next(request)
    return response


app.include_router(api_router)

app.mount("/assets", StaticFiles(directory="web/dist/assets"), name="assets")


@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    from pathlib import Path

    index = Path("web/dist/index.html")
    return HTMLResponse(content=index.read_text())
