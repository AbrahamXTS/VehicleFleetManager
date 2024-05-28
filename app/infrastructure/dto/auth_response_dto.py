from pydantic import BaseModel

from app.infrastructure.dto.authenticated_user_dto import AuthenticatedUserDTO


class AuthResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthenticatedUserDTO
