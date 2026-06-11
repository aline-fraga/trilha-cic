from pydantic import BaseModel, ConfigDict

from server.models.enums import UserRole


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    role: UserRole
    cartao_ufrgs: str | None = None
