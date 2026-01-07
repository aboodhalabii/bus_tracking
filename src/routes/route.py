from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.database.execution import db_client
from src.database.schema import routes as routes_table

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/", status_code=200)
def list_routes() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(routes_table))
    if not rows:
        return []
    return rows


@router.get("/{route_id}", status_code=200)
def get_route(route_id: UUID) -> dict[str, Any]:
    row = db_client.execute_one(select(routes_table).where(routes_table.c.id == route_id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return row
