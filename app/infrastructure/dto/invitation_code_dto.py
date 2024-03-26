from pydantic import BaseModel, EmailStr


class InvitationCodeDTO(BaseModel):
    code: str
    email: EmailStr
