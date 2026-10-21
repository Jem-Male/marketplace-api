import pytest
import pytest_asyncio
from faker import Faker
from src.user.model import UserModel
from src.user.auth import create_access_token
from src.user.security import generate_password_hash


fake = Faker("RU-ru")

@pytest.fixture
def user_data():
    return {
        "name": fake.first_name(),
        "email": fake.email(),
        "number": fake.phone_number(),
        "password": fake.password()
    }


@pytest.fixture
def store_data():
    return {
        "name": fake.first_name(),
        "description": fake.text(1000),
        "phone": fake.phone_number(),
        "email": fake.email()
    }


@pytest_asyncio.fixture
async def create_admin(db_session):
    pasword = "SuperPass1234!"
    hash_pass = await generate_password_hash(pasword)
    admin = UserModel(
        name="admin", 
        email="admin@example.com", 
        hashed_password=hash_pass,
        is_active=True,
        number="+71231231212",
        role="admin",
        is_email_verified=True,
        is_phone_verified=True
    )
    
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    
    yield admin


@pytest_asyncio.fixture
async def admin_token(create_admin):
    token_data = {
        "sub": str(create_admin.id),
        "role": str("admin")
    } 
    return await create_access_token(token_data)


@pytest_asyncio.fixture
async def create_test_user(async_client, user_data):
    response = await async_client.post("/user/register", json=user_data)
    assert response.status_code == 200      
    return {
        **user_data,
        "access_token": response.json().get("access_token"),
        "id": response.json().get("id"),
    }


@pytest.mark.asyncio
async def test_store_create(async_client, admin_token, store_data):
    token = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/store/create", json=store_data, headers=token)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert data["message"] == "Store is created"
    assert data["status"] == "success"
    

@pytest.mark.asyncio
async def test_store_create_customer(async_client, create_test_user, store_data):
    user = create_test_user["access_token"]
    token = {"Authorization": f"Bearer {user}"}
    response = await async_client.post("/store/create", json=store_data, headers=token)
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "No editing rights"


@pytest_asyncio.fixture
async def store_create(async_client, admin_token, store_data):
    token = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/store/create", json=store_data, headers=token)
    assert response.status_code == 200
    data = response.json()
    return {**store_data, **data}


@pytest.mark.asyncio
async def test_get_all_store(async_client, store_create):
    response_data = {"id", "name", "description", "image", "phone", "email", "created_at", "updated_at", "is_active"}
    response = await async_client.get("/store/get/all/")
    
    assert response.status_code == 200
    
    data = response.json()[0]
    assert set(data.keys()) == response_data


@pytest.mark.asyncio
async def test_get_store(async_client, store_create):
    response_data = {"id", "name", "description", "image", "phone", "email", "created_at", "updated_at", "is_active"}
    store_id = store_create["id"]
    response = await async_client.get(f"/store/get/{store_id}")
    
    assert response.status_code == 200
    
    data = response.json()
    assert set(data.keys()) == response_data


@pytest.mark.asyncio
async def test_upload_store_image(async_client, store_create, admin_token):
    store_id = store_create["id"]
    header = {"Authorization": f"Bearer {admin_token}"}
    with open("test/assets/image/image.png", "rb") as image:
        response = await async_client.post(
            f"/store/image/{store_id}",
            headers=header,
            files={
                "file": (
                    "image.png",
                    image,
                    "image/png"
                )
            }
        )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Successfully created"
    assert "image name" in data


@pytest_asyncio.fixture
async def create_store_image(async_client, store_create, admin_token):
    store_id = store_create["id"]
    header = {"Authorization": f"Bearer {admin_token}"}
    with open("test/assets/image/image.png", "rb") as image:
        response = await async_client.post(
            f"/store/image/{store_id}",
            headers=header,
            files={
                "file": (
                    "image.png",
                    image,
                    "image/png"
                )
            }
        )

    assert response.status_code == 201    
    return response.json()["image name"]


@pytest.mark.asyncio
async def test_get_store_image(async_client, create_store_image):
    response = await async_client.get(f"/user/image/{create_store_image}")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/")
    assert len(response.content) > 0


@pytest.mark.asyncio
async def test_update_store(async_client, store_create, admin_token, store_data):
    store_id = store_create["id"]
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.patch(f"/store/update/{store_id}", json=store_data, headers=header)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Store is updated"
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_update_store_customer(async_client, store_create, create_test_user, store_data):
    store_id = store_create["id"]
    token = create_test_user["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    response = await async_client.patch(f"/store/update/{store_id}", json=store_data, headers=header)
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "No editing rights"


@pytest.mark.asyncio
async def test_deactivate_store(async_client, store_create, admin_token):
    store_id = store_create["id"]
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.patch(f"/store/deactivate/{store_id}", headers=header)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_delete_store_customer(async_client, store_create, create_test_user):
    user = create_test_user["access_token"]
    store_id = store_create["id"]
    token = {"Authorization": f"Bearer {user}"}
    response = await async_client.delete(f"/store/delete/{store_id}", headers=token)
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "No editing rights"


@pytest_asyncio.fixture
async def deactivate_store(async_client, store_create, admin_token):
    store_id = store_create["id"]
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.patch(f"/store/deactivate/{store_id}", headers=header)
    assert response.status_code == 200
    return store_id


@pytest.mark.asyncio
async def test_get_deactivate_store(async_client, deactivate_store, admin_token):
    response_data = {"id", "name", "description", "image", "phone", "email", "created_at", "updated_at", "is_active"}
    store_id = deactivate_store
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/store/get/deactive/{store_id}", headers=header)
    
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == response_data