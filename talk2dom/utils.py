from bs4 import BeautifulSoup, Comment
from loguru import logger


def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")

    blacklist = [
        "script",
        "style",
        "meta",
        "link",
        "noscript",
        "iframe",
        "svg",
        "object",
        "embed",
    ]

    for tag in soup(blacklist):
        tag.decompose()

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    if soup.body is not None:
        body = soup.body
    else:
        body = soup

    cleaned = str(body).replace("\n", "").replace("\r", "").replace("\t", "")
    logger.debug("Cleaned html")
    return cleaned.strip()
