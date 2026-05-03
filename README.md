# TrilhaCiC

## Frontend

O frontend do projeto está na pasta `front-end/`.

### Requisitos

- Node.js
- npm

### Como rodar

Entre na pasta do frontend:

```bash
cd front-end
```

Instale as dependências:

```bash
npm install
```

Inicie o servidor de desenvolvimento:

```bash
npm start
```

O frontend está configurado para encaminhar as requisições da rota `trilhas/get`
para um backend local em `http://localhost:8000` por meio de proxy do Angular.
Se o seu backend usar outra porta, ajuste o arquivo:

```text
front-end/proxy.conf.json
```

Depois, abra no navegador:

```text
http://localhost:4200
```

### Build

Para gerar a versão de produção:

```bash
cd front-end
npm run build
```

## Server

O server do projeto está na pasta `server/`.

### Requisitos

- Python 3.10+
- pip (já incluso com o Python)

### Como rodar

Entre na pasta do projeto:

```bash
cd trilha-cic
```

Prepare o ambiente (cria `.venv` e instala dependências) — só na primeira vez:

```bash
./server/setup.sh
```

Suba o servidor escolhendo um dos modos:

```bash
./server/run.sh demo       # banco populado com data/*.csv (recomendado para demo)
./server/run.sh new        # banco vazio
./server/run.sh existing   # usa o banco existente
```

A API sobe em `http://localhost:8000`, mesma porta para a qual o frontend
está configurado (via `front-end/proxy.conf.json`). Para explorar os
endpoints de forma interativa (Swagger UI), abra:

```text
http://localhost:8000/docs
```
