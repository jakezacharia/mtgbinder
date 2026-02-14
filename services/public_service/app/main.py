from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, PackageLoader, select_autoescape
import httpx

app = FastAPI(title="public_service")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/health")
def health():
    return {"status": "healthy"}

# home page get request
@app.get("/")
def home(request: Request):
    context = {"request": request, "page_title": "Home"}
    return templates.TemplateResponse("search.html", context)

@app.get("/card_test")
def card(request: Request):