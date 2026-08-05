from fastapi import FastAPI

app = FastAPI()


@app.get("/", status_code=200)
async def root():
	return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", status_code=200)
async def health():
	return {"status": "ok"}

