# scraper.py

import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import logging

# ---------- Config ----------
BASE_URL = "http://www.paulgraham.com"
ESSAYS_URL = "http://www.paulgraham.com/articles.html"
OUTPUT_DIR = "../data/essays"

# ---------- Logging ----------
logging.basicConfig(filename="scraper.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# ---------- Get all essay links ----------
def get_essay_links():
    response = requests.get(ESSAYS_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")
    essay_links = []

    for link in links:
        href = link.get("href")
        if href and href.endswith(".html") and not href.startswith("http"):
            essay_links.append((link.text.strip(), BASE_URL + "/" + href))

    return essay_links

# ---------- Download essays ----------
def download_essays(essay_links):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for title, link in tqdm(essay_links, desc="📚 Scraping Essays"):
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, "html.parser")
            essay_text = soup.get_text()
            filename = title.replace(" ", "_").replace("/", "_") + ".txt"

            with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                f.write(essay_text)

            print(f"✅ Saved: {title}")
            logging.info(f"Saved: {title} - {link}")

        except Exception as e:
            print(f"❌ Failed: {title}")
            logging.error(f"Failed: {title} - Error: {e}")

# ---------- Run ----------
if __name__ == "__main__":
    print("🚀 Collecting essay links...")
    essay_links = get_essay_links()
    print(f"Found {len(essay_links)} essays.\n")
    download_essays(essay_links)
    print("\n🎉 Done! All essays are saved in /data/essays")
