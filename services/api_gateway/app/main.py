from fastapi import FastAPI
from .routes.v1 import router as v1_router

app = FastAPI(title="KFRP API Gateway", version="1.0.0")
app.include_router(v1_router, prefix="/v1")
