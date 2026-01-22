from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine
from app.api.routes.users import router as users_router

app = FastAPI(title="FastAPI Docker Stack", version="1.0.0")

app.include_router(users_router)


@app.get("/health")
def health():
    # DB health check
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}
