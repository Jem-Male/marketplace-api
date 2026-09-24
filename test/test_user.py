from urllib import response
import pytest
from rich import print
from rich.panel import Panel
from rich.json import JSON

@pytest.mark.asyncio
async def test_register_user(async_client):
    user_data = {
        "name": "Test User",
        "email": "test@mail.com",
        "number": "77771234567",
        "password": "Superpassword123.",
        "description": "I am a test"
    }

    response = await async_client.post("/user/register", json=user_data)
    
    assert response.status_code == 200
    
    data = response.json()
    # assert data["status"] == "success"
    assert "access_token" in data
    # assert data["message"] == "user is registered"
    assert data["id"] > 0
    
    print("\n\n", Panel(JSON(response.text), title="Test register user data result", expand=False, style="green"), "\n")


@pytest.mark.asyncio
async def test_login_user(async_client):
    register_data = {
        "name": "Test User",
        "email": "test@mail.com",
        "number": "77771234567",
        "password": "Superpassword123.",
        "description": "I am a test"
    }
    await async_client.post("/user/register", json=register_data)
    
    login_data = {
        "username": "test@mail.com",
        "password": "Superpassword123."
    }

    response = await async_client.post("/user/login", data=login_data)
    
    print(f"dsfdsfdsfdsfds{response.text}")
    
    assert response.status_code == 200
    
    data = response.json()
    # assert data["status"] == "success"
    assert "access_token" in data
    # assert data["message"] == "user is registered"
    assert data["id"] > 0
    
    print("\n\n", Panel(JSON(response.text), title="Test login user data result", expand=False, style="green"), "\n")