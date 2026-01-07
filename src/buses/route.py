from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, insert

from src.database.execution import db_client
from src.database.schema import buses as buses_table

router = APIRouter(prefix="/buses", tags=["buses"])


@router.get("/", status_code=200)
def list_buses() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(buses_table))
    if not rows:
        return []
    return rows


@router.get("/{bus_id}", status_code=200)
def get_bus(bus_id: UUID) -> dict[str, Any]:
    row = db_client.execute_one(select(buses_table).where(buses_table.c.id == bus_id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")
    return row


@router.post("/", status_code=201)
def create_bus(payload: dict) -> dict[str, Any]:
    query = insert(buses_table).values(**payload).returning(buses_table)
    row = db_client.execute_one(query)
    return row
