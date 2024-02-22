import fastapi.testclient
import main

client = fastapi.testclient.TestClient(main.app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Root of eduAPI"}
