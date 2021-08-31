"""Module for handling async request in order to speed up network activities
Perhaps it is not worth to do it for couple of endpoints but one can imagine how it could
improve performance for dozens or hundreds requests."""
from typing import List
import asyncio
import httpx

from provider.meta import MetaProvider


class AsyncResolver:
    """Helper class for scheduling http requests"""
    def __init__(self, meta_providers: List[MetaProvider]):
        self._meta_providers = meta_providers
        self._responses = {}

    @staticmethod
    async def _get_page(url: str) -> dict:
        """Async function to get single page"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
            except Exception:  # pylint: disable=W0703
                return {url: None}
            return {url: response.text}

    async def _prepare(self):
        """Async function that acts as async main"""
        tasks = [AsyncResolver._get_page(meta_provider.url) for meta_provider in self._meta_providers]
        results = await asyncio.gather(*tasks)
        for result in results:
            self._responses.update(result)

    def execute(self):
        """Starts sending requests and waits for reponses"""
        asyncio.run(self._prepare())

    @property
    def responses(self) -> dict:
        """Getter for responses"""
        return self._responses


def get_pages(meta_providers: List[MetaProvider]) -> dict:
    """Helper method to make usage of this module very simple"""
    resolver = AsyncResolver(meta_providers)
    resolver.execute()
    return resolver.responses
