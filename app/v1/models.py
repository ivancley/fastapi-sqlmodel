import uuid
from datetime import datetime, timezone
from typing import List, Optional

from decouple import config as decouple_config
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Index, Column, DateTime
from sqlalchemy.sql import func

#SCHEMA = decouple_config("SCHEMA")


class BaseModel(SQLModel, table=False):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.utcnow()
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.utcnow(),
        sa_column_kwargs={"onupdate": lambda: datetime.utcnow()},
    )
    
    is_deleted: bool = Field(default=False, nullable=False)
    

class UserContextLink(SQLModel, table=True):
    __tablename__ = "user_context"
    __table_args__ = (
        UniqueConstraint("user_id", "context_id", name="uq_user_context"),
        #{"schema": SCHEMA},
    )
    
    #user_id: uuid.UUID = Field(primary_key=True, foreign_key=f"{SCHEMA}.users.id")
    #context_id: uuid.UUID = Field(primary_key=True, foreign_key=f"{SCHEMA}.contexts.id")
    
    user_id: uuid.UUID = Field(primary_key=True, foreign_key=f"users.id")
    context_id: uuid.UUID = Field(primary_key=True, foreign_key=f"contexts.id")


class ContextModel(BaseModel, table=True):
    __tablename__ = "contexts"
    __table_args__ = (
        UniqueConstraint("name", name="uq_context_name"),
        Index("ix_context_name", "name", unique=False),
        #{"schema": SCHEMA},
    )
    name: str = Field(max_length=60, index=True, nullable=False)

    # Relação muitos-para-muitos com UserModel
    users: List["UserModel"] = Relationship(
        back_populates="contexts", link_model=UserContextLink
    )


class UserModel(BaseModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        Index("ix_user_email", "email"),
        #{"schema": SCHEMA},
    )

    name: str = Field(max_length=60, index=True, nullable=False)
    full_name: Optional[str] = Field(max_length=120, index=True, nullable=False)
    email: str = Field(
        max_length=255,
        index=True,
        nullable=False,
    )
    phone: Optional[str] = Field(max_length=20, default=None)
    is_active: bool = Field(default=True, nullable=False)
    password_hash: str = Field(max_length=128, nullable=False)

    contexts: List[ContextModel] = Relationship(
        back_populates="users", link_model=UserContextLink
    )
