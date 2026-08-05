from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# In-memory "database" of tasks
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write tests", "done": True},
    {"id": 3, "title": "Read book", "done": False},
]


@app.get("/tasks", status_code=200)
async def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
