from apps import route_questions
from fastapi import APIRouter

app_router = APIRouter()

app_router.include_router(
    route_questions.router, prefix="", tags=["questions"], include_in_schema=False
)
