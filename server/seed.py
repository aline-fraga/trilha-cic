"""Idempotent seed script — populates the DB from CSV files in data/.

Usage (from `trilha-cic/`):
    .venv/bin/python -m server.seed

Reads:
    data/disciplinas.csv  (nome, codigo, carga_horaria)
    data/trilhas.csv      (nome, resumo, disciplinas_codigos — codes joined by ';')
"""

import csv
from pathlib import Path

from sqlalchemy import delete, select

from server.database import SessionLocal
from server.models import (
    Disciplina,
    Pergunta,
    PerguntaTrilhaPeso,
    Trilha,
    trilha_disciplinas,
)
from server.models.aluno import Aluno
from server.models.enums import (
    DisciplinaTipo,
    PerguntaTipo,
    SolicitacaoStatus,
    UserRole,
)
from server.models.solicitacao import Solicitacao
from server.models.user import User
from server.services.auth_service import AuthService

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DISCIPLINAS_CSV = DATA_DIR / "disciplinas.csv"
TRILHAS_CSV = DATA_DIR / "trilhas.csv"

PERGUNTAS_SEED = [
    {"ordem": 1, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender algoritmos eficientes, estruturas de dados e análise de complexidade."},
    {"ordem": 2, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender os métodos matemáticos e estatísticos por trás de modelos preditivos e simulações."},
    {"ordem": 3, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender como dados são organizados, armazenados e consultados em bancos relacionais e distribuídos."},
    {"ordem": 4, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender como máquinas aprendem com exemplos (aprendizado de máquina, redes neurais, IA generativa)."},
    {"ordem": 5, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender como redes de computadores funcionam — protocolos, arquitetura e comunicação distribuída."},
    {"ordem": 6, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender como proteger sistemas, identificar vulnerabilidades e aplicar criptografia."},
    {"ordem": 7, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender métodos para construir software com qualidade — testes, processos e padrões de projeto."},
    {"ordem": 8, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender como imagens, vídeos, ambientes 3D e experiências imersivas são gerados computacionalmente."},
    {"ordem": 9, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender arquitetura de hardware, paralelismo, GPUs e o que limita o desempenho dos sistemas."},
    {"ordem": 10, "tipo": PerguntaTipo.CONCEITUAL,
     "enunciado": "Tenho interesse em estudar / entender os impactos sociais, éticos, econômicos e legais da computação na sociedade."},
    {"ordem": 11, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em analisar dados para encontrar padrões e gerar insights de negócio."},
    {"ordem": 12, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em construir, treinar e avaliar modelos de aprendizado de máquina."},
    {"ordem": 13, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em projetar esquemas de banco, escrever consultas SQL/NoSQL e otimizar acesso a dados."},
    {"ordem": 14, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em configurar redes, gerenciar tráfego, monitorar e diagnosticar problemas de infraestrutura."},
    {"ordem": 15, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em identificar falhas de segurança, simular ataques e implementar mecanismos de defesa."},
    {"ordem": 16, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em desenvolver aplicações web ou mobile que sejam usadas por pessoas no dia a dia."},
    {"ordem": 17, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em aplicar testes automatizados, code review e processos ágeis para entregar software com qualidade."},
    {"ordem": 18, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em criar gráficos 3D, jogos, experiências em RV/RA ou processar imagens digitalmente."},
    {"ordem": 19, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em escrever código de baixo nível, programar em paralelo (CPU/GPU) e otimizar desempenho."},
    {"ordem": 20, "tipo": PerguntaTipo.PRATICA,
     "enunciado": "Gosto de / Tenho interesse em empreender, transformar uma ideia técnica em produto, startup ou negócio inovador."},
]

PESOS_POR_TRILHA: dict[str, list[float]] = {
    "Ciência de Dados": [
        0.4, 0.8, 1.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2,
        1.0, 0.5, 1.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.2, 0.3,
    ],
    "Inteligência Artificial": [
        0.4, 1.0, 0.2, 1.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.6,
        0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.2,
    ],
    "Redes e Segurança": [
        0.2, 0.2, 0.0, 0.0, 1.0, 1.0, 0.2, 0.0, 0.3, 0.3,
        0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.2, 0.0,
    ],
    "Engenharia de Software e Desenvolvimento Web": [
        0.3, 0.0, 0.3, 0.0, 0.2, 0.2, 1.0, 0.0, 0.0, 0.3,
        0.3, 0.0, 0.2, 0.0, 0.2, 1.0, 1.0, 0.0, 0.0, 0.8,
    ],
    "Visualização e Computação Gráfica": [
        0.4, 0.5, 0.0, 0.4, 0.0, 0.0, 0.0, 1.0, 0.2, 0.2,
        0.0, 0.4, 0.0, 0.0, 0.0, 0.2, 0.0, 1.0, 0.2, 0.0,
    ],
    "Processamento de Alto Desempenho": [
        0.9, 0.4, 0.0, 0.2, 0.3, 0.0, 0.2, 0.2, 1.0, 0.0,
        0.0, 0.3, 0.0, 0.3, 0.0, 0.0, 0.0, 0.2, 1.0, 0.0,
    ],
}


USERS_SEED = [
    {
        "email": "aluno1@ufrgs.br",
        "password": "aluno123",
        "nome": "Lucas Martins",
        "role": UserRole.ALUNO,
        "cartao_ufrgs": "00333331",
        "semestre_ingresso": "2023/2",
    },
    {
        "email": "aluno2@ufrgs.br",
        "password": "aluno123",
        "nome": "Mariana Burzlaff",
        "role": UserRole.ALUNO,
        "cartao_ufrgs": "00333332",
        "semestre_ingresso": "2024/1",
    },
    {
        "email": "aluno3@ufrgs.br",
        "password": "aluno123",
        "nome": "Pedro Diello",
        "role": UserRole.ALUNO,
        "cartao_ufrgs": "00333333",
        "semestre_ingresso": "2024/2",
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
        db.execute(delete(Solicitacao))
        db.execute(delete(PerguntaTrilhaPeso))
        db.execute(delete(Pergunta))
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
                    link_plano_ensino=row.get("link_plano_ensino") or None,
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

        perguntas: list[Pergunta] = []
        for data in PERGUNTAS_SEED:
            pergunta = Pergunta(
                enunciado=data["enunciado"],
                tipo=data["tipo"],
                ordem=data["ordem"],
            )
            db.add(pergunta)
            perguntas.append(pergunta)

        db.flush()

        trilhas_db = list(db.scalars(select(Trilha).order_by(Trilha.id)))
        pesos_default = [0.0] * len(perguntas)
        for trilha in trilhas_db:
            pesos = PESOS_POR_TRILHA.get(trilha.nome, pesos_default)
            for pergunta, peso in zip(perguntas, pesos):
                db.add(
                    PerguntaTrilhaPeso(
                        pergunta_id=pergunta.id,
                        trilha_id=trilha.id,
                        peso=peso,
                    )
                )

        alunos = list(
            db.scalars(
                select(User).where(User.role == UserRole.ALUNO).order_by(User.id)
            )
        )
        total_trilhas = len(trilhas_db)
        for idx, aluno_user in enumerate(alunos):
            candidatas = [
                trilhas_db[idx % total_trilhas],
                trilhas_db[(idx + 1) % total_trilhas],
            ]
            db.add(
                Solicitacao(
                    aluno_id=aluno_user.id,
                    status=SolicitacaoStatus.PENDENTE,
                    trilhas_candidatas=candidatas,
                )
            )

        db.commit()

        print(
            f"Seed concluído: {db.query(User).count()} usuários, "
            f"{db.query(Disciplina).count()} disciplinas, "
            f"{db.query(Trilha).count()} trilhas, "
            f"{db.query(Pergunta).count()} perguntas, "
            f"{db.query(PerguntaTrilhaPeso).count()} pesos pergunta-trilha, "
            f"{db.query(Solicitacao).count()} solicitações"
        )
        print("Usuários de teste:")
        for data in USERS_SEED:
            print(f"  {data['role'].value}: {data['email']} / {data['password']}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
