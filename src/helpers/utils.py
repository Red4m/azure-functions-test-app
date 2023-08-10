import logging
import time
from functools import wraps
from typing import Callable

from azure.functions import HttpRequest, HttpResponse

from src.api_clients.exceptions import ApiClientError


def retry(max_retries: int = 1):
    def exponential_backoff(f):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logging.error(f"An error occurred: {e}")
                    retries += 1
                    wait_time = 2**retries
                    logging.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            logging.error("Max retries reached, giving up.")
            raise ApiClientError(f"API request failed.")

        return wrapper

    return exponential_backoff


def exception_handler(f: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    @wraps(f)
    def wrapper(*args: HttpRequest, **kwargs: HttpRequest) -> HttpResponse:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return HttpResponse("Error occurred", status_code=400)

    return wrapper
