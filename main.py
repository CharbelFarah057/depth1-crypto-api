from fastapi import FastAPI
from api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="Riot Take-Home API")
    app.include_router(router)
    return app


app = create_app()
# Run with: python -m uvicorn main:app --reload