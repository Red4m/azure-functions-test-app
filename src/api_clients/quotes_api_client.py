import abc

import requests

from src.api_clients.exceptions import ApiClientError
from src.helpers.utils import retry

QUOTES_BASE_URL = "https://api.quotable.io"


class AbstractApiClient(abc.ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    @abc.abstractmethod
    def _get(self, url):
        pass


class QuoteApiClient(AbstractApiClient):
    def __init__(self, base_url=QUOTES_BASE_URL):
        super().__init__(base_url)

    def fetch_quotes(self, limit: int):
        url = f"{self.base_url}/quotes?limit={limit}"
        response = self._get(url)
        return response.json()

    def fetch_random_quote(self):
        url = f"{self.base_url}/random"
        response = self._get(url)
        return response.json()

    @retry(max_retries=1)
    def _get(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException as ex:
            raise ApiClientError(f"API request failed: {ex}")
