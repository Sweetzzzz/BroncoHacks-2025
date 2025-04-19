from datetime import datetime
from typing import Annotated
from sqlmodel import Column, Field, SQLModel
from pgvector.sqlalchemy import Vector


class ResourceBase(SQLModel):
    name: str
    file_path: str
    label: str
    type: str


class Resource(ResourceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(ResourceBase):
    name: str | None
    file_path: str | None
    label: str | None
    type: str | None


class UserBase(SQLModel):
    name: str
    email: str
    student_id: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: str | None
    email: str | None
    student_id: str | None
