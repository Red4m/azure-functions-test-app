import logging
from typing import List

import azure.functions as func
from pydantic import TypeAdapter

from src.helpers.utils import exception_handler
from src.serializers.quote import Quote
from src.services.quote_service import QuoteService


@exception_handler
def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retrieve filtered quotes based on provided query parameters.

    Query params:
        keyword (str): A keyword to filter quotes by author's name.
        limit (int): The maximum number of quotes to retrieve.

    Returns:
        List[Quote]: A list of filtered quotes matching the provided keyword.

    Raises:
        Error: Return 400 'Error occurred' if there is an error while fetching quotes from the external API.
    """
    keyword = req.params.get("keyword")
    limit = req.params.get("limit")
    quote_service = QuoteService()
    quotes = quote_service.get_quotes(limit=limit)

    filtered_quotes = quote_service.filter_quotes_by_author(quotes, keyword)

    if not filtered_quotes:
        return func.HttpResponse(
            "No quotes found for the specified keyword.", status_code=404
        )
    ta = TypeAdapter(List[Quote])
    response = ta.dump_json(filtered_quotes)
    return func.HttpResponse(response, status_code=200)
