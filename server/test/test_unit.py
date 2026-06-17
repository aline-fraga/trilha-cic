import pytest
from pydantic import ValidationError

from server.schemas.chamado import AbrirChamadoRequest, ChamadoResponder
from server.schemas.sugestao_trilha import SugestaoTrilhaCreate

LIMITE_MAXIMO_DISCIPLINAS = 4


class TestRNF10LimiteDisciplinasSugestao:
    def test_aceita_uma_disciplina(self):
        sugestao = SugestaoTrilhaCreate(nome="Trilha X", disciplinas_ids=[1])
        assert sugestao.disciplinas_ids == [1]

    def test_aceita_o_maximo_de_disciplinas(self):
        ids = list(range(1, LIMITE_MAXIMO_DISCIPLINAS + 1))
        sugestao = SugestaoTrilhaCreate(nome="Trilha X", disciplinas_ids=ids)
        assert len(sugestao.disciplinas_ids) == LIMITE_MAXIMO_DISCIPLINAS

    def test_rejeita_lista_vazia(self):
        with pytest.raises(ValidationError):
            SugestaoTrilhaCreate(nome="Trilha X", disciplinas_ids=[])

    def test_rejeita_acima_do_maximo(self):
        ids = list(range(1, LIMITE_MAXIMO_DISCIPLINAS + 2))  # 5 disciplinas
        with pytest.raises(ValidationError):
            SugestaoTrilhaCreate(nome="Trilha X", disciplinas_ids=ids)


class TestRNF10NomeSugestao:
    def test_rejeita_nome_vazio(self):
        with pytest.raises(ValidationError):
            SugestaoTrilhaCreate(nome="", disciplinas_ids=[1])

    def test_rejeita_nome_acima_de_150_caracteres(self):
        with pytest.raises(ValidationError):
            SugestaoTrilhaCreate(nome="a" * 151, disciplinas_ids=[1])


class TestRNF12LimiteComentarioChamado:
    """RNF #12 (UC07): comentário do chamado deve ter entre 50 e 2000 chars.

    A regra vive em `AbrirChamadoRequest` (corpo do POST /chamados), não no
    `ChamadoCreate` compartilhado — então os chamados automáticos não são afetados.
    """

    BASE = {"assunto": "Revisão de trilha", "tipo": "TRILHA_REJEITADA"}

    def test_aceita_limite_inferior_50(self):
        req = AbrirChamadoRequest(**self.BASE, mensagem="a" * 50)
        assert len(req.mensagem) == 50

    def test_aceita_limite_superior_2000(self):
        req = AbrirChamadoRequest(**self.BASE, mensagem="a" * 2000)
        assert len(req.mensagem) == 2000

    def test_rejeita_abaixo_de_50(self):
        with pytest.raises(ValidationError):
            AbrirChamadoRequest(**self.BASE, mensagem="a" * 49)

    def test_rejeita_acima_de_2000(self):
        with pytest.raises(ValidationError):
            AbrirChamadoRequest(**self.BASE, mensagem="a" * 2001)


class TestRespostaChamado:
    def test_aceita_resposta_nao_vazia(self):
        req = ChamadoResponder(resposta="Solicitação analisada e respondida.")
        assert req.resposta == "Solicitação analisada e respondida."

    def test_rejeita_resposta_vazia(self):
        with pytest.raises(ValidationError):
            ChamadoResponder(resposta="")
