#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

MODE="${1:-}"

usage() {
  cat <<EOF
Uso: ./server/run.sh <modo>

Modos:
  new        Apaga e recria o banco (tabelas vazias) antes de subir o servidor
  demo       Apaga, recria e popula o banco com os CSVs de data/ antes de subir
  existing   Sobe o servidor usando o banco existente

Exemplos:
  ./server/run.sh new        # começa do zero (banco vazio)
  ./server/run.sh demo       # banco populado a partir de data/*.csv
  ./server/run.sh existing   # mantém dados de runs anteriores
EOF
}

if [ ! -d .venv ]; then
  echo "Erro: ambiente virtual não encontrado em ./.venv"
  echo "Rode primeiro: ./server/setup.sh"
  exit 1
fi

case "$MODE" in
  new)
    echo "==> Recriando banco (tabelas vazias)..."
    rm -f server/trilha-cic.db
    .venv/bin/python -m server.init_db
    echo
    echo "Banco recriado. Para popular com dados de exemplo, em outro terminal rode:"
    echo "  .venv/bin/python -m server.seed"
    echo
    ;;
  demo)
    echo "==> Recriando banco e populando com data/*.csv..."
    rm -f server/trilha-cic.db
    .venv/bin/python -m server.init_db
    .venv/bin/python -m server.seed
    echo
    ;;
  existing)
    if [ ! -f server/trilha-cic.db ]; then
      echo "Erro: server/trilha-cic.db não existe."
      echo "Rode primeiro: ./server/run.sh new"
      exit 1
    fi
    echo "==> Usando banco existente em server/trilha-cic.db"
    ;;
  ""|--help|-h|help)
    usage
    exit 0
    ;;
  *)
    echo "Modo desconhecido: '$MODE'"
    echo
    usage
    exit 1
    ;;
esac

echo "==> Iniciando API em http://localhost:8000 (Ctrl+C para parar)"
echo "    Swagger UI: http://localhost:8000/docs"
.venv/bin/uvicorn server.main:app --reload --port 8000
