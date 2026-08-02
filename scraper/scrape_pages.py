import os
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from urls import URLS


PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = PROJECT_ROOT / "knowledge"
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

TIMEOUT = 20
MAX_RETRIES = 3


def clean_markdown(text):
    """
    Remove extra spaces and blank lines.
    """

    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def filename_from_url(url):
    """
    Convert URL into filename.
    """

    filename = (
        url.replace("https://", "")
        .replace("http://", "")
        .strip("/")
        .replace("/", "_")
    )

    return filename + ".md"


def fetch_page(url):
    """
    Download webpage with retry logic.
    """

    for attempt in range(MAX_RETRIES):

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=TIMEOUT
            )

            response.raise_for_status()

            return response.text

        except Exception as e:

            print(
                f"Retry {attempt + 1}/{MAX_RETRIES} failed."
            )

            print(e)

            time.sleep(2)

    return None


print("=" * 60)
print("Starting Clinikk Website Scraper")
print("=" * 60)

for url in URLS:

    print(f"\nDownloading : {url}")

    html = fetch_page(url)

    if html is None:

        print("Skipping page...\n")
        continue

    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags

    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "footer"
    ]):
        tag.decompose()

    # Prefer extracting only the main content

    main = soup.find("main")

    if main:

        html_content = str(main)

    elif soup.body:

        html_content = str(soup.body)

    else:

        html_content = str(soup)

    # Convert HTML → Markdown

    markdown = md(html_content)

    markdown = clean_markdown(markdown)

    filename = filename_from_url(url)

    filepath = OUTPUT_DIR / filename

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(markdown)

    print(f"Saved : {filename}")

    # Delay to avoid sending rapid requests
    time.sleep(1)

print("\n" + "=" * 60)
print("Scraping Completed Successfully!")
print("=" * 60)

print(f"\nKnowledge files saved in:\n{OUTPUT_DIR}")