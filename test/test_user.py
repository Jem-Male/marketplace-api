from urllib import response
import pytest
from rich import print
from rich.panel import Panel
from rich.json import JSON
import pytest_asyncio


@pytest_asyncio.fixture
async def create_test_user(async_client):
    user_data = {
        "name": "Damir",
        "email": "damirr045@mail.com",
        "number": "77771234567",
        "password": "Damiroshko/12",
        "description": "I am a test Damir!"
    }

    response = await async_client.post("/user/register", json=user_data)
    
    assert response.status_code == 200
    
    data = response.json()
    # assert data["status"] == "success"
    assert "access_token" in data
    # assert data["message"] == "user is registered"
    assert data["id"] > 0
    
    return user_data


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
async def test_login_user(async_client, create_test_user):
    
    login_data = {
        "username": create_test_user["email"],
        "password": create_test_user["password"]
    }

    response = await async_client.post("/user/login", data=login_data)
    
    assert response.status_code == 200
    
    data = response.json()
    # assert data["status"] == "success"
    assert "access_token" in data
    # assert data["message"] == "user is registered"
    assert data["id"] > 0
    
    print("\n\n", Panel(JSON(response.text), title="Test login user data result", expand=False, style="green"), "\n")


@pytest.mark.asyncio
async def test_login_wrong_password(async_client, create_test_user):
    login_data = {
        "username": create_test_user["email"],
        "password": "WrongPassword123!"
    }

    response = await async_client.post("/user/login", data=login_data)
    
    assert response.status_code == 400 
    assert response.json()["detail"] == "password is not valid"


