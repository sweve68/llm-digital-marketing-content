from fastapi import APIRouter
from app.helpers.hello import add_two_numbers
router = APIRouter()

@router.get("/hello")
def say_hello():
    return {"Sum is": add_two_numbers(1, 2)}