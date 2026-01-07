from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.database.execution import db_client
from src.database.schema import trips as trips_table

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("/", status_code=200)
def list_trips() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(trips_table))
    if not rows:
        return []
    return rows


@router.get("/{trip_id}", status_code=200)
def get_trip(trip_id: UUID) -> dict[str, Any]:
    row = db_client.execute_one(select(trips_table).where(trips_table.c.id == trip_id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return row
