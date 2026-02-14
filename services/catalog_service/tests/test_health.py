from fastapi.testclient import TestClient
from app.main import app

# functions for testing - im using this to practice app.get requests 
def test_health():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_hello():
    client = TestClient(app)
    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.json() == {"message": "hello"}