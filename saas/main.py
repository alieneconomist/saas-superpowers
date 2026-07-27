from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="saas-superpowers")

class Request(BaseModel):
    input: str
    options: dict = {}


@app.get("/health")
def health():
    return {"status": "ok", "service": __name__}

@app.get("/readyz")
def readyz():
    return {"status": "ready", "service": __name__}

@app.get("/")
def home():
    return {"name": "saas-superpowers", "description": "An agentic skills framework & software development methodology that works.", "source": "https://github.com/obra/superpowers"}

@app.post("/run")
def run(req: Request):
    # TODO: wrap the actual tool logic here
    return {"status": "prototype", "input": req.input, "message": "Coming soon"}
