FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy pydantic requests redis rq alembic opentelemetry-api opentelemetry-sdk reportlab jsonschema
COPY services/mock-integrations/ ./
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9000"]
