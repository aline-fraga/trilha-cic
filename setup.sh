#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Erro: python3 não encontrado."
  echo "Instale com: brew install python3 (macOS) ou sudo apt install python3-venv (Linux)"
  exit 1
fi

echo "==> Python detectado: $(python3 --version)"

if [ ! -d .venv ]; then
  echo "==> Criando ambiente virtual em ./.venv ..."
  python3 -m venv .venv
else
  echo "==> ./.venv já existe — pulando criação"
fi

echo "==> Atualizando pip..."
.venv/bin/pip install --quiet --upgrade pip

echo "==> Instalando dependências de server/requirements.txt..."
.venv/bin/pip install -r server/requirements.txt

echo
echo "Setup concluído. Próximos passos:"
echo "  ./run.sh demo       # banco populado a partir de data/*.csv + servidor"
echo "  ./run.sh new        # banco vazio + servidor"
echo "  ./run.sh existing   # mantém dados atuais + servidor"
