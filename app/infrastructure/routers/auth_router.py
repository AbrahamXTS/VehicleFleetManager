from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import logging

from app.application.services.auth_service import AuthService
from app.domain.exceptions.conflict_with_existing_resource_exception import (
    ConflictWithExistingResourceException,
)
from app.domain.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.infrastructure.dto.auth_response_dto import AuthResponseDTO
from app.infrastructure.dto.candidate_dto import CandidateDTO
from app.infrastructure.dto.authenticated_user_dto import AuthenticatedUserDTO
from app.infrastructure.mappers.candidate_mappers import (
    map_candidate_dto_to_candidate_model,
)
from app.infrastructure.mappers.user_mappers import map_user_model_to_user_logged_dto
from app.infrastructure.repositories.relational_database_invitation_code_repository_impl import (
    RelationalDatabaseInvitationCodeRepositoryImpl,
)
from app.infrastructure.repositories.relational_database_user_repository_impl import (
    RelationalDatabaseUserRepositoryImpl,
)
from app.infrastructure.security.bcrypt_password_encryptor_impl import (
    BcryptPasswordEncryptorImpl,
)
from app.infrastructure.security.json_web_token_tools import JsonWebTokenTools


logger = logging.getLogger(__name__)
auth_router = APIRouter()
auth_service = AuthService(
    invitation_code_repository=RelationalDatabaseInvitationCodeRepositoryImpl(),
    password_encryptor=BcryptPasswordEncryptorImpl(),
    user_repository=RelationalDatabaseUserRepositoryImpl(),
)


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> AuthResponseDTO:
    try:
        logger.info("POST /login/")
        logger.debug(f"{status.HTTP_200_OK}, Request body: {user_data.username}")
        user = auth_service.login(email=user_data.username, password=user_data.password)

        return AuthResponseDTO(
            access_token=JsonWebTokenTools.create_access_token(user.email),
            token_type="bearer",
            user=map_user_model_to_user_logged_dto(user),
        )
    except InvalidCredentialsException:
        logger.warning(f"POST /login/ , Invalid credentials. {status.HTTP_401_UNAUTHORIZED}")
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup_user(candidate: CandidateDTO) -> AuthenticatedUserDTO:
    try:
        logger.info("POST /signup/")
        logger.debug(f"Request body: {candidate.email}")
        return map_user_model_to_user_logged_dto(
            auth_service.signup(map_candidate_dto_to_candidate_model(candidate))
        )
    except InvalidCredentialsException:
        logger.warning(f"POST /signup/ , Invalid credentials. {status.HTTP_401_UNAUTHORIZED}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid invitation code",
        )
    except ConflictWithExistingResourceException:
        logger.warning(f"POST /signup/ , Email address already in use. {status.HTTP_409_CONFLICT}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email address is already in use",
        )
