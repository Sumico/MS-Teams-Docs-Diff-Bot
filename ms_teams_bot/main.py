import requests
import crawler
import url_getter
import os
import yaml
from datetime import datetime
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "https://learn.microsoft.com/en-us/microsoftteams/"
TOC_URL = "https://learn.microsoft.com/en-us/microsoftteams/toc.json"

def main():
    """
    Entry point for the web crawling process. Fetches the TOC (Table Of Contents) 
    from a specified URL, extracts all relevant URLs, and passes each URL 
    to the crawler for content extraction and saving. Finally, it saves 
    statistics on the number of files added and changed to a YAML file.
    """
    start_time = time.time()

    try:
        toc = requests.get(TOC_URL).json()
    except Exception as e:
        print(f"Error fetching TOC from {TOC_URL} - {e}")
        return

    urls = url_getter.get_urls(toc, BASE_URL)
    
    stats = {"added": 0, "changed": 0, "unchanged": 0, "error": 0}
    
    for url in urls:
        status = crawler.crawl(url)
        stats[status] += 1

    end_time = time.time()
    duration = round(end_time - start_time, 2)  # Duration in seconds, rounded to two decimal places
    stats["duration_seconds"] = duration

    # Save statistics to a YAML file
    today = datetime.now().strftime("%Y%m%d")
    os.makedirs("./stats", exist_ok=True)
    with open(f"./stats/{today}.yaml", "w") as f:
        yaml.dump(stats, f)

main()
