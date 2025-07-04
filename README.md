# Media utility

Originally made for automatic compression and transcription of lecture footage \
Api docs can be found at `backend/README.md` and `backend/openapi.yaml`

## How to run

See `backend/README.md` if you only want to run the api

### No Docker

```bash
git clone https://github.com/om3lette/Media-api.git
```

#### Frontend
```bash
npm i && npm run dev
```

#### Backend

See `backend/README.md`

### Docker

```bash
git clone https://github.com/om3lette/Media-api.git && \
cd Media-api && \
docker compose build && docker compose up -d
```

Visit `localhost:80` or `localhost:443` to access site
