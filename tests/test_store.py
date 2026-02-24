import allure
import pytest
from jsonschema import validate

from schemas.store import (
    create_order_request_schema,
    order_response_schema,
)
from schemas.common import api_response_schema


@allure.feature("Store")
class TestStore:

    @allure.title("Создание заказа (POST /store/order)")
    def test_create_order(self, api):
        body = {
            "id": 5,
            "petId": 112233,
            "quantity": 1,
            "shipDate": "2026-03-01T10:00:00.000+0000",
            "status": "placed",
            "complete": True,
        }

        with allure.step("Валидация request-схемы"):
            validate(instance=body, schema=create_order_request_schema)

        with allure.step("Отправка POST /store/order"):
            response = api.post("/store/order", json_data=body)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200

        response_json = response.json()

        with allure.step("Проверка значений в response"):
            assert response_json["petId"] == 112233
            assert response_json["status"] == "placed"
            assert response_json["complete"] is True

        with allure.step("Валидация response-схемы"):
            validate(instance=response_json, schema=order_response_schema)

    @allure.title("Получение заказа по ID (GET /store/order/{orderId})")
    def test_get_order_by_id(self, api):
        order_id = 5

        with allure.step(f"Отправка GET /store/order/{order_id}"):
            response = api.get(f"/store/order/{order_id}")

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200

        response_json = response.json()

        with allure.step("Проверка значений в response"):
            assert response_json["id"] == order_id

        with allure.step("Валидация response-схемы"):
            validate(instance=response_json, schema=order_response_schema)

    @allure.title("Удаление заказа (DELETE /store/order/{orderId})")
    def test_delete_order(self, api):
        order_id = 5

        with allure.step(f"Отправка DELETE /store/order/{order_id}"):
            response = api.delete(f"/store/order/{order_id}")

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200

        response_json = response.json()

        with allure.step("Проверка значений в response"):
            assert response_json["message"] == str(order_id)

        with allure.step("Валидация response-схемы"):
            validate(instance=response_json, schema=api_response_schema)
