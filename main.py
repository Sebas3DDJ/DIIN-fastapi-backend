from fastapi import FastAPI
from app.db.init_db import init_db

app = FastAPI(title="DIIN FASTAPI Backend")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Backend DIIN FASTAPI funcionando correctamente!"}

from app.api.auth import router as authRouter

app.include_router(authRouter)
