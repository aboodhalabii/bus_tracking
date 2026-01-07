from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, insert

from src.database.execution import db_client
from src.database.schema import drivers as drivers_table

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.get("/", status_code=200)
def list_drivers() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(drivers_table))
    if not rows:
        return []
    return rows


@router.get("/{driver_id}", status_code=200)
def get_driver(driver_id: UUID) -> dict[str, Any]:
    row = db_client.execute_one(select(drivers_table).where(drivers_table.c.id == driver_id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    return row


@router.post("/", status_code=201)
def create_driver(payload: dict) -> dict[str, Any]:
    query = insert(drivers_table).values(**payload).returning(drivers_table)
    row = db_client.execute_one(query)
    return row
