from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Any, Optional

from app.api.v1.crud import get_courses
from app.schemas import ExchangeData, Course

router = APIRouter()


@router.get("/courses/", status_code=200)
def search_recipes():
    return get_courses()
