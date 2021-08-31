from bs4 import BeautifulSoup


def scrap_headlines(page_text: str, tag: str, attrs: dict):
    """Looks for given tag and attributes, then read text and link"""
    if not page_text:
        return []
    soup = BeautifulSoup(page_text, 'html.parser')
    found = soup.find_all(tag, attrs=attrs)

    return [{'title': item.text, 'link': item['href']} for item in remove_not_valid_entries(found)]


def remove_not_valid_entries(found_data):
    return filter(lambda item: item['href'].startswith('https://'), found_data)
