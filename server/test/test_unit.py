import pytest
from pydantic import ValidationError

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
