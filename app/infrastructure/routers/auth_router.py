from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

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


auth_router = APIRouter()
auth_service = AuthService(
    invitation_code_repository=RelationalDatabaseInvitationCodeRepositoryImpl(),
    password_encryptor=BcryptPasswordEncryptorImpl(),
    user_repository=RelationalDatabaseUserRepositoryImpl(),
)


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AuthResponseDTO:
    try:
        logger.info("API REQUEST - POST /auth/login/")
        logger.debug(f"Request body: {user_data.username}")
        user = auth_service.login(email=user_data.username, password=user_data.password)

        logger.success(f"API RESPONSE {status.HTTP_200_OK} - POST /login/")
        return AuthResponseDTO(
            access_token=JsonWebTokenTools.create_access_token(user.email),
            token_type="bearer",
            user=map_user_model_to_user_logged_dto(user),
        )
    except InvalidCredentialsException:
        error_detail = "Invalid credentials"
        logger.warning(f"API RESPONSE {status.HTTP_401_UNAUTHORIZED} - POST /login/ - {error_detail}")
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_detail,
        )


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup_user(candidate: CandidateDTO) -> AuthenticatedUserDTO:
    try:
        logger.info("API REQUEST - POST /auth/signup/")
        logger.debug(f"Request body: {candidate.model_dump()}")
        user = auth_service.signup(map_candidate_dto_to_candidate_model(candidate))
        logger.success(f"API RESPONSE {status.HTTP_201_CREATED} - POST /signup/")
        return map_user_model_to_user_logged_dto(user)
    except InvalidCredentialsException:
        error_detail = "Invalid invitation code"
        logger.warning(f"API RESPONSE {status.HTTP_401_UNAUTHORIZED} - POST /signup/ - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_detail,
        )
    except ConflictWithExistingResourceException:
        error_detail = "This email address is already in use"
        logger.warning(f"API RESPONSE {status.HTTP_409_CONFLICT} - POST /signup/ - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_detail,
        )
