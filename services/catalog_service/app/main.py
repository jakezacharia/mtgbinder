from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="catalog service")

# wire URLs to Python functions

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "hello world!"}

@app.get("/card_test")
def card_test():
    url = "https://api.scryfall.com/cards/named"
    params = {"exact": "lightning bolt"}
    headers = {"User-Agent": "mtg-binder dev"}
    
    resp = httpx.get(url, params=params, headers=headers, timeout=10.0)
    
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Card not found on scryfall")
    
    resp.raise_for_status()
    # this returns the entire json blob 
    return resp.json()
