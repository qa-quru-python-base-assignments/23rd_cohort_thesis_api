import allure
import pytest
from jsonschema import validate

from schemas.pet import (
    create_pet_request_schema,
    pet_response_schema,
    pets_list_response_schema,
)
from schemas.common import api_response_schema


@allure.feature("Pet")
class TestPet:

    @allure.title("Создание питомца (POST /pet)")
    def test_create_pet(self, api):
        body = {
            "id": 112233,
            "category": {"id": 1, "name": "Dogs"},
            "name": "Buddy",
            "photoUrls": ["https://example.com/buddy.jpg"],
            "tags": [{"id": 1, "name": "friendly"}],
            "status": "available",
        }

        with allure.step("Валидация request-схемы"):
            validate(instance=body, schema=create_pet_request_schema)

        with allure.step("Отправка POST /pet"):
            response = api.post("/pet", json_data=body)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200

        response_json = response.json()

        with allure.step("Проверка значений в response"):
            assert response_json["name"] == "Buddy"
            assert response_json["status"] == "available"

        with allure.step("Валидация response-схемы"):
            validate(instance=response_json, schema=pet_response_schema)

    @allure.title("Получение питомца по ID (GET /pet/{petId})")
    def test_get_pet_by_id(self, api):
        pet_id = 112233

        with allure.step(f"Отправка GET /pet/{pet_id}"):
            response = api.get(f"/pet/{pet_id}")

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200

        response_json = response.json()

        with allure.step("Проверка значений в response"):
            assert response_json["id"] == pet_id
            assert response_json["name"] == "Buddy"

        with allure.step("Валидация response-схемы"):
            validate(instance=response_json, schema=pet_response_schema)

    @allure.title("Поиск питомцев по статусу (GET /pet/findByStatus)")
    def test_find_pets_by_status(self, api):
        status = "available"

        with allure.step(f"Отправка GET /pet/findByStatus?status={status}"):
            response = api.get("/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200

        response_json = response.json()

        with allure.step("Проверка значений в response"):
            assert isinstance(response_json, list)
            assert len(response_json) > 0
            for pet in response_json[:5]:
                assert pet["status"] == status

        with allure.step("Валидация response-схемы"):
            validate(instance=response_json, schema=pets_list_response_schema)

    @allure.title("Удаление питомца (DELETE /pet/{petId})")
    def test_delete_pet(self, api):
        pet_id = 112233

        with allure.step(f"Отправка DELETE /pet/{pet_id}"):
            response = api.delete(f"/pet/{pet_id}")

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200

        response_json = response.json()

        with allure.step("Проверка значений в response"):
            assert response_json["message"] == str(pet_id)

        with allure.step("Валидация response-схемы"):
            validate(instance=response_json, schema=api_response_schema)
