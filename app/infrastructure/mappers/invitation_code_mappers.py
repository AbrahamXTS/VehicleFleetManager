from app.domain.models.invitation_code_model import InvitationCodeModel
from app.infrastructure.dto.invitation_code_dto import InvitationCodeDTO
from app.infrastructure.entities.invitation_code_entity import InvitationCode


def map_invitation_code_entity_to_invitation_code_model(
    invitation_code_entity: InvitationCode,
) -> InvitationCodeModel:
    return InvitationCodeModel(
        code=invitation_code_entity.code,
        created_by_user=invitation_code_entity.created_by_user,
        email=invitation_code_entity.email,
    )


def map_invitation_code_model_to_invitation_code_entity(
    invitation_code_model: InvitationCodeModel,
) -> InvitationCode:
    return InvitationCode(
        code=invitation_code_model.code,
        created_by_user=invitation_code_model.created_by_user,
        email=invitation_code_model.email,
    )


def map_invitation_code_model_to_invitation_code_dto(
    invitation_code_model: InvitationCodeModel,
) -> InvitationCodeDTO:
    return InvitationCodeDTO(
        code=invitation_code_model.code or "",
        email=invitation_code_model.email,
    )
