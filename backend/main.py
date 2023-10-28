from api.v1.router import router
from fastapi import FastAPI

# from settings import settings
from starlette.middleware.cors import CORSMiddleware


def create_app():
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://localhost:3000",
            "http://frontend",
            "http://frontend:3000",
        ],
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
