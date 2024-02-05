import time
from quotes_toscrape.entities import Quote
from bs4 import BeautifulSoup
import requests


def fetch_content(url: str) -> str:
    time.sleep(0.3)
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Error fetching {url}: {e}")
    return res.text


def extract_quotes_data(html_content: str) -> list[Quote]:
    bs = BeautifulSoup(html_content, "html.parser")
    quote_divs = bs.find_all("div", {"class": "quote"})
    result = []
    for quote_div in quote_divs:
        quote_content = quote_div.find("span", {"class": "text"}).text
        quote_author = quote_div.find("small", {"class": "author"}).text
        quote_tags = quote_div.find_all("a", {"class": "tag"})

        result.append(
            Quote(
                content=quote_content[1:-1],
                author=quote_author,
                tags=[tag.text for tag in quote_tags],
            )
        )
    return result


def get_next_page_path(html_content: str) -> str:
    bs = BeautifulSoup(html_content, "html.parser")
    try:
        return bs.find("li", {"class": "next"}).a["href"]
    except AttributeError:
        return None


def scrape_all_quotes() -> list[Quote]:
    """
    Acessa http://quotes.toscrape.com e retorna
    uma lista com as citações encontradas
    """
    BASE_URL = "http://quotes.toscrape.com"
    next_page_path = "/"
    results = []
    while next_page_path is not None:
        print(f"Scraping {BASE_URL + next_page_path}")
        html_content = fetch_content(BASE_URL + next_page_path)
        results.extend(extract_quotes_data(html_content))
        next_page_path = get_next_page_path(html_content)
    return results
