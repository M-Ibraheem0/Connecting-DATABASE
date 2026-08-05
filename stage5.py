import sqlite3
from pathlib import Path

from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, Response

DATABASE_PATH = Path(__file__).resolve().parent / "tasks.db"

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple task API with Swagger UI documentation available at /docs",
)


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_task(row):
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"]) }


def initialize_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN NOT NULL)"
        )
        count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                [
                    ("Buy milk", 0),
                    ("Write tests", 1),
                    ("Read book", 0),
                ],
            )
            conn.commit()


@app.on_event("startup")
async def on_startup():
    initialize_database()


@app.get("/", status_code=200)
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", status_code=200)
async def health():
    return {"status": "ok"}


@app.get("/tasks", status_code=200)
async def list_tasks():
    with get_connection() as conn:
        rows = conn.execute("SELECT id, title, done FROM tasks").fetchall()
        return [row_to_task(row) for row in rows]


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if row:
            return row_to_task(row)
    return JSONResponse(status_code=404, content={"error": "Task not found"})


@app.post("/tasks")
async def create_task(payload: dict = Body(...)):
    title = payload.get("title") if isinstance(payload, dict) else None
    if not title or not isinstance(title, str) or title.strip() == "":
        return JSONResponse(status_code=400, content={"error": "title is required"})

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (title.strip(), 0),
        )
        conn.commit()
        task_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return JSONResponse(status_code=201, content=row_to_task(row))


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

    updates = []
    params = []
    if title is not None:
        updates.append("title = ?")
        params.append(title.strip())
    if "done" in payload:
        updates.append("done = ?")
        params.append(int(done))

    if not updates:
        return JSONResponse(status_code=400, content={"error": "request body must include title and/or done"})

    params.append(task_id)
    with get_connection() as conn:
        cursor = conn.execute(
            f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", tuple(params)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return row_to_task(row)


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("stage5:app", host="127.0.0.1", port=8000, reload=True)
