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
    """Search this repo's README for matching entries."""
    query = (req.input or "").lower().strip()
    if not query:
        return {"status": "error", "message": "empty query"}
    from pathlib import Path as _P
    readme = _P(__file__).parent.parent / "README.md"
    try:
        text = readme.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"status": "no_data", "message": "README not found"}
    lines = text.splitlines()
    matches = []
    needle = query
    for i, line in enumerate(lines):
        if needle in line.lower() and ("[" in line or "*" in line or "-" in line):
            entry = line.strip()
            if 10 < len(entry) < 400:
                matches.append({"line": i + 1, "entry": entry})
            if len(matches) >= 15:
                break
    return {"status": "ok", "query": req.input, "matches": matches, "total": len(matches)}