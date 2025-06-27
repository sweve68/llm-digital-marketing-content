from fastapi import FastAPI
from app.routers.content import router as digital_content_router

app = FastAPI()

app.router.include_router(digital_content_router, prefix="/app", tags=["Digital"])

