import pytest
import pytest_asyncio
from faker import Faker
from src.user.model import UserModel
from src.user.auth import create_access_token
from src.user.security import generate_password_hash
import random


fake = Faker("RU-ru")


@pytest.fixture
def user_data():
    return {
        "name": fake.first_name(),
        "email": fake.email(),
        "number": fake.phone_number(),
        "password": fake.password()
    }

@pytest_asyncio.fixture
async def create_test_category(async_client, admin_token, make_category_data):
    header = {"Authorization": f"Bearer {admin_token}"}
    category_info = make_category_data()
    response = await async_client.post("/category/create", json=category_info, headers=header)
    data = response.json()
    assert response.status_code == 200
    
    return {**data, **category_info}

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

@pytest.fixture
def item_data(create_test_category, store_create):
    def _make_data():
        while True:
            name = fake.first_name()
            if len(name) > 2:
                break  
        return {
            "name": name,
            "description": fake.text(1000),
            "price": round(random.uniform(1.00, 99999999.99), 2),
            "store": store_create["id"],
            "category": create_test_category["id"],
            "stock": random.randint(1, 99999999)
        }
    return _make_data

@pytest.fixture
def store_data():
    return {
        "name": fake.first_name(),
        "description": fake.text(1000),
        "phone": fake.phone_number(),
        "email": fake.email()
    }


@pytest_asyncio.fixture
async def store_create(async_client, admin_token, store_data):
    token = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/store/create", json=store_data, headers=token)
    assert response.status_code == 200
    data = response.json()
    return {**store_data, **data}


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
async def test_create_item(async_client, admin_token, item_data):
    product_keys = {
        "name",
        "description",
        "price",
        "image",
        "category",
        "store",
        "creator",
        "id",
        "created_at",
        "updated_at",
    }

    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/item/create", json=item_data(), headers=header)
    assert response.status_code == 201

    data: dict = response.json()
    assert set(data.keys()) == product_keys


@pytest.mark.asyncio
async def test_create_item_customer(async_client, create_test_user, item_data):
    token = create_test_user["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    response = await async_client.post("/item/create", json=item_data(), headers=header)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_item_customer(async_client, create_test_user, item_data):
    token = create_test_user["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    response = await async_client.post("/item/create", json=item_data(), headers=header)
    assert response.status_code == 403
    assert response.json()["detail"] == "No editing rights"


@pytest_asyncio.fixture
async def create_item(async_client, admin_token, item_data):
    header = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/item/create", json=item_data(), headers=header)
    assert response.status_code == 201
    return response.json()


@pytest.mark.asyncio
async def test_get_item(async_client, create_item):
    product_keys = {
        "name",
        "description",
        "price",
        "image",
        "category",
        "store",
        "creator",
        "id",
        "created_at",
        "updated_at",
    }

    item_id = create_item["id"]
    response = await async_client.get(f"/item/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == product_keys


@pytest_asyncio.fixture
async def create_items(async_client, admin_token, item_data):
    data = []
    header = {"Authorization": f"Bearer {admin_token}"}
    for i in range(10):
        response = await async_client.post("/item/create", json=item_data(), headers=header)
        assert response.status_code == 201
        data.append(response.json())
    return data


@pytest.mark.asyncio
async def test_get_items(async_client, create_items):
    product_keys = {
        "name",
        "description",
        "price",
        "image",
        "category",
        "store",
        "creator",
        "id",
        "created_at",
        "updated_at",
    }

    response = await async_client.get(f"/item/all")
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert set(item.keys()) == product_keys
   

@pytest.mark.asyncio
async def test_upload_item_image(async_client, create_item, admin_token):
    token = admin_token
    item_id = create_item["id"]
    header = {"Authorization": f"Bearer {token}"}
    with open("test/assets/image/image.png", "rb") as image:
        response = await async_client.post(
            f"/item/image/{item_id}",
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
async def upload_item_image(async_client, create_item, admin_token):
    token = admin_token
    item_id = create_item["id"]
    header = {"Authorization": f"Bearer {token}"}
    with open("test/assets/image/image.png", "rb") as image:
        response = await async_client.post(
            f"/item/image/{item_id}",
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
async def test_get_item_image(async_client, upload_item_image):
    img_uuid = upload_item_image["image name"]
    response = await async_client.get(f"/item/image/{img_uuid}")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/")
    assert len(response.content) > 0


@pytest.mark.asyncio
async def test_update_img(async_client, create_item, admin_token, item_data):
    header = {"Authorization": f"Bearer {admin_token}"}
    item_id = create_item["id"]
    response = await async_client.put(f"/item/{item_id}", headers=header, json=item_data())
    assert response.status_code == 200


