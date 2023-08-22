from urllib.parse import urljoin
from typing import Dict, List, Any, Tuple
import os

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



def save_urls_to_file(filename: str, urls: List[str]) -> None:
    """Save a list of URLs to a file."""
     # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        for url in urls:
            f.write(f"{url}\n")

def load_urls_from_file(filename: str) -> List[str]:
    """Load a list of URLs from a file."""
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]

def get_urls(toc: Dict[str, Any], base_url: str) -> Tuple[List[str], List[str]]:
    """
    Given a table of contents (TOC) and a base URL, extracts and returns all URLs. 
    Also returns the URLs from the previous run.

    :param toc: A dictionary representing the table of contents.
    :param base_url: The base URL to join with relative URLs.
    :return: A tuple containing two lists: current URLs extracted from the TOC and previous URLs.
    """

    # Load previous URLs
    previous_filename = './urls/previous_urls.txt'
    previous_pages_to_crawl = load_urls_from_file(previous_filename)

    # Extract current URLs from the TOC
    pages_to_crawl = []
    for item in toc["items"]:
        toc_recurse(item, pages_to_crawl, base_url)

    # Save the current URLs for next time
    save_urls_to_file(previous_filename, pages_to_crawl)

    return pages_to_crawl, previous_pages_to_crawl