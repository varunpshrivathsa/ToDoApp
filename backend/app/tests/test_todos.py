from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def register_and_login():
    """Register a user and login to get JWT headers"""
    register_payload = {
        "username": "testuser",
        "password": "testpass"
    }

    # Register user (POST /users/)
    client.post("/users/", json=register_payload)

    # Login with form-data (POST /token)
    response = client.post("/token", data={
        "username": "testuser",
        "password": "testpass"
    })

    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_get_todo():
    headers = register_and_login()

    # Create a todo
    todo_payload = {"title": "My first todo", "completed": False}
    response = client.post("/todos/", json=todo_payload, headers=headers)
    assert response.status_code in [200, 201], f"Create todo failed: {response.text}"
    todo = response.json()
    assert todo["title"] == "My first todo"

    # Fetch todos
    response = client.get("/todos/", headers=headers)
    assert response.status_code == 200, f"Get todos failed: {response.text}"
    todos = response.json()
    assert any(t["title"] == "My first todo" for t in todos)
