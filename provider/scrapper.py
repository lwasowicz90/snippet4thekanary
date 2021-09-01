"""Module that scraps text data based on html tags and attributes"""
from bs4 import BeautifulSoup


def scrap_headlines(page_text: str, tag: str, attrs: dict):
    """Looks for given tag and attributes, then read text and link"""
    if not page_text:
        return []
    soup = BeautifulSoup(page_text, 'html.parser')
    found = soup.find_all(tag, attrs=attrs)

    return [{'title': item.text, 'link': item.get('href')} for item in remove_not_valid_entries(found)]


def remove_not_valid_entries(found_data):
    """Filters out broken items"""
    return filter(lambda item: item.get('href') and item['href'].startswith('https://') and item.text, found_data)
