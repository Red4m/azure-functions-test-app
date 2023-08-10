from typing import List, Optional

from pydantic import TypeAdapter

from src.api_clients.quotes_api_client import QuoteApiClient
from src.serializers.quote import Quote


class QuoteService:
    def __init__(self, api_client: QuoteApiClient = QuoteApiClient()):
        self.api_client = api_client

    def get_random_quote(self) -> Quote:
        """
        This method retrieve random quote from the external API
        :return: random quote
        """
        data = self.api_client.fetch_random_quote()
        ta = TypeAdapter(Quote)
        quote = ta.validate_python(data)
        return quote

    def get_quotes(self, limit: int = 10) -> Optional[List[Quote]]:
        """
        This method retrieve list of quotes from external API
        :return: list of quotes
        """
        data = self.api_client.fetch_quotes(limit)
        ta = TypeAdapter(List[Quote])
        quotes = ta.validate_python(data["results"])
        return quotes

    @staticmethod
    def filter_quotes_by_author(quotes: List[Quote], keyword: str) -> List[Quote]:
        return (
            list(filter(lambda quote: keyword.lower() in quote.author.lower(), quotes))
            if keyword
            else quotes
        )
