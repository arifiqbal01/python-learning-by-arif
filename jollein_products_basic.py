#!/usr/bin/env python3
"""
Scrape first 3 pages of Jollein collection for clean product title, handle, and URL.
Author: ChatGPT for Arif
"""

import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://jollein.nl"
COLLECTION_URL = f"{BASE_URL}/collections/all"
OUTPUT_CSV = "jollein_products_all.csv"
HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 15
DELAY = 1.0
MAX_PAGES = 400  # limit to first 3 pages

def get_html(url):
    for _ in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.text
        except Exception:
            time.sleep(1)
    return None

def extract_products_from_page(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for card in soup.select("product-card"):
        link = card.select_one("a[href*='/products/']")
        title_tag = card.select_one("p.text-surface-500.headline-3xs")  # clean title
        if not link or not title_tag:
            continue

        href = link["href"].split("?")[0]
        handle = href.replace("/products/", "").strip("/")
        title = title_tag.get_text(strip=True)
        url = BASE_URL + href

        products.append({"title": title, "handle": handle, "url": url})

    return products

def scrape_products(max_pages=MAX_PAGES):
    all_products = []
    for page in range(1, max_pages + 1):
        url = f"{COLLECTION_URL}?page={page}"
        html = get_html(url)
        if not html:
            print(f"❌ Failed to load page {page}.")
            continue

        products = extract_products_from_page(html)
        if not products:
            print(f"⚠️ No products found on page {page}.")
            break

        print(f"✅ Page {page}: Found {len(products)} products.")
        all_products.extend(products)
        time.sleep(DELAY)

    # remove duplicates by handle
    unique = {p["handle"]: p for p in all_products}
    return list(unique.values())

def save_to_csv(products):
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "handle", "url"])
        writer.writeheader()
        writer.writerows(products)

def main():
    print(f"🔍 Scraping first {MAX_PAGES} pages from {COLLECTION_URL} ...")
    products = scrape_products(MAX_PAGES)
    print(f"✅ Total products found: {len(products)}")
    save_to_csv(products)
    print(f"💾 Saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
