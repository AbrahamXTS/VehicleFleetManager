from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.services.auth_service import AuthService

from ..dto.bearer_token_dto import BearerTokenDTO
from ..dto.candidate_dto import CandidateDTO
from ..mappers.candidate_mappers import map_candidate_dto_to_candidate_model
from ..repositories.relational_database_user_repository_impl import (
    RelationalDatabaseUserRepositoryImpl,
)
from ..security.bcrypt_password_encryptor_impl import BcryptPasswordEncryptorImpl
from ..security.json_web_token_tools import JsonWebTokenTools


auth_router = APIRouter()
auth_service = AuthService(
    password_encryptor=BcryptPasswordEncryptorImpl(),
    user_repository=RelationalDatabaseUserRepositoryImpl(),
)


@auth_router.post("/login")
def login_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> BearerTokenDTO:
    try:
        user = auth_service.login(email=user_data.username, password=user_data.password)

        return BearerTokenDTO(
            access_token=JsonWebTokenTools.create_access_token(user.email)
        )
    except:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@auth_router.post("/signup")
def signup_user(candidate: CandidateDTO):
    auth_service.signup(map_candidate_dto_to_candidate_model(candidate))
