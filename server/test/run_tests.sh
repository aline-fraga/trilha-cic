#!/usr/bin/env bash
#
# Roda toda a bateria de testes do backend TrilhaCiC:
#   1. Unitários + integração (pytest)
#   2. Carga/performance (Locust) — sobe um servidor temporário e o derruba ao final
#
# Uso:
#   ./server/test/run_tests.sh            # roda tudo (pytest + load)
#   ./server/test/run_tests.sh pytest     # só unitários + integração
#   ./server/test/run_tests.sh load       # só o teste de carga
#
# Parâmetros do load ajustáveis por variável de ambiente:
#   LOAD_USERS (10)  LOAD_SPAWN (2)  LOAD_RUNTIME (15s)  LOAD_PORT (8001)
#
set -euo pipefail

cd "$(dirname "$0")/../.."   # raiz do projeto (trilha-cic)

PY=".venv/bin/python"
LOCUST=".venv/bin/locust"
MODE="${1:-all}"

if [ ! -x "$PY" ]; then
  echo "Erro: ambiente virtual não encontrado em ./.venv — rode ./server/setup.sh primeiro." >&2
  exit 1
fi

run_pytest() {
  echo "==> Unitários + integração (pytest)"
  "$PY" -m pytest server/test -v
}

run_load() {
  local port="${LOAD_PORT:-8001}"
  local host="http://localhost:${port}"
  echo "==> Carga/performance (Locust) em ${host}"

  "$PY" -m uvicorn server.main:app --port "$port" >/tmp/trilha-load-server.log 2>&1 &
  server_pid=$!   # global de propósito: o trap EXIT precisa enxergá-lo após o retorno

  trap 'rc=$?; kill "$server_pid" 2>/dev/null || true; pkill -P "$server_pid" 2>/dev/null || true; exit $rc' EXIT

  echo "    Aguardando o servidor (pid $server_pid) ficar pronto..."
  for _ in $(seq 1 30); do
    if curl -sf "${host}/docs" >/dev/null 2>&1; then
      break
    fi
    sleep 0.5
  done
  if ! curl -sf "${host}/docs" >/dev/null 2>&1; then
    echo "Erro: servidor não respondeu em ${host}. Veja /tmp/trilha-load-server.log" >&2
    exit 1
  fi

  local resultado="${LOAD_RESULTS:-server/test/load_results.txt}"
  echo "    Resultados serão salvos em ${resultado}"
  # Locust escreve as estatísticas no stderr; `2>&1` garante que o relatório
  # completo (tabelas + percentis) chegue ao arquivo e ao terminal.
  "$LOCUST" -f server/test/test_load.py --host "$host" \
    --users "${LOAD_USERS:-10}" --spawn-rate "${LOAD_SPAWN:-2}" \
    --run-time "${LOAD_RUNTIME:-15s}" --headless --exit-code-on-error 1 2>&1 \
    | tee "$resultado"
}

case "$MODE" in
  pytest) run_pytest ;;
  load)   run_load ;;
  all)    run_pytest; echo; run_load ;;
  *)
    echo "Modo desconhecido: '$MODE' (use: pytest | load | all)" >&2
    exit 1
    ;;
esac

echo
echo "==> Concluído."
