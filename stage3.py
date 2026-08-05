from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Body

app = FastAPI()

# In-memory tasks
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


@app.post("/tasks")
async def create_task(payload: dict = Body(...)):
    title = payload.get("title") if isinstance(payload, dict) else None
    if not title or not isinstance(title, str) or title.strip() == "":
        return JSONResponse(status_code=400, content={"error": "title is required"})

    next_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": next_id, "title": title.strip(), "done": False}
    tasks.append(new_task)
    return JSONResponse(status_code=201, content=new_task)
