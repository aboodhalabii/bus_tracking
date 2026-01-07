from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.database.execution import db_client
from src.database.schema import stops as stops_table

router = APIRouter(prefix="/stops", tags=["stops"])


@router.get("/", status_code=200)
def list_stops() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(stops_table))
    if not rows:
        return []
    return rows


@router.get("/{stop_id}", status_code=200)
def get_stop(stop_id: UUID) -> dict[str, Any]:
    row = db_client.execute_one(select(stops_table).where(stops_table.c.id == stop_id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")
    return row
