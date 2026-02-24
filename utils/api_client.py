import json
import logging

import allure
import requests

logger = logging.getLogger("api_client")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(levelname)s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _log(self, response: requests.Response) -> None:
        logger.info(
            "Status %s | %s %s",
            response.status_code,
            response.request.method,
            response.request.url,
        )

    def _allure_attach_request(self, method: str, endpoint: str, body=None) -> None:
        request_info = f"{method} {endpoint}"
        if body is not None:
            request_info += f"\n\n{json.dumps(body, indent=2, ensure_ascii=False)}"
        allure.attach(
            request_info,
            name="Request",
            attachment_type=allure.attachment_type.TEXT,
        )

    def _allure_attach_response(self, response: requests.Response) -> None:
        try:
            body = json.dumps(response.json(), indent=2, ensure_ascii=False)
        except Exception:
            body = response.text
        response_info = f"Status: {response.status_code}\n\n{body}"
        allure.attach(
            response_info,
            name="Response",
            attachment_type=allure.attachment_type.TEXT,
        )

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        self._allure_attach_request("GET", endpoint)
        response = self.session.get(f"{self.base_url}{endpoint}", **kwargs)
        self._log(response)
        self._allure_attach_response(response)
        return response

    def post(self, endpoint: str, json_data=None, **kwargs) -> requests.Response:
        self._allure_attach_request("POST", endpoint, body=json_data)
        response = self.session.post(
            f"{self.base_url}{endpoint}", json=json_data, **kwargs
        )
        self._log(response)
        self._allure_attach_response(response)
        return response

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        self._allure_attach_request("DELETE", endpoint)
        response = self.session.delete(f"{self.base_url}{endpoint}", **kwargs)
        self._log(response)
        self._allure_attach_response(response)
        return response
