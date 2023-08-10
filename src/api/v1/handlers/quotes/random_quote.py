import json
import logging

import azure.functions as func

from src.helpers.utils import exception_handler
from src.services.quote_service import QuoteService


@exception_handler
def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retrieve random quote from an external API.

    Returns:
        Quote

    Raises:
        Error: Return 400 'Error occurred' if there is an error while fetching quotes from the external API.
    """
    quote_service = QuoteService()
    quote = quote_service.get_random_quote()
    if not quote:
        return func.HttpResponse(
            "No quotes found for the specified keyword.", status_code=404
        )
    response = json.dumps(quote.model_dump())
    return func.HttpResponse(response, status_code=200)
