from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine
from app.api.routes.users import router as users_router
from app.events import register_listeners
from app.middleware.request_id import RequestIDMiddleware

app = FastAPI(title="FastAPI Docker Stack", version="1.0.0")
app.add_middleware(RequestIDMiddleware)

app.include_router(users_router)
register_listeners()


@app.get("/health")
def health():
    # DB health check
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}
