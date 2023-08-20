import requests
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import os
from datetime import datetime


def crawl(url: str) -> None:
    """
    Fetches the content of the provided URL and saves it as an HTML file
    in a directory structure based on the URL slug and either the current
    date or the date found within the page content.

    :param url: The URL to fetch and save content from.

    Example:
        If provided with the URL "https://example.com/news/article1234"
        and the page has a <time> element with "datetime" attribute of "2023-08-18",
        the content will be saved under "./article1234/2023-08-18/index.html".
        If no <time> element is found, it will default to the current date and append at nodt folder, e.g.,
        "./article1234/nodt/20230818/index.html".
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we're not processing error responses (like 404s)
    except Exception as e:
        print(f"Error fetching {url} - {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    path = urlsplit(url).path
    slug = path.split("/")[-1]

    today = datetime.now().strftime("%Y%m%d")

    # Set default date value in case "time" element is not available
    date = f"nodt/{today}"

    # Try to get the date from a <time> element in the page
    time = soup.find("time")
    if time:
        date = time.get("datetime")[:10]

    # Create directory path based on slug and date
    folder = f"./data/{slug}/{date}"
    os.makedirs(folder, exist_ok=True)

    # Save the page content
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(response.text)
