from markdown_it.rules_inline import image
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

@pytest.fixture
def make_category_data():
    save = set()
    def _make_data():
        data = {
            "name": fake.unique.first_name(),
            "description": fake.text(1000)
        }
        for i in range(100): 
            if data["name"] in save:
                data = {
                    "name": fake.unique.first_name(),
                    "description": fake.text(1000)
                }
                break
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


@pytest.mark.asyncio
async def test_get_categories(async_client, create_test_categories):
    category_info_json = {"id", "name", "description", "image", "created_at", "updated_at", "is_active"}
    response = await async_client.get(f"/category/get/all/")
    assert response.status_code == 200
    # data = response.json()
    # assert data["id"] > 0
    # assert set(data.keys()) == category_info_json


@pytest.mark.asyncio
async def test_get_category(async_client, create_test_categories):
    category_id = create_test_categories[0]["id"]
    category_info_json = {"id", "name", "description", "image", "created_at", "updated_at", "is_active"}
    response = await async_client.get(f"/category/get/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert set(data.keys()) == category_info_json

# @pytest.mark.asyncio
# async def test_login_user(async_client, create_test_user):
    
#     login_data = {
#         "username": create_test_user["email"],
#         "password": create_test_user["password"]
#     }
#     response = await async_client.post("/user/login", data=login_data)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "success"
#     assert "access_token" in data
#     assert data["message"] == "user has logged"
#     assert data["id"] > 0


# @pytest.mark.asyncio
# async def test_login_wrong_password(async_client, create_test_user):
#     login_data = {
#         "username": create_test_user["email"],
#         "password": "WrongPassword123!"
#     }
#     response = await async_client.post("/user/login", data=login_data)
#     assert response.status_code == 400 
#     assert response.json()["detail"] == "password is not valid"


# @pytest.mark.asyncio
# async def test_update_user(async_client, create_test_user, user_data):
#     header = {"Authorization": f"Bearer {create_test_user['access_token']}"}
#     response = await async_client.patch(f"/user/update/{create_test_user['id']}", json=user_data, headers=header)
#     assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_get_all_user(async_client, admin_token):
#     header = {"Authorization": f"Bearer {admin_token}"}
#     response = await async_client.get("/user/all", headers=header)
#     assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_upload_user_image(async_client, create_test_user):
#     token = create_test_user["access_token"]
#     header = {"Authorization": f"Bearer {token}"}
#     with open("test/assets/image/image.png", "rb") as image:
#         response = await async_client.post(
#             "/user/image",
#             headers=header,
#             files={
#                 "file": (
#                     "image.png",
#                     image,
#                     "image/png"
#                 )
#             }
#         )

#     assert response.status_code == 201
#     data = response.json()
#     assert data["message"] == "Successfully created"
#     assert "image name" in data


# @pytest_asyncio.fixture
# async def create_user_image(async_client, create_test_user):
#     token = create_test_user["access_token"]
#     header = {"Authorization": f"Bearer {token}"}
#     with open("test/assets/image/image.png", "rb") as image:
#         response = await async_client.post(
#             "/user/image",
#             headers=header,
#             files={
#                 "file": (
#                     "image.png",
#                     image,
#                     "image/png"
#                 )
#             }
#         )
#     assert response.status_code == 201, response.text
    
#     return response.json()["image name"]


# @pytest.mark.asyncio
# async def test_get_user_image(async_client, create_user_image):
#     response = await async_client.get(f"/user/image/{create_user_image}")
#     assert response.status_code == 200
#     assert response.headers["content-type"].startswith("image/")
#     assert len(response.content) > 0


# @pytest.mark.asyncio
# async def test_deactivate_user(async_client, create_test_user):
#     test_user_id = create_test_user["id"]
#     token = create_test_user["access_token"]
#     password = {"password": create_test_user["password"]}
#     header = {"Authorization": f"Bearer {token}"}
#     response = await async_client.patch(f"/user/deactivate/{test_user_id}", headers=header, json=password)

#     assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_delete_user(async_client, create_test_user, admin_token):
#     test_user_id = create_test_user["id"]
#     password = {"password": "SuperPass1234!"}
#     header = {"Authorization": f"Bearer {admin_token}"}
#     response = await async_client.request("DELETE", f"/user/delete/{test_user_id}", headers=header, json=password)

#     assert response.status_code == 200

