from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, Response

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple task API with Swagger UI documentation available at /docs",
)

# In-memory tasks
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write tests", "done": True},
    {"id": 3, "title": "Read book", "done": False},
]


@app.get("/", status_code=200)
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", status_code=200)
async def health():
    return {"status": "ok"}


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


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, payload: dict = Body(...)):
    if not isinstance(payload, dict) or not payload:
        return JSONResponse(status_code=400, content={"error": "request body must include title and/or done"})

    title = payload.get("title")
    done = payload.get("done") if "done" in payload else None

    if title is None and "done" not in payload:
        return JSONResponse(status_code=400, content={"error": "request body must include title and/or done"})

    if title is not None:
        if not isinstance(title, str) or title.strip() == "":
            return JSONResponse(status_code=400, content={"error": "title must be a non-empty string"})

    if "done" in payload and not isinstance(done, bool):
        return JSONResponse(status_code=400, content={"error": "done must be true or false"})

    for idx, t in enumerate(tasks):
        if t["id"] == task_id:
            updated_task = t.copy()
            if title is not None:
                updated_task["title"] = title.strip()
            if "done" in payload:
                updated_task["done"] = done
            tasks[idx] = updated_task
            return updated_task

    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    for idx, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(idx)
            return Response(status_code=204)
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("stage5:app", host="127.0.0.1", port=8000, reload=True)
