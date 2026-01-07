from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, insert

from src.database.execution import db_client
from src.database.schema import students as students_table

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/", status_code=200)
def list_students() -> list[dict[str, Any]]:
    rows = db_client.execute_all(select(students_table))
    if not rows:
        return []
    return rows


@router.get("/{student_id}", status_code=200)
def get_student(student_id: UUID) -> dict[str, Any]:
    row = db_client.execute_one(select(students_table).where(students_table.c.id == student_id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return row


@router.post("/", status_code=201)
def create_student(payload: dict) -> dict[str, Any]:
    query = insert(students_table).values(**payload).returning(students_table)
    row = db_client.execute_one(query)
    return row
