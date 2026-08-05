# Stage 0 — Hello, server (~30 min)
# The scene: before a restaurant serves food, the doors have to open.

# Install your lane's tools (Node or Python — see the W2 resources, section 6).

# Follow your framework's official hello-world page (linked in the table above) to start a server on localhost — Express on port 3000, FastAPI on port 8000.

# Visit it in your browser. You should see your hello message.

# Checkpoint: curl -i http://localhost:3000/ (or :8000/) returns status code 200 and your message.

# Commit: Stage 0: hello server


from fastapi import FastAPI

app = FastAPI()

@app.get("/",status_code=200)
async def hello_server():
    return {
        "status_code":200,
        "message":"Welcome to FASTAPI backend"
    }