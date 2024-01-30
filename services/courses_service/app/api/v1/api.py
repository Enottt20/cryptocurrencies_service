from fastapi import APIRouter

from app.api.v1.endpoints import courses


api_router = APIRouter()
api_router.include_router(courses.router, prefix="/recipes", tags=["recipes"])
