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
        the content will be saved under "./data/article1234/2023-08-18/index.html".
        If no <time> element is found, it will default to the current date.
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

    # Try to get the date from a <time> element in the page
    time_element = soup.find("time")
    if time_element:
        date = time_element.get("datetime")[:10]
    else:
        date = today

    # Check existing saved dates for the URL
    slug_dir = f"./data/{slug}"
    existing_dates = [
        d for d in os.listdir(slug_dir) if os.path.isdir(os.path.join(slug_dir, d))
    ] if os.path.exists(slug_dir) else []

    # If there's no existing date or the current date is newer, save the content
    if not existing_dates or date > max(existing_dates):
        folder = f"./data/{slug}/{date}"
        os.makedirs(folder, exist_ok=True)
        # Save the page content
        with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(response.text)
    elif date == max(existing_dates) and not time_element:  # Same date, but no <time> tag
        existing_file_path = os.path.join(slug_dir, date, "index.html")
        with open(existing_file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()

        # If the content is different, save it with a modified name
        if existing_content != response.text:
            folder = f"./data/{slug}/{date}_{datetime.now().strftime('%H%M%S')}"
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(response.text)
