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

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DISCIPLINAS_CSV = DATA_DIR / "disciplinas.csv"
TRILHAS_CSV = DATA_DIR / "trilhas.csv"


def main() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(trilha_disciplinas))
        db.execute(delete(Trilha))
        db.execute(delete(Disciplina))
        db.commit()

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
            f"Seed concluído: {db.query(Disciplina).count()} disciplinas, "
            f"{db.query(Trilha).count()} trilhas"
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
