.PHONY: up down seed demo fmt lint test cov clean

up:
docker-compose -f infra/docker-compose.yml up -d --build
echo "Dashboard: http://localhost:3000"
echo "API: http://localhost:8000/docs"
echo "Jaeger: http://localhost:16686"

down:
docker-compose -f infra/docker-compose.yml down

seed:
python services/mock-integrations/seed.py

demo:
curl -X POST http://localhost:8000/incidents/simulate
echo "Open http://localhost:3000 to approve"

fmt:
black .
isort .

lint:
ruff .

test:
pytest -q

cov:
pytest --cov=pkg --cov=services -q

clean:
rm -rf __pycache__ */__pycache__ .pytest_cache storage/*.json storage/*.pdf
