from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.database.execution import db_client
from src.database.schema import buses as buses_table, trips as trips_table

router = APIRouter(prefix="/bus_locations", tags=["bus_locations"])


@router.get("/trips", status_code=200)
def list_trip_locations() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(trips_table))
    if not rows:
        return []
    return rows


@router.get("/buses", status_code=200)
def list_bus_locations() -> list[dict[str, Any]]:
    # Simple aggregate: join trips + buses could be added; for now return buses
    rows = db_client.execute_all(select(buses_table))
    if not rows:
        return []
    return rows
