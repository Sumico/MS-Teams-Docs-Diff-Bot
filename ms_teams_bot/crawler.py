import requests
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import os
from datetime import datetime

def save_page(url, folder, content):
    """
    Save the content of a webpage to a specified folder.
    
    Parameters:
    - url (str): The URL of the page to be saved.
    - folder (str): The directory where the content should be saved.
    - content (str): The content to be saved.
    """
    filename = 'index.html'
  
    # Ensure the directory exists
    os.makedirs(folder, exist_ok=True) 
  
    # Write the content to the file
    with open(os.path.join(folder, filename), "w") as f:
        f.write(content)


def crawl(url):
    """
    Fetch and save the content of a webpage. Determine if the content is new, unchanged, or changed.
    
    Parameters:
    - url (str): The URL of the page to be fetched.
    
    Returns:
    - tuple: A tuple containing the status ('added', 'unchanged', 'changed') and optionally the URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url} - {e}")
        return ("error",)

    soup = BeautifulSoup(response.text, 'html.parser')
    time_element = soup.find("time")
    date = time_element["datetime"][:10] if time_element else datetime.now().strftime("%Y%m%d")
    slug = urlsplit(url).path.split("/")[-1]
    slug_dir = f"./data/{slug}"

    if not os.path.exists(slug_dir):
        save_page(url, f"./data/{slug}/{date}", response.text)
        return ("added", url)

    if time_element:
        # Check if content for this date already exists
        date_folder = os.path.join(slug_dir, date)
        if os.path.exists(date_folder):
            existing_content_file = os.path.join(date_folder, "index.html")
            
            with open(existing_content_file, 'r') as f:
                existing_content = f.read()
            
            if existing_content != response.text:
                save_page(url, f"./data/{slug}/{date}", response.text)
                return ("changed", url)
        
        else:
            save_page(url, f"./data/{slug}/{date}", response.text)
            return ("changed", url)
    
    else:
        # When there's no time element, compare with the most recent scraped version
        existing_dates = sorted([d for d in os.listdir(slug_dir) if os.path.isdir(os.path.join(slug_dir, d))])
        latest_date = existing_dates[-1] if existing_dates else None
        
        if latest_date:
            existing_content_file = os.path.join(slug_dir, latest_date, "index.html")
            with open(existing_content_file, 'r') as f:
                existing_content = f.read()

            if existing_content != response.text:
                save_page(url, f"./data/{slug}/{date}", response.text)
                return ("changed", url)
        else:
            save_page(url, f"./data/{slug}/{date}", response.text)
            return ("changed", url)

    # Default return
    return ("unchanged",)
