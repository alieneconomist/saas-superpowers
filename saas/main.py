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
    if not readme.exists():
        # Try lowercase
        for alt in ('readme.md', 'Readme.md', 'awesome.md', 'AWESOME.md'):
            p = _P(__file__).parent.parent / alt
            if p.exists():
                readme = p
                break
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

@app.get("/suggest")
def suggest():
    """Return popular categories from this repo."""
    from pathlib import Path as _P
    candidates = ['README.md', 'readme.md', 'awesome.md']
    text = ''
    for c in candidates:
        p = _P(__file__).parent.parent / c
        if p.exists():
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
                break
            except Exception:
                pass
    if not text:
        return {"suggestions": ["python", "async", "docker", "api", "http"], "total_sections": 0}
    sections = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## ") and "Table of Contents" not in s and "Sponsors" not in s and len(s) < 80:
            name = s[3:].strip()
            if name and name not in sections:
                sections.append(name)
        elif s.startswith("### ") and "Table of Contents" not in s and len(s) < 80:
            name = s[4:].strip()
            if name and name not in sections:
                sections.append(name)
    return {"suggestions": sections[:30], "total_sections": len(sections)}


@app.get("/stats")
def stats():
    """Return basic stats about this repo's readme."""
    from pathlib import Path as _P
    candidates = ['README.md', 'readme.md', 'awesome.md']
    text = ''
    for c in candidates:
        p = _P(__file__).parent.parent / c
        if p.exists():
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
                break
            except Exception:
                pass
    if not text:
        return {"error": "readme not found"}
    lines = text.splitlines()
    return {
        "lines": len(lines),
        "sections": sum(1 for l in lines if l.startswith("## ") or l.startswith("### ")),
        "links": sum(1 for l in lines if "](" in l),
        "size_kb": round(len(text) / 1024, 1),
    }
