#!/usr/bin/env python3
"""
General Shopify JSON Product Scraper
Fetches all products from a store using /products.json API,
handles pagination automatically (batches of 250 products).
"""

import requests
import csv
import time

STORE = "https://wigiwama.com"  # replace with any Shopify store
OUTPUT_CSV = "products_all.csv"
LIMIT = 250  # Shopify max per page
DELAY = 1.0  # polite delay between requests

def scrape_all_products():
    all_products = []
    page = 1

    while True:
        url = f"{STORE}/products.json?limit={LIMIT}&page={page}"
        try:
            r = requests.get(url, timeout=15)
            if r.status_code != 200:
                print(f"❌ Failed to fetch page {page}, status code: {r.status_code}")
                break
        except Exception as e:
            print(f"❌ Error fetching page {page}: {e}")
            break

        data = r.json()
        products = data.get("products", [])

        if not products:
            print(f"⚠️ No more products found on page {page}. Ending.")
            break

        for p in products:
            all_products.append({
                "title": p.get("title"),
                "handle": p.get("handle"),
                "url": f"{STORE}/products/{p.get('handle')}"
            })

        print(f"✅ Page {page}: {len(products)} products fetched.")
        page += 1
        time.sleep(DELAY)

    print(f"✅ Total products fetched: {len(all_products)}")
    return all_products

def save_to_csv(products):
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "handle", "url"])
        writer.writeheader()
        writer.writerows(products)
    print(f"💾 Saved {len(products)} products to {OUTPUT_CSV}")

if __name__ == "__main__":
    products = scrape_all_products()
    save_to_csv(products)
