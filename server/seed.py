"""Idempotent seed script — populates the DB from CSV files in data/.

Usage (from `trilha-cic/`):
    .venv/bin/python -m server.seed

Reads:
    data/disciplinas.csv  (nome, codigo, tipo, carga_horaria, link_plano_ensino)
    data/trilhas.csv      (nome, resumo, disciplinas_codigos — codes joined by ';')
"""

import csv
from pathlib import Path

from sqlalchemy import delete

from server.database import SessionLocal
from server.models import Disciplina, DisciplinaTipo, Trilha, trilha_disciplinas
from server.models.aluno import Aluno
from server.models.enums import UserRole
from server.models.user import User
from server.services.auth_service import AuthService

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DISCIPLINAS_CSV = DATA_DIR / "disciplinas.csv"
TRILHAS_CSV = DATA_DIR / "trilhas.csv"

USERS_SEED = [
    {
        "email": "aluno@ufrgs.br",
        "password": "aluno123",
        "nome": "Lucas Martins",
        "role": UserRole.ALUNO,
        "cartao_ufrgs": "00333333",
        "semestre_ingresso": "2023/2",
    },
    {
        "email": "comgrad@ufrgs.br",
        "password": "comgrad123",
        "nome": "Coordenação de Graduação",
        "role": UserRole.COMGRAD,
    },
    {
        "email": "admin@ufrgs.br",
        "password": "admin123",
        "nome": "Administrador",
        "role": UserRole.ADMIN,
    },
]


def main() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(trilha_disciplinas))
        db.execute(delete(Trilha))
        db.execute(delete(Disciplina))
        db.execute(delete(Aluno))
        db.execute(delete(User))
        db.commit()

        for data in USERS_SEED:
            user = User(
                email=data["email"],
                password_hash=AuthService.hash_password(data["password"]),
                nome=data["nome"],
                role=data["role"],
                is_active=True,
            )
            db.add(user)
            db.flush()

            if data["role"] == UserRole.ALUNO:
                db.add(Aluno(
                    user_id=user.id,
                    cartao_ufrgs=data["cartao_ufrgs"],
                    semestre_ingresso=data["semestre_ingresso"],
                ))

        disciplinas_por_codigo: dict[str, Disciplina] = {}
        with open(DISCIPLINAS_CSV, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                disciplina = Disciplina(
                    nome=row["nome"],
                    codigo=row["codigo"],
                    tipo=DisciplinaTipo(row["tipo"]),
                    carga_horaria=int(row["carga_horaria"]),
                    link_plano_ensino=row["link_plano_ensino"] or None,
                )
                disciplinas_por_codigo[row["codigo"]] = disciplina
                db.add(disciplina)

        with open(TRILHAS_CSV, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                codigos = [c.strip() for c in row["disciplinas_codigos"].split(";") if c.strip()]
                trilha = Trilha(
                    nome=row["nome"],
                    resumo=row["resumo"],
                    disciplinas=[disciplinas_por_codigo[c] for c in codigos],
                )
                db.add(trilha)

        db.commit()

        print(
            f"Seed concluído: {db.query(User).count()} usuários, "
            f"{db.query(Disciplina).count()} disciplinas, "
            f"{db.query(Trilha).count()} trilhas"
        )
        print("Usuários de teste:")
        for data in USERS_SEED:
            print(f"  {data['role'].value}: {data['email']} / {data['password']}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
