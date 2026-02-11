from fastapi import FastAPI

app = FastAPI(title="catalog service")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"message": "hello"}