# trilha-cic

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
para um backend local em `http://localhost:8080` por meio de proxy do Angular.
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
