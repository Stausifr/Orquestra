# Orquestra MVP

A vendor-neutral AI orchestration & governance platform.

## Prerequisites
- Docker
- Node.js LTS
- Python 3.11
- Make

## Quickstart
```sh
make up
make seed
make demo
```

Run tests:
```sh
make test
```

## URLs
- Dashboard: http://localhost:3000
- Orchestrator API docs: http://localhost:8000/docs
- Jaeger UI: http://localhost:16686

## Demo Walkthrough
1. `make up` to start the stack.
2. Open the dashboard and observe pending approval.
3. Approve the workflow to let it continue and finish.
