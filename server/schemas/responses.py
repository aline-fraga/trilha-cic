UNAUTHORIZED_401 = {
    "description": "Token ausente, inválido ou expirado",
    "content": {
        "application/json": {
            "example": {"detail": "Not authenticated"}
        }
    },
}

FORBIDDEN_403 = {
    "description": "Acesso negado: papel do usuário não tem permissão",
    "content": {
        "application/json": {
            "example": {"detail": "Acesso negado"}
        }
    },
}

NOT_FOUND_404 = {
    "description": "Recurso não encontrado",
    "content": {
        "application/json": {
            "example": {"detail": "Recurso não encontrado"}
        }
    },
}

BAD_REQUEST_400 = {
    "description": "Erro de regra de negócio ou inconsistência nos dados",
    "content": {
        "application/json": {
            "example": {"detail": "Dados inválidos"}
        }
    },
}

CONFLICT_409 = {
    "description": "Conflito com estado atual do recurso (ex.: e-mail já em uso)",
    "content": {
        "application/json": {
            "example": {"detail": "E-mail 'usuario@inf.ufrgs.br' já está em uso"}
        }
    },
}
