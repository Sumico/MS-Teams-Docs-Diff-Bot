import requests

BASE_URL = "https://learn.microsoft.com/en-us/microsoftteams/"
toc = requests.get("https://learn.microsoft.com/en-us/microsoftteams/toc.json").json()
