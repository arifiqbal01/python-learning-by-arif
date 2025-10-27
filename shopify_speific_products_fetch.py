#!/usr/bin/env python3
"""
Shopify JSON Scraper (specific products only)
Fetches only given product handles or URLs and generates Shopify import CSV.
"""

import requests
import csv
from urllib.parse import urlparse
import time

# 🛍️ CONFIGURATION
STORE = "https://hemnature.com/"
OUTPUT_CSV = "shopify_selected_products_hemnature.csv"
DELAY = 0.8

# 🔹 Add your handles or URLs here
PRODUCTS_TO_FETCH = [
    "natuurlijk-vloeibare-wasmiddel",
    "incia-natuurlijk-afwasmiddel",
    "incia-preventieve-natuurlijk-luieruitslag-gel",
    "incia-natuurlijke-baby-olie",
    "incia-verzorgende-en-hydraterende-gel-voor-de-droge-huid",
    "incia-natuurlijke-allesreiniger-spray",
    "incia-natuurlijke-baby-schuimende-shampoo",
    "incia-natuurlijke-kinder-shampoo",
    "incia-sos-stick",
    "incia-vloeibare-handzeep-gevoelige-huid",
    "incia-natuurlijke-schuimende-handzeep-kinderen",
    "incia-creme-voor-droge-huid",
    "incia-natuurlijke-vloerreiniger",
    "incia-tepel-zalf",
    "incia-aromatherapie-baby",
    "incia-vloeibare-handzeep",
    "incia-kids-easy-hair-spray-anti-klit",
    "mini-shampoo",
    "incia-kids-lippenbalsem-sinaasappel",
    "incia-coconut-butter",
    "hydraterende-olie-voor-ellebogen-en-hielen",
    "incia-kids-lippenbalsem-citroen"
]

CSV_FIELDS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
    "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
    "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price",
    "Variant Compare at Price", "Variant Requires Shipping", "Variant Taxable",
    "Variant Barcode", "Image Src", "Image Position", "Gift Card",
    "SEO Title", "SEO Description", "Google Shopping / Google Product Category",
    "Google Shopping / Gender", "Google Shopping / Age Group", "Google Shopping / MPN",
    "Google Shopping / AdWords Grouping", "Google Shopping / AdWords Labels",
    "Google Shopping / Condition", "Google Shopping / Custom Product", "Google Shopping / Custom Label 0",
    "Google Shopping / Custom Label 1", "Google Shopping / Custom Label 2",
    "Google Shopping / Custom Label 3", "Google Shopping / Custom Label 4",
    "Variant Image", "Variant Weight Unit", "Variant Tax Code", "Cost per item"
]

def extract_handle(value):
    """Extracts the handle from a Shopify URL or returns handle if already plain."""
    if value.startswith("http"):
        path = urlparse(value).path
        if "/products/" in path:
            return path.split("/products/")[-1].split("?")[0]
    return value.strip()

def fetch_product(handle):
    """Fetch a single product by handle"""
    url = f"{STORE}/products/{handle}.json"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"❌ Failed to fetch {handle}")
            return None
        data = r.json().get("product", {})
        if not data:
            print(f"⚠️ No product found for {handle}")
            return None
        return data
    except Exception as e:
        print(f"⚠️ Error fetching {handle}: {e}")
        return None

def parse_product(p):
    """Parse single product data to Shopify CSV format"""
    rows = []
    handle = p.get("handle", "")
    title = p.get("title", "")
    body_html = p.get("body_html", "")
    vendor = p.get("vendor", "")
    type_ = p.get("product_type", "")
    tags = ", ".join(p.get("tags", [])) if isinstance(p.get("tags"), list) else p.get("tags","")
    published = "TRUE" if p.get("published_at") else "FALSE"

    options = p.get("options", [])
    option1_name = options[0]["name"] if len(options) > 0 else ""
    option2_name = options[1]["name"] if len(options) > 1 else ""
    option3_name = options[2]["name"] if len(options) > 2 else ""

    for idx, variant in enumerate(p.get("variants", [])):
        row = {
            "Handle": handle,
            "Title": title,
            "Body (HTML)": body_html,
            "Vendor": vendor,
            "Type": type_,
            "Tags": tags,
            "Published": published,
            "Option1 Name": option1_name,
            "Option1 Value": variant.get("option1", ""),
            "Option2 Name": option2_name,
            "Option2 Value": variant.get("option2", ""),
            "Option3 Name": option3_name,
            "Option3 Value": variant.get("option3", ""),
            "Variant SKU": variant.get("sku", ""),
            "Variant Grams": variant.get("grams", 0),
            "Variant Inventory Tracker": variant.get("inventory_management", ""),
            "Variant Inventory Qty": variant.get("inventory_quantity", 0),
            "Variant Inventory Policy": variant.get("inventory_policy", "deny"),
            "Variant Fulfillment Service": variant.get("fulfillment_service", "manual"),
            "Variant Price": variant.get("price", ""),
            "Variant Compare at Price": variant.get("compare_at_price", ""),
            "Variant Requires Shipping": "TRUE" if variant.get("requires_shipping", True) else "FALSE",
            "Variant Taxable": "TRUE" if variant.get("taxable", True) else "FALSE",
            "Variant Barcode": variant.get("barcode", ""),
            "Image Src": p["images"][idx]["src"] if idx < len(p.get("images", [])) else "",
            "Image Position": idx + 1 if idx < len(p.get("images", [])) else "",
            "Gift Card": "FALSE",
            "SEO Title": p.get("seo", {}).get("title", ""),
            "SEO Description": p.get("seo", {}).get("description", ""),
            "Google Shopping / Google Product Category": "",
            "Google Shopping / Gender": "",
            "Google Shopping / Age Group": "",
            "Google Shopping / MPN": "",
            "Google Shopping / AdWords Grouping": "",
            "Google Shopping / AdWords Labels": "",
            "Google Shopping / Condition": "",
            "Google Shopping / Custom Product": "",
            "Google Shopping / Custom Label 0": "",
            "Google Shopping / Custom Label 1": "",
            "Google Shopping / Custom Label 2": "",
            "Google Shopping / Custom Label 3": "",
            "Google Shopping / Custom Label 4": "",
            "Variant Image": "",
            "Variant Weight Unit": variant.get("weight_unit", ""),
            "Variant Tax Code": "",
            "Cost per item": ""
        }
        rows.append(row)
    return rows

def save_to_csv(rows):
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"💾 Saved {len(rows)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    all_rows = []
    for item in PRODUCTS_TO_FETCH:
        handle = extract_handle(item)
        product = fetch_product(handle)
        if product:
            rows = parse_product(product)
            all_rows.extend(rows)
        time.sleep(DELAY)
    save_to_csv(all_rows)
