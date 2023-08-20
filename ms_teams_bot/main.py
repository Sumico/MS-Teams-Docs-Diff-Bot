import requests
import crawler
import url_getter

BASE_URL = "https://learn.microsoft.com/en-us/microsoftteams/"
toc = requests.get("https://learn.microsoft.com/en-us/microsoftteams/toc.json").json()

urls = url_getter.get_urls(toc, BASE_URL)
for url in urls:
    crawler.crawl(url)

