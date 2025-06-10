from fastapi import APIRouter
from app.prompts.content import content

router = APIRouter()
@router.get("/status")
def get_status():
    return {"status": "ok", "content": content}