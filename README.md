# Task API

A simple FastAPI task management service built in stages 0–5, now backed by SQLite for persistent data storage.

This repository contains a REST API with persistent task storage, full CRUD operations, health checks, and Swagger UI documentation.

## Database: SQLite

### Why SQLite?

- **No server required**: SQLite is embedded; no separate database process to manage.
- **Persistent storage**: Data survives application restarts.
- **Simple and lightweight**: Perfect for learning and small-scale applications.
- **Zero configuration**: Just a file on disk (`tasks.db`).

### Database Location

The database file is stored at:

```
./tasks.db
```

This file is created automatically when the application starts. It persists across restarts.

### Example SQL Query

Here's a sample query to fetch all tasks from the database:

```sql
SELECT id, title, done FROM tasks;
```

Result:

```
id | title         | done
1  | Buy milk      | 0
2  | Write tests   | 1
3  | Read book     | 0
```

![SQLite database viewer](sqlite_exploring.png)

## Install & Run

### Prerequisites

- Python 3.7+ (included in the virtual environment `./env/`)
- Uvicorn (FastAPI web server, pre-installed)

### Start the server

From the repository root, run:

```bash
./env/bin/python stage5.py
```

The server will:

1. Initialize `tasks.db` if it doesn't exist
2. Create the `tasks` table if missing
3. Seed 3 example tasks (only on first run)
4. Start listening on `http://127.0.0.1:8000`

### Access the API

Once running, open:

- **Swagger UI (interactive docs)**: `http://127.0.0.1:8000/docs`
- **OpenAPI specification**: `http://127.0.0.1:8000/openapi.json`

## Database Viewer

![Database viewer](task_content.png)

## Endpoints

| Method | Path          | Description                                      |
| ------ | ------------- | ------------------------------------------------ |
| GET    | `/`           | API metadata and available endpoints             |
| GET    | `/health`     | Health check with `status: ok`                   |
| GET    | `/tasks`      | List all tasks from database                     |
| GET    | `/tasks/{id}` | Get a single task by id                          |
| POST   | `/tasks`      | Create a new task with JSON `{ "title": "..." }` |
| PUT    | `/tasks/{id}` | Update a task's `title` and/or `done` fields     |
| DELETE | `/tasks/{id}` | Delete a task and return `204 No Content`        |

## Example curl output

```bash
curl -i http://127.0.0.1:8000/
```

Example response:

```
HTTP/1.1 200 OK
content-length: 58
content-type: application/json

{"name":"Task API","version":"1.0","endpoints":["/tasks"]}
```

## Swagger UI

![Swagger UI screenshot](swaggerUI.png)

## Project Structure

- `stage0.py` — Hello server
- `stage1.py` — Root and health endpoints
- `stage2.py` — Read endpoints with 404 handling
- `stage3.py` — Create with validation
- `stage4.py` — Full CRUD operations
- `stage5.py` — **Main entrypoint** with SQLite and Swagger UI
- `tasks.db` — SQLite database file (auto-created)
- `env/` — Python virtual environment with dependencies
