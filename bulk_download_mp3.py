import os
import requests
from bs4 import BeautifulSoup

URL = "[YOUR URL LINK HERE]"

# Create folder
folder = "[NAME OF FOLDER YOU WANT]"
os.makedirs(folder, exist_ok=True)

print("[+] Fetching page...")
page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(page.text, "html.parser")

# Find all links containing ".mp3"
links = []
for a in soup.find_all("a"):
    href = a.get("href")
    if href and href.endswith(".mp3"):
        links.append(href)

print(f"[+] Found {len(links)} MP3 files.")

# Download each file
for i, link in enumerate(links, start=1):
    filename = link.split("/")[-1]
    path = os.path.join(folder, filename)

    print(f"Downloading {i}/{len(links)}: {filename}")
    try:
        r = requests.get(link, stream=True, timeout=60)
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(f"Failed to download {link}: {e}")

print("\n[✔] All downloads completed!")
