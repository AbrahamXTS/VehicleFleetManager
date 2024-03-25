from typing import Annotated
from fastapi import APIRouter, Depends

from ..security.security_scheme import SECURITY_SCHEME

invitation_codes_router = APIRouter()


@invitation_codes_router.get("/{invitation_code}")
def get_invitation_code_by_id(
    invitation_code: str, token: Annotated[str, Depends(SECURITY_SCHEME)]
) -> None:
    return None


@invitation_codes_router.get("/")
def get_all_invitation_codes(token: Annotated[str, Depends(SECURITY_SCHEME)]) -> None:
    return None


@invitation_codes_router.post("/")
def create_invitation_code(token: Annotated[str, Depends(SECURITY_SCHEME)]) -> None:
    return None


@invitation_codes_router.put("/{invitation_code}")
def edit_invitation_code(
    invitation_code: str, token: Annotated[str, Depends(SECURITY_SCHEME)]
) -> None:
    return None


@invitation_codes_router.delete("/{invitation_code}")
def delete_invitation_code(
    invitation_code: str, token: Annotated[str, Depends(SECURITY_SCHEME)]
) -> None:
    return None
