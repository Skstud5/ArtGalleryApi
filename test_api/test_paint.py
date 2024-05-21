import datetime

import pytest
import asyncio

from bson import ObjectId


@pytest.mark.asyncio(scope="session")
async def test_root(async_client):
    async for client in async_client:
        response = await client.get("/")
        assert response.status_code == 200


# region User
# @pytest.mark.asyncio(scope="session")
@pytest.mark.skip(reason="Временно отключен")
async def test_200_create_user(async_client):
    async for client in async_client:
        user_data = {
            "username": "AutotestUser",
            "email": "AutotestUser@mail.ru",
            "password": "AutotestUser"
        }
        response = await client.post("/users", json=user_data)
        data = response.json()
        print(f"{data}")
        assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_200_get_all_users(async_client):
    async for client in async_client:
        response = await client.get("/users")
        data = response.json()
        print(f"all users: {data}")
        assert response.status_code == 200


# endregion

# region Paint
@pytest.mark.asyncio(scope="session")
async def test_200_get_all_paint(async_client):
    async for client in async_client:
        response = await client.get("/paintings")
        data = response.json()
        print(f"all paintings: {data}")
        assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_500_error_create_paint(async_client):
    async for client in async_client:
        paint_data = {
            "title": "TitlePaint",
            "description": "DescriptionPaint",
            "uploaded_by": "TestUser",
            "image": "some_url_image"
        }
        response = await client.post("/paintings", json=paint_data)
        assert response.status_code == 500

# @pytest.mark.asyncio(scope="session")
# async def test_404_get_paint(async_client):
#     id_paint = ObjectId()
#     print(id_paint)
#     async for client in async_client:
#         response = await client.get(f"/paintings/{id_paint}")
#         assert response.status_code == 404
# endregion
