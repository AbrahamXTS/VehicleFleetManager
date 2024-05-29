from pydantic import BaseModel, EmailStr


class InvitationCodeRequestDTO(BaseModel):
    email: EmailStr
