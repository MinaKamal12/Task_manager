# Task Manager API

A simple production-style REST API built with FastAPI and PostgreSQL.

This project intentionally contains **application code only**. Docker, CI/CD,
deployment, reverse proxy, monitoring, and other DevOps components are left
for the DevOps implementation.

## Features

- Create tasks
- List tasks with pagination
- Get a task by ID
- Update tasks
- Delete tasks
- Health check
- PostgreSQL persistence
- Alembic database migrations
- Automated API tests
- OpenAPI/Swagger documentation

## Requirements

- Python 3.12+
- PostgreSQL 14+

## Local setup

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a PostgreSQL database:

```sql
CREATE DATABASE task_manager;
```

Create your environment file:

```bash
cp .env.example .env
```

Update `DATABASE_URL` in `.env` if necessary.

Run migrations:

```bash
alembic upgrade head
```

Start the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

## API

### Health

```http
GET /health
```

### Create task

```http
POST /api/v1/tasks
Content-Type: application/json

{
  "title": "Learn Docker",
  "description": "Containerize the application"
}
```

### List tasks

```http
GET /api/v1/tasks
GET /api/v1/tasks?skip=0&limit=10
```

### Get task

```http
GET /api/v1/tasks/{id}
```

### Update task

```http
PUT /api/v1/tasks/{id}
Content-Type: application/json

{
  "completed": true
}
```

### Delete task

```http
DELETE /api/v1/tasks/{id}
```

## Run tests

```bash
pytest
```

## Suggested DevOps progression

The application is intentionally ready for you to add:

1. Docker
2. Docker Compose
3. GitLab repository
4. GitLab CI pipeline
5. Container registry
6. Automated deployment
7. Nginx/reverse proxy
8. HTTPS
9. Prometheus/Grafana
10. Kubernetes as a second phase
