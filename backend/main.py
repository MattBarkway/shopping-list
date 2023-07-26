from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from api.utils import get_session
from api.v1.router import router
from settings import settings


def create_app():
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router, prefix="/api/v1")

    return application


app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}
