# import pytest
# import pytest_asyncio
# from faker import Faker
# from src.user.model import UserModel
# from src.user.auth import create_access_token
# from src.user.security import generate_password_hash


# fake = Faker("RU-ru")

# @pytest.fixture
# def user_data():
#     return {
#         "name": fake.first_name(),
#         "email": fake.email(),
#         "number": fake.phone_number(),
#         "password": fake.password()
#     }


# @pytest_asyncio.fixture
# async def create_admin(db_session):
#     pasword = "SuperPass1234!"
#     hash_pass = await generate_password_hash(pasword)
#     admin = UserModel(
#         name="admin", 
#         email="admin@example.com", 
#         hashed_password=hash_pass,
#         is_active=True,
#         number="+71231231212",
#         role="admin",
#         is_email_verified=True,
#         is_phone_verified=True
#     )
    
#     db_session.add(admin)
#     await db_session.commit()
#     await db_session.refresh(admin)
    
#     yield admin


# @pytest_asyncio.fixture
# async def admin_token(create_admin):
#     token_data = {
#         "sub": str(create_admin.id),
#         "role": str("admin")
#     } 
#     return await create_access_token(token_data)


# @pytest_asyncio.fixture
# async def create_test_user(async_client, user_data):
#     response = await async_client.post("/user/register", json=user_data)
#     assert response.status_code == 200        
#     return {
#         **user_data,
#         "access_token": response.json().get("access_token"),
#         "id": response.json().get("id"),
#     }


# @pytest.mark.asyncio
# async def test_register_user(async_client, user_data):
#     response = await async_client.post("/user/register", json=user_data)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "success"
#     assert "access_token" in data
#     assert data["message"] == "user is registered"
#     assert data["id"] > 0
    

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
# async def test_get_all_user(async_client):
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

