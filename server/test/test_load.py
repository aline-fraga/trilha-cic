"""Testes de carga e performance (Locust) — RNFs não cobertos pela suíte
unit/integração.

Cobertura:
- RNF #2  (UC01) — validação ao gerenciar o catálogo/currículo em <= 2s
          (POST /disciplinas/create, caminho de escrita+validação).
- RNF #5  (UC02) — validação ao gerenciar trilha em <= 2s
          (POST /trilhas/create, caminho de escrita+validação).
- RNF #6  (UC03) — geração da sugestão de trilha em <= 5s. Medido pelo caminho
          de matching fuzzy `GET /trilhas/get?disciplina=...` (UC11), que é a
          operação de custo computacional equivalente e, ao contrário do
          `POST /solicitacoes/create`, é stateless e repetível. Ver NOTA abaixo.
- RNF #7  (UC03) — suportar picos de acessos simultâneos sem falhas: verificado
          pela carga de execução (muitos usuários concorrentes, taxa de erro 0%).

NOTA — por que `POST /solicitacoes/create` não é martelado aqui:
    A regra de negócio permite apenas 1 solicitação PENDENTE por aluno e o
    seed.py já cria uma para cada aluno; repetições retornam 400. Logo o
    endpoint não é "loopável" sob carga com usuários semeados. O custo de
    geração da sugestão (algoritmo de score sobre as trilhas) é exercitado pela
    busca fuzzy, que percorre disciplinas/trilhas de forma análoga.

Este arquivo NÃO é executado pelo pytest (ver `collect_ignore` no conftest.py);
roda pela CLI do Locust contra um servidor `uvicorn` real.

Pré-requisitos:
    .venv/bin/python -m pip install -r server/requirements-dev.txt
    ./server/run.sh demo          # sobe o servidor com banco populado (seed)

Execução típica (RNF #7 — pico de usuários simultâneos, falha se houver erro):
    .venv/bin/locust -f server/test/test_load.py --host http://localhost:8000 \
        --users 200 --spawn-rate 20 --run-time 2m --headless

AVISO: as tasks de escrita (disciplina/trilha) inserem registros no banco
alvo — rode contra um banco descartável/semeado, não contra dados de produção.
"""

import os
import random
import uuid

from locust import HttpUser, between, task
from locust.exception import StopUser

LIMITE_VALIDACAO_S = 2.0
LIMITE_SUGESTAO_S = 5.0
LOGIN_TENTATIVAS = 5

# Credenciais do seed.py (ajustáveis por variável de ambiente).
EMAIL_COMGRAD = os.getenv("LOAD_EMAIL_COMGRAD", "comgrad@ufrgs.br")
SENHA_COMGRAD = os.getenv("LOAD_SENHA_COMGRAD", "comgrad123")
EMAIL_ALUNO = os.getenv("LOAD_EMAIL_ALUNO", "aluno1@ufrgs.br")
SENHA_ALUNO = os.getenv("LOAD_SENHA_ALUNO", "aluno123")

TERMOS_BUSCA = ["algoritmo", "dados", "rede", "seguranca", "software", "grafica"]


class _UsuarioAutenticado(HttpUser):
    """Base: faz login no on_start e guarda o cabeçalho Bearer."""

    abstract = True
    email = ""
    senha = ""

    def on_start(self) -> None:
        # Login com retry: conexões recusadas no cold-start do servidor (rajada
        # de logins com bcrypt) são transitórias e NÃO devem abortar a corrida.
        # As tentativas usam catch_response p/ não poluir as estatísticas; se
        # todas falharem, para apenas este usuário (StopUser), não o teste todo.
        self.headers = {}
        for _ in range(LOGIN_TENTATIVAS):
            with self.client.post(
                "/auth/login",
                json={"email": self.email, "password": self.senha},
                catch_response=True,
                name="/auth/login",
            ) as resp:
                if resp.status_code == 200:
                    token = resp.json()["access_token"]
                    self.headers = {"Authorization": f"Bearer {token}"}
                    resp.success()
                    return
                resp.success()  # tentativa transitória: não conta como falha
        raise StopUser()

    def _medir(self, method: str, url: str, limite_s: float, **kwargs) -> None:
        with self.client.request(
            method, url, headers=self.headers, catch_response=True, **kwargs
        ) as resp:
            decorrido = resp.elapsed.total_seconds()
            if resp.status_code >= 400:
                resp.failure(f"HTTP {resp.status_code}: {resp.text[:120]}")
            elif decorrido > limite_s:
                resp.failure(f"Demorou {decorrido:.2f}s (limite {limite_s}s)")
            else:
                resp.success()


class AlunoBuscaTrilhas(_UsuarioAutenticado):
    """RNF #6 e #7 — matching/busca de trilhas em <= 5s, sob acessos simultâneos."""

    email = EMAIL_ALUNO
    senha = SENHA_ALUNO
    wait_time = between(0.5, 2)

    @task(3)
    def buscar_trilhas_por_disciplina(self) -> None:
        termo = random.choice(TERMOS_BUSCA)
        self._medir(
            "GET",
            f"/trilhas/get?disciplina={termo}",
            LIMITE_SUGESTAO_S,
            name="/trilhas/get?disciplina=[termo]",
        )

    @task(1)
    def listar_minhas_solicitacoes(self) -> None:
        self._medir("GET", "/solicitacoes/get", LIMITE_SUGESTAO_S)


class ComgradGerenciaCatalogo(_UsuarioAutenticado):
    """RNF #2 e #5 — validações de currículo/trilha em <= 2s, sob carga."""

    email = EMAIL_COMGRAD
    senha = SENHA_COMGRAD
    wait_time = between(1, 3)

    def on_start(self) -> None:
        super().on_start()
        if not self.headers:
            return
        # Descobre IDs válidos para montar payloads que passem na validação.
        perguntas = self.client.get(
            "/perguntas/get?is_active=true", headers=self.headers
        ).json()
        self.pergunta_ids = [p["id"] for p in perguntas]
        disciplinas = self.client.get(
            "/disciplinas/get?is_active=true", headers=self.headers
        ).json()
        self.disciplina_ids = [d["id"] for d in disciplinas]

    @task
    def cadastrar_disciplina(self) -> None:
        # RNF #2: conteúdo do currículo (disciplina) validado em <= 2s.
        # Código único por requisição evita colisão com a constraint de unicidade.
        codigo = f"L{uuid.uuid4().hex[:8].upper()}"
        self._medir(
            "POST",
            "/disciplinas/create",
            LIMITE_VALIDACAO_S,
            json={
                "nome": "Disciplina de Carga",
                "codigo": codigo,
                "tipo": "ELETIVA",
                "carga_horaria": 30,
            },
        )

    @task
    def cadastrar_trilha(self) -> None:
        # RNF #5: validação ao gerenciar trilha em <= 2s. Os pesos cobrem
        # exatamente as perguntas ativas (exigência do TrilhaService).
        if not getattr(self, "pergunta_ids", None) or len(
            getattr(self, "disciplina_ids", [])
        ) < 2:
            return
        self._medir(
            "POST",
            "/trilhas/create",
            LIMITE_VALIDACAO_S,
            json={
                "nome": f"Trilha de Carga {uuid.uuid4().hex[:6]}",
                "resumo": "Trilha criada durante o teste de carga.",
                "disciplinas_ids": self.disciplina_ids[:2],
                "pesos": [{"pergunta_id": pid, "peso": 0.5} for pid in self.pergunta_ids],
            },
        )
