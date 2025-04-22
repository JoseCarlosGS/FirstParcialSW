from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str = Field(index=True)
    name: str = Field()
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: str = Field(default="2023-10-01T00:00:00Z")
    updated_at: str = Field(default="2023-10-01T00:00:00Z")
    last_login: str = Field(default="2023-10-01T00:00:00Z")
    

# Code below omitted 👇