"""Testes de integração — exercitam os endpoints reais (Controller -> Service ->
Repository) contra um banco SQLite in-memory.

Cobertura:
- RNF #1  (UC01) — edição do catálogo é exclusiva da COMGRAD; ALUNO/ADMIN são
          barrados (403). Verificado via endpoints de Disciplina, que é o
          conteúdo gerenciado do currículo e onde a regra está implementada.
- RNF #4  (UC02) — exclusão de trilha é lógica (soft delete): o registro
          permanece no banco com `is_active=False` e some das listagens.
- RNF #9  (UC13) — disciplinas inativas não podem ser selecionadas na sugestão
          de nova trilha (retorna 400).
- RNF #11 (UC07) — o chamado grava automaticamente o aluno (a partir do token,
          não do corpo da requisição) e a data/hora de criação.
"""

from server.models.disciplina import Disciplina
from server.models.enums import DisciplinaTipo, UserRole
from server.models.trilha import Trilha


def _nova_disciplina(db, codigo: str, *, ativa: bool = True) -> Disciplina:
    disciplina = Disciplina(
        nome=f"Disciplina {codigo}",
        codigo=codigo,
        tipo=DisciplinaTipo.OBRIGATORIA,
        carga_horaria=60,
        is_active=ativa,
    )
    db.add(disciplina)
    db.commit()
    db.refresh(disciplina)
    return disciplina


class TestRNF1EdicaoExclusivaComgrad:
    PAYLOAD = {
        "nome": "Banco de Dados",
        "codigo": "INF01145",
        "tipo": "OBRIGATORIA",
        "carga_horaria": 60,
    }

    def test_comgrad_pode_cadastrar(self, client, criar_usuario, auth_header):
        comgrad = criar_usuario(UserRole.COMGRAD)
        resp = client.post(
            "/disciplinas/create",
            json=self.PAYLOAD,
            headers=auth_header(comgrad),
        )
        assert resp.status_code == 201
        assert resp.json()["codigo"] == "INF01145"

    def test_aluno_nao_pode_cadastrar(self, client, criar_usuario, auth_header):
        aluno = criar_usuario(UserRole.ALUNO)
        resp = client.post(
            "/disciplinas/create",
            json=self.PAYLOAD,
            headers=auth_header(aluno),
        )
        assert resp.status_code == 403

    def test_admin_nao_pode_cadastrar(self, client, criar_usuario, auth_header):
        admin = criar_usuario(UserRole.ADMIN)
        resp = client.post(
            "/disciplinas/create",
            json=self.PAYLOAD,
            headers=auth_header(admin),
        )
        assert resp.status_code == 403

    def test_sem_token_e_barrado(self, client):
        resp = client.post("/disciplinas/create", json=self.PAYLOAD)
        assert resp.status_code in (401, 403)


class TestRNF4SoftDeleteTrilha:
    def test_exclusao_marca_inativa_e_preserva_registro(
        self, client, db_session
    ):
        disciplina = _nova_disciplina(db_session, "INF01202")
        trilha = Trilha(
            nome="Sistemas de Computação",
            resumo="Trilha de teste",
            disciplinas=[disciplina],
        )
        db_session.add(trilha)
        db_session.commit()
        db_session.refresh(trilha)
        trilha_id = trilha.id

        resp = client.delete(f"/trilhas/delete/{trilha_id}")
        assert resp.status_code == 204

        # O registro continua no banco, apenas inativado (exclusão lógica).
        persistida = db_session.get(Trilha, trilha_id)
        assert persistida is not None
        assert persistida.is_active is False

    def test_trilha_inativa_some_da_listagem(self, client, db_session):
        disciplina = _nova_disciplina(db_session, "INF01203")
        trilha = Trilha(
            nome="Trilha Removível",
            resumo="Trilha de teste",
            disciplinas=[disciplina],
        )
        db_session.add(trilha)
        db_session.commit()
        db_session.refresh(trilha)
        trilha_id = trilha.id

        client.delete(f"/trilhas/delete/{trilha_id}")

        listadas = client.get("/trilhas/get").json()
        assert all(t["id"] != trilha_id for t in listadas)


class TestRNF9DisciplinaInativaNaoSelecionavel:
    def test_sugestao_com_disciplina_inativa_e_rejeitada(
        self, client, db_session, criar_usuario, auth_header
    ):
        aluno = criar_usuario(UserRole.ALUNO)
        inativa = _nova_disciplina(db_session, "INF99999", ativa=False)

        resp = client.post(
            "/sugestoes-trilha/create",
            json={"nome": "Trilha Nova", "disciplinas_ids": [inativa.id]},
            headers=auth_header(aluno),
        )
        assert resp.status_code == 400

    def test_sugestao_com_disciplina_ativa_e_aceita(
        self, client, db_session, criar_usuario, auth_header
    ):
        aluno = criar_usuario(UserRole.ALUNO)
        ativa = _nova_disciplina(db_session, "INF01202")

        resp = client.post(
            "/sugestoes-trilha/create",
            json={"nome": "Trilha Nova", "disciplinas_ids": [ativa.id]},
            headers=auth_header(aluno),
        )
        assert resp.status_code == 201


class TestRNF11AutofillChamado:
    def test_chamado_grava_aluno_do_token_e_data_automaticos(
        self, client, criar_usuario, auth_header
    ):
        aluno = criar_usuario(UserRole.ALUNO)

        # O corpo NÃO informa aluno_id nem data — devem ser preenchidos pelo sistema.
        resp = client.post(
            "/chamados",
            json={
                "assunto": "Preciso de ajuda",
                "mensagem": "Rejeitei a trilha sugerida e gostaria de orientação.",
                "tipo": "TRILHA_REJEITADA",
            },
            headers=auth_header(aluno),
        )

        assert resp.status_code == 201
        corpo = resp.json()
        assert corpo["aluno_id"] == aluno.id  # associado pelo token, não pelo cliente
        assert corpo["status"] == "ABERTO"
        assert corpo["created_at"]  # data/hora preenchida automaticamente
