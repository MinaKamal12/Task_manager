from fastapi import FastAPI
from app.api.tasks import router as tasks_router

app = FastAPI(
    title="Task Manager API",
    description="A simple Task Manager REST API for an end-to-end DevOps project.",
    version="1.0.0",
)

app.include_router(tasks_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
