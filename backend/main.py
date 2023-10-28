from fastapi import FastAPI
from settings import settings
from src.api.v1 import router
from starlette.middleware.cors import CORSMiddleware


def create_app():
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
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
