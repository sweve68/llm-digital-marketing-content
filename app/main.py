from fastapi import FastAPI
from app.routers.status import router as status_router
from app.routers.hello import router as hello_router

app = FastAPI()

app.router.include_router(status_router, prefix="/app", tags=["Status"])
app.router.include_router(hello_router, prefix="/app", tags=["Status"])
