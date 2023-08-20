from urllib.parse import urljoin
from typing import Dict, List, Any

def toc_recurse(node: Dict[str, Any], pages_to_crawl: List[str], base_url: str) -> None:
    """
    Recursively traverses the given node to extract URLs from the 'href' keys.

    :param node: A dictionary representing a node in the table of contents.
    :param pages_to_crawl: A list to append found URLs to.
    :param base_url: The base URL to join with relative URLs.
    """

    if "href" in node:
        # Urls starting with "/" in the TOC file appear to be either invalid or have a different base URL.
        # We're excluding them for now.
        if not node["href"].startswith("/"):
            url = urljoin(base_url, node["href"])
            pages_to_crawl.append(url)

    # Recurse into children or items, if present
    for key in ["children", "items"]:
        if key in node:
            for child in node[key]:
                toc_recurse(child, pages_to_crawl, base_url)

def get_urls(toc: Dict[str, Any], base_url: str) -> List[str]:
    """
    Given a table of contents (TOC) and a base URL, extracts and returns all URLs.

    :param toc: A dictionary representing the table of contents.
    :param base_url: The base URL to join with relative URLs.
    :return: A list of URLs extracted from the TOC.
    """

    pages_to_crawl = []
    for item in toc["items"]:
        toc_recurse(item, pages_to_crawl, base_url)
    return pages_to_crawl
