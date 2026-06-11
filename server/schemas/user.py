from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from server.models.enums import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    role: UserRole
    cartao_ufrgs: str | None = None


class AlunoData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cartao_ufrgs: str = Field(min_length=1, max_length=20)
    semestre_ingresso: str = Field(min_length=1, max_length=7)


class UserCreate(BaseModel):
    email: EmailStr
    nome: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=8)
    role: UserRole
    aluno: AlunoData | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    nome: str | None = Field(default=None, min_length=1, max_length=150)
    is_active: bool | None = None
    aluno: AlunoData | None = None


class UserAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    nome: str
    role: UserRole
    is_active: bool
    created_at: datetime
    aluno: AlunoData | None = None
