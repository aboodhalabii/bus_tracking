from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select, insert

from src.database.execution import db_client
from src.database.schema import users as users_table
from src.utils.auth import hash_password, verify_password, create_access_token


class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    role: str = "student"
    first_name: str | None = None
    last_name: str | None = None


class LoginIn(BaseModel):
    email: EmailStr
    password: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(payload: RegisterIn) -> Dict[str, Any]:
    # Check if exists
    exists = db_client.execute_one(select(users_table).where(users_table.c.email == payload.email))
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed = hash_password(payload.password)
    query = insert(users_table).values(
        email=payload.email,
        password_hash=hashed,
        role=payload.role,
        first_name=payload.first_name,
        last_name=payload.last_name,
    ).returning(users_table)
    row = db_client.execute_one(query)
    if not row:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create user")
    # remove password
    row.pop("password_hash", None)
    return row


@router.post("/login", status_code=200)
def login(payload: LoginIn) -> Dict[str, Any]:
    row = db_client.execute_one(select(users_table).where(users_table.c.email == payload.email))
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(payload.password, row.get("password_hash")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token_data = {"sub": str(row.get("id")), "email": row.get("email"), "role": row.get("role")}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}
