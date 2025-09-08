# Orquestra MVP

Vendor-neutral AI orchestration & governance platform.

## Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11
- Make

## Codespaces Quickstart
1. `cp .env.example .env`
2. **Run Stack** task or `make up`
3. Open Ports tab → 3000 (Dashboard), 8000 (API), 16686 (Jaeger)
4. **Trigger Demo** task or `make demo`
5. Approve in **Approvals**, view **Traces**, download **Audit** JSON/PDF

Troubleshooting: check Ports tab, `make logs`, `docker compose ps`.

## Commands
```sh
make up      # start stack
make seed    # seed mock data
make demo    # trigger sample incident
make test    # run tests
```

## URLs
- Dashboard: http://localhost:3000
- Orchestrator API docs: http://localhost:8000/docs
- Jaeger UI: http://localhost:16686
