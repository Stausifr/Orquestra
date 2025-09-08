.PHONY: up down logs seed demo fmt lint test cov clean

up:
	docker compose -f infra/docker-compose.yml up -d --build
	echo "Dashboard: http://localhost:3000"
	echo "API: http://localhost:8000/docs"
	echo "Jaeger: http://localhost:16686"

down:
	docker compose -f infra/docker-compose.yml down -v --remove-orphans

logs:
	docker compose -f infra/docker-compose.yml logs -f --tail=200

seed:
	docker compose -f infra/docker-compose.yml exec mock-integrations python /app/seed.py || true

demo:
	docker compose -f infra/docker-compose.yml exec orchestrator curl -s -X POST http://orchestrator:8000/incidents/simulate -H "Content-Type: application/json" -d '{"source":"servicenow","type":"patient_portal_login_failure"}' || true

fmt:
	black .
	isort .

lint:
	ruff .

test:
	docker compose -f infra/docker-compose.yml exec orchestrator pytest -q

cov:
	docker compose -f infra/docker-compose.yml exec orchestrator pytest --cov=pkg --cov=services -q

clean:
	docker compose -f infra/docker-compose.yml down -v --remove-orphans
	rm -rf __pycache__ */__pycache__ .pytest_cache storage/*.json storage/*.pdf
