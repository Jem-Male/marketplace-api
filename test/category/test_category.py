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
def make_category_data():
    save = set()
    def _make_data():
        data = {
            "name": fake.unique.first_name(),
            "description": fake.text(1000)
        }
        for i in range(100): 
            if data["name"] not in save and len(data["name"]) > 2:
                break
            data = {
                "name": fake.unique.first_name(),
                "description": fake.text(1000)
            }
        save.add(data["name"])
        return data
    return _make_data


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

@pytest_asyncio.fixture
async def create_test_category(async_client, admin_token, make_category_data):
    header = {"Authorization": f"Bearer {admin_token}"}
    category_info = make_category_data()
    response = await async_client.post("/category/create", json=category_info, headers=header)
    data = response.json()
    assert response.status_code == 200
    
    return {**data, **category_info}


@pytest_asyncio.fixture
async def create_test_categories(async_client, admin_token, make_category_data):
    header = {"Authorization": f"Bearer {admin_token}"}
    created_category = []
    for i in range(10):
        category_info = make_category_data()
        response = await async_client.post("/category/create", json=category_info, headers=header)
        data = response.json()
        assert response.status_code == 200
        
        created_category.append({
            "id": data["id"],
            "name": category_info["name"],
            "description": category_info["description"]
        })
    
    return created_category


@pytest.mark.asyncio
async def test_category_create(async_client, admin_token, make_category_data):
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/category/create", json=make_category_data(), headers=header)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert data["message"] == "Category is created"
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_category_create_customer(async_client, create_test_user, make_category_data):
    token = create_test_user["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    response = await async_client.post("/category/create", json=make_category_data(), headers=header)
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] =="Not priveleges"


@pytest.mark.asyncio
async def test_get_categories(async_client, create_test_categories):
    category_info_json = {"id", "name", "description", "image", "created_at", "updated_at", "is_active"}
    response = await async_client.get(f"/category/get/all/")
    assert response.status_code == 200
    data = response.json()
    print(data[0]["id"])
    for i in range(10):
        assert data[i]["id"] == create_test_categories[i]["id"]
        assert data[i]["name"] == create_test_categories[i]["name"]
        assert data[i]["description"] == create_test_categories[i]["description"]
        assert set(data[i]) == category_info_json


@pytest.mark.asyncio
async def test_get_category(async_client, create_test_category):
    category_id = create_test_category["id"]
    category_info_json = {"id", "name", "description", "image", "created_at", "updated_at", "is_active"}
    response = await async_client.get(f"/category/get/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert set(data.keys()) == category_info_json


@pytest.mark.asyncio
async def test_get_category_by_name(async_client, create_test_category):
    category_name = create_test_category["name"]
    category_info_json = {"id", "name", "description", "image", "created_at", "updated_at", "is_active"}
    response = await async_client.get(f"/category/get/name/{category_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert set(data.keys()) == category_info_json


@pytest.mark.asyncio
async def test_update_category(async_client, admin_token, make_category_data, create_test_category):
    category_info = create_test_category
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.patch(f"/category/update/{category_info['id']}", json=make_category_data(), headers=header)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_upload_category_image_customer(async_client, create_test_user, create_test_category):
    token = create_test_user["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    category_id = create_test_category["id"]
    with open("test/assets/image/image.png", "rb") as image:
        response = await async_client.post(
            f"category/image/{category_id}",
            headers=header,
            files={
                "file": (
                    "image.png",
                    image,
                    "image/png"
                )
            }
        )
        assert response.status_code == 403
        data = response.json()
        assert data["detail"] == "Not priveleges"


@pytest.mark.asyncio
async def test_upload_category_image(async_client, admin_token, create_test_category):
    header = {"Authorization": f"Bearer {admin_token}"}
    category_id = create_test_category["id"]
    with open("test/assets/image/image.png", "rb") as image:
        response = await async_client.post(
            f"category/image/{category_id}",
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
async def create_test_image_category(async_client, admin_token, create_test_category):
    header = {"Authorization": f"Bearer {admin_token}"}
    category_id = create_test_category["id"]
    with open("test/assets/image/image.png", "rb") as image:
        response = await async_client.post(
            f"category/image/{category_id}",
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
        return response.json()


@pytest.mark.asyncio
async def test_get_category_image(async_client, create_test_image_category):
    category_uuid = create_test_image_category["image name"]
    response = await async_client.get(f"/category/image/{category_uuid}")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/")
    assert len(response.content) > 0


@pytest.mark.asyncio
async def test_deactivate_category(async_client, create_test_category, admin_token):
    category_id = create_test_category["id"]
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.patch(f"/category/deactivate/{category_id}", headers=header)

    assert response.status_code == 200


@pytest_asyncio.fixture
async def create_test_deactivate_category(async_client, create_test_category, admin_token):
    category_id = create_test_category["id"]
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.patch(f"/category/deactivate/{category_id}", headers=header)

    assert response.status_code == 200
    return response.json()


@pytest.mark.asyncio
async def test_get_deactivate_category(async_client, create_test_deactivate_category, admin_token):
    category_id = create_test_deactivate_category["id"]
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/category/get/deactive/{category_id}", headers=header)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_category(async_client, create_test_category, admin_token):
    category_id = create_test_category["id"]
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.delete(f"/category/delete/{category_id}", headers=header)

    assert response.status_code == 200