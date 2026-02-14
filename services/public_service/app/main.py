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


# this function takes the json blob for a card, iterates through all image URIs and returns the URI for normal sized image
def extract_image_url(card: dict) -> str | None:
    
    # single sided card, storing all image uris in dict to iterate through and checking if normal size exists
    # if normal size exists, return it, return exact image uri
    image_uris = card.get("image_uris")
    if image_uris and "normal" in image_uris:
        return image_uris["normal"]
    
    # two sided card, need to grab front side, check if card is two sided, then grab card image from index 0
    card_faces = card.get("card_faces")
    if card_faces:
        face_image_uri = card_faces[0].get("image_uris")
        if "normal" in face_image_uri:
            return face_image_uri["normal"]
        


# home page get request
@app.get("/")
def home(request: Request):
    context = {"request": request, "page_title": "Home"}
    return templates.TemplateResponse("home.html", context)



@app.get("/card_test")
async def card(request: Request):
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get("http://127.0.0.1:8002/card_test")
    
    # error handling, can't find card
    if resp.status_code == 404:
        return templates.TemplateResponse(
            "card.html",
            {"request": request, "error": "Card not found", "card": None, "image_url": None},
            status_code=404,
        )
    
    resp.raise_for_status()
    
    # this creates a python dict from a json response
    card = resp.json()
    # call our function that yoinks the image url out from the card dict we pass in
    image_url = extract_image_url(card)
    
    return templates.TemplateResponse(
        "card.html",
        {"request": request, "card": card, "image_url": image_url, "error": None},
    )