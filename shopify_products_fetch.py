#!/usr/bin/env python3
"""
General Shopify JSON to Official CSV Scraper
Fetches all products from a store and generates CSV in Shopify import format
"""

import requests
import csv
import time

STORE = "https://jollein.nl"  # replace with store domain
OUTPUT_CSV = "shopify_import_jollein.csv"
LIMIT = 250
DELAY = 1.0

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

def scrape_all_products():
    products_rows = []
    page = 1

    while True:
        url = f"{STORE}/products.json?limit={LIMIT}&page={page}"
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            print(f"❌ Failed to fetch page {page}")
            break

        data = r.json()
        products = data.get("products", [])
        if not products:
            print(f"⚠️ No more products on page {page}")
            break

        for p in products:
            handle = p.get("handle")
            title = p.get("title")
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
                products_rows.append(row)

        print(f"✅ Page {page}: {len(products)} products processed.")
        page += 1
        time.sleep(DELAY)

    return products_rows

def save_to_csv(rows):
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"💾 Saved {len(rows)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    all_rows = scrape_all_products()
    save_to_csv(all_rows)
