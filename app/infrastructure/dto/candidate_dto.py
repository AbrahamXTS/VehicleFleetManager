from pydantic import BaseModel


class CandidateDTO(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    invitation_code: str
