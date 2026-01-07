from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from src.utils.auth import require_admin
from sqlalchemy import select, insert, update, delete

from src.database.execution import db_client
from src.database.schema import buses as buses_table, drivers as drivers_table, students as students_table

router = APIRouter(prefix="/admins", tags=["admins"], dependencies=[Depends(require_admin)])


@router.get("/buses", status_code=200)
def admin_list_buses() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(buses_table))
    if not rows:
        return []
    return rows


@router.delete("/buses/{bus_id}", status_code=204)
def admin_delete_bus(bus_id: UUID):
    query = delete(buses_table).where(buses_table.c.id == bus_id)
    db_client.execute_one(query)
    return None


@router.get("/drivers", status_code=200)
def admin_list_drivers() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(drivers_table))
    if not rows:
        return []
    return rows


@router.get("/students", status_code=200)
def admin_list_students() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(students_table))
    if not rows:
        return []
    return rows
