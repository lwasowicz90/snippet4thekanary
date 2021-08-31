import logging
from typing import List

from config.config import JsonDataLoader, validate
from provider.resolver import get_pages
from provider.meta import MetaProvider
from provider.scrapper import scrap_headlines


logger = logging.getLogger("ProviderManager")


class ProviderManager:
    """Class that delegates: reading pages, scrapping headlines from pages and dumping headlines to file"""
    def __init__(self, config_path: str):
        self._providers_meta_data = ProviderManager._load_providers_meta_data(config_path)
        logger.debug("Initialized {} with {} provider(s)".format(ProviderManager.__name__,
                                                                 len(self._providers_meta_data)))
        self._headlines = []

    @property
    def headlines(self):
        """Headlines getter"""
        return self._headlines

    @staticmethod
    def _load_providers_meta_data(path) -> List[MetaProvider]:
        """Helper method for loading providers data"""
        with JsonDataLoader(path) as loader:
            config = loader.data
        validate(config)
        return [MetaProvider(url=p_data['url'], tag=p_data['tag'], attrs=p_data['attrs']) for p_data in config.values()]

    def process(self):
        """Starts entire process of reading pages and extracting headlines"""
        pages_map = get_pages(self._providers_meta_data)

        for page_text, metadata in zip(pages_map.values(), self._providers_meta_data):
            headlines_data = scrap_headlines(page_text, metadata.tag, metadata.attrs)
            self._headlines.append({metadata.url: headlines_data})
