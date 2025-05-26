import requests
from helpers.log_helper import Logger

logger = Logger("api-client").get_logger()

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {}

    def set_headers(self, headers: dict):
        self.headers.update(headers)
        logger.info(f"Headers set: {self.headers}")

    def request(self, method: str, endpoint: str, data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Sending {method.upper()} request to {url}")
        if data:
            logger.debug(f"Payload: {data}")
        if params:
            logger.debug(f"Query Params: {params}")

        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data,
            params=params
        )

        logger.info(f"Response status: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        return response

    def get(self, endpoint: str, params=None):
        return self.request("get", endpoint, params=params)

    def post(self, endpoint: str, data=None):
        return self.request("post", endpoint, data=data)

    def put(self, endpoint: str, data=None):
        return self.request("put", endpoint, data=data)

    def patch(self, endpoint: str, data=None):
        return self.request("patch", endpoint, data=data)

    def delete(self, endpoint: str):
        return self.request("delete", endpoint)
