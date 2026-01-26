from contextlib import asynccontextmanager
from fastapi import FastAPI
from .app.core.config import settings

from rich import print, panel
# The merit of async lifespan is consistency with FastAPI’s async model and the ability to do useful async work at startup when you have it (async DB, HTTP, etc.).
@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started...", border_style="green"))
    yield
    print(panel.Panel("...stopped!", border_style="red"))

# init_db()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan_handler
)

@app.get("/")
def read_root():
    return {"Detail": "Server running "}