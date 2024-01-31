from fastapi import APIRouter
from app.api.v1.endpoints import courses


api_router_v1 = APIRouter()
api_router_v1.include_router(courses.router, tags=["courses"])
