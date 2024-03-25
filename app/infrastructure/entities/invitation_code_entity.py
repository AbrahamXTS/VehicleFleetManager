import uuid
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

# Removing circular references on runtime execution
if TYPE_CHECKING:
    from .user_entity import User


class InvitationCode(SQLModel, table=True):
    code: str = Field(default=uuid.uuid4, primary_key=True)
    email: str
    created_by_user: int = Field(foreign_key="user.id")
    created_by: "User" = Relationship(back_populates="invitation_codes")
