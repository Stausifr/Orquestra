FROM python:3.11-slim
WORKDIR /app
COPY ../../pyproject.toml ./
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy pydantic requests redis rq alembic opentelemetry-api opentelemetry-sdk reportlab jsonschema
COPY . .
CMD ["python", "worker.py"]
