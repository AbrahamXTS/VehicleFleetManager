from sqlmodel import Field, Relationship, SQLModel

from .invitation_code_entity import InvitationCode


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    last_name: str
    email: str = Field(unique=True)
    password: str
    invitation_codes: list[InvitationCode] = Relationship(back_populates="created_by")
