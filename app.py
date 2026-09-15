from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.requests import Request

from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi import FastAPI,HTTPException

from backend import run_workflow

base_dir = Path(__file__).resolve().parent


app = FastAPI(title='self-correcting Multi agent Demo')
app.mount("/static", StaticFiles(directory=base_dir/ 'static'),name = 'static')
templates = Jinja2Templates(directory=base_dir/ "templates")

class RunRequest(BaseModel):
    topic : str = Field(min_length = 2, max_length=200)

@app.get("/", response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse(
        request = request,
        name = 'index.html',
        context = {'example_topic' : "What is an AI agent"}
    )

@app.post("/api/run")
def run_agents(payload : RunRequest):
    topic = payload.topic.strip()

    if not topic:
        raise HTTPException(status_code = 400, detail = "Please enter a topic.")

    try:
        return run_workflow(topic)
    except Exception as exc:
        # Keep the demo response friendly while preserving the useful error text.
        raise HTTPException(status_code=500, detail=str(exc)) from exc

