.PHONY: up down logs seed demo test

up:
	docker compose -f infra/docker-compose.yml up -d --build

down:
	docker compose -f infra/docker-compose.yml down -v --remove-orphans

logs:
	docker compose -f infra/docker-compose.yml logs -f --tail=200

seed:
	docker compose exec mock-integrations python /app/seed.py || true

demo:
	docker compose exec orchestrator curl -s -X POST http://orchestrator:8000/incidents/simulate -H "Content-Type: application/json" -d '{"source":"servicenow","type":"patient_portal_login_failure"}' || true

test:
	docker compose -f infra/docker-compose.yml exec orchestrator pytest -q
