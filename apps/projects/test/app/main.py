from fastapi import FastAPI

from app.api.v1.routes import health, users


def create_app() -> FastAPI:
    application = FastAPI(title="FastAPI Test Project", version="1.0.0")

    application.include_router(health.router, prefix="/api/v1", tags=["Health"])
    application.include_router(users.router, prefix="/api/v1", tags=["Users"])

    return application


app = create_app()
