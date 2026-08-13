from fastapi import APIRouter, Query

from services.analytics import (
    get_province_activity,
    get_cell_activity,
    get_hourly_activity,
)


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def province_activity():
    return {
        "data": get_province_activity()
    }


@router.get("/cells")
def cell_activity():
    return {
        "data": get_cell_activity()
    }


@router.get("/hourly")
def hourly_activity(
    province: str | None = Query(default=None)
):
    return {
        "data": get_hourly_activity(province)
    }