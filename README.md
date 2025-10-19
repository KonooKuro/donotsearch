## Prerequisites
- Docker and Docker Compose
- (Optionally) Python 3.10+ for local tools and scripts

## Quick Start (Docker Compose)
```bash
# From repository root
docker compose up -d --build
# Health check (replace port/path if different)
curl -fsS http://127.0.0.1:5000/api/healthz || curl -fsS http://127.0.0.1:5000/healthz
```

## Tests and Coverage
```bash
# Run inside the application container
docker compose exec -it $(docker compose ps --services | head -n1) sh -lc '
  pip install -U pip pytest pytest-cov &&   pytest -q || true &&   pytest --cov=. --cov-report=term-missing --cov-report=html:htmlcov
'
# Coverage HTML will be at ./htmlcov/index.html in the container
```

## API (typical endpoints)
- `GET /api/healthz` (or `/healthz`)
- `GET /api/get-watermarking-methods`
- `POST /api/upload-document`
- `POST /api/create-watermark/<doc_id>`
- `POST /api/read-watermark/<doc_id>`
- `GET /api/list-versions/<doc_id>`
- `GET /api/list-all-versions`
- `POST /api/rmap-initiate`
- `POST /api/rmap-get-link`

## Deployment (Compose)
```bash
docker compose up -d --build
docker compose logs -f
```
