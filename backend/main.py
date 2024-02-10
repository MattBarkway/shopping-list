import sentry_sdk
from fastapi import FastAPI

from settings import Settings
from src.api.v1 import router
from starlette.middleware.cors import CORSMiddleware


def create_app():
    settings = Settings()
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://frontend",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router.router, prefix="/api/v1")

    return application


app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}
