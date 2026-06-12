from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from server.models.enums import UserRole


class LoginRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "comgrad@ufrgs.br",
                "password": "comgrad123",
            }
        }
    )

    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    )

    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "Lucas Martins",
                "email": "aluno@ufrgs.br",
                "role": "ALUNO",
                "cartao_ufrgs": "00333333",
            }
        },
    )

    id: int
    nome: str
    email: EmailStr
    role: UserRole
    cartao_ufrgs: str | None = None


class AlunoData(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "cartao_ufrgs": "00567890",
                "semestre_ingresso": "2026/01",
            }
        },
    )

    cartao_ufrgs: str = Field(min_length=1, max_length=20)
    semestre_ingresso: str = Field(min_length=1, max_length=7)


class UserCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "novo.aluno@inf.ufrgs.br",
                "nome": "João da Silva",
                "password": "senha1234",
                "role": "ALUNO",
                "aluno": {
                    "cartao_ufrgs": "00567890",
                    "semestre_ingresso": "2026/01",
                },
            }
        }
    )

    email: EmailStr
    nome: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=8)
    role: UserRole
    aluno: AlunoData | None = None


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "João Silva Júnior",
                "is_active": True,
            }
        }
    )

    email: EmailStr | None = None
    nome: str | None = Field(default=None, min_length=1, max_length=150)
    is_active: bool | None = None
    aluno: AlunoData | None = None


class UserAdminResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 2,
                "email": "novo.aluno@inf.ufrgs.br",
                "nome": "João da Silva",
                "role": "ALUNO",
                "is_active": True,
                "created_at": "2026-06-11T14:32:11",
                "aluno": {
                    "cartao_ufrgs": "00567890",
                    "semestre_ingresso": "2026/01",
                },
            }
        },
    )

    id: int
    email: EmailStr
    nome: str
    role: UserRole
    is_active: bool
    created_at: datetime
    aluno: AlunoData | None = None
