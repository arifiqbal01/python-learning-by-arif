import requests
import csv
import os

# --- 1. Shopify headers ---
SHOPIFY_HEADERS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type",
    "Tags", "Published", "Option1 Name", "Option1 Value", "Option2 Name",
    "Option2 Value", "Option3 Name", "Option3 Value", "Variant SKU",
    "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
    "Variant Inventory Policy", "Variant Fulfillment Service",
    "Variant Price", "Variant Compare At Price", "Variant Requires Shipping",
    "Variant Taxable", "Variant Barcode", "Image Src", "Image Position",
    "Image Alt Text", "Gift Card", "SEO Title", "SEO Description",
    "Google Shopping / Google Product Category", "Google Shopping / Gender",
    "Google Shopping / Age Group", "Google Shopping / MPN",
    "Google Shopping / AdWords Grouping", "Google Shopping / AdWords Labels",
    "Google Shopping / Condition", "Google Shopping / Custom Product",
    "Google Shopping / Custom Label 0", "Google Shopping / Custom Label 1",
    "Google Shopping / Custom Label 2", "Google Shopping / Custom Label 3",
    "Google Shopping / Custom Label 4", "Variant Image", "Variant Weight Unit",
    "Variant Tax Code", "Cost per item", "Included / Primary",
    "Included / International", "Status"
]

# --- 2. Initialize CSV if missing ---
def initialize_csv(filepath):
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(SHOPIFY_HEADERS)
        print(f"Created new CSV with Shopify headers: {filepath}")

# --- 3. Append products ---
def append_to_csv(filepath, product_rows):
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SHOPIFY_HEADERS)
        for row in product_rows:
            writer.writerow(row)

# --- 4. Fetch product JSON and format for Shopify CSV ---
def fetch_product(handle):
    url = f"https://jollein.nl/products/{handle}.js"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def format_product_to_csv(product):
    variants = product.get("variants", [])
    media = product.get("media", [])
    tags = ", ".join(product.get("tags", []))

    rows = []
    for i, variant in enumerate(variants):
        row = {h: "" for h in SHOPIFY_HEADERS}

        row.update({
            "Handle": product.get("handle", ""),
            "Title": product.get("title", "") if i == 0 else "",
            "Body (HTML)": product.get("description", "") if i == 0 else "",
            "Vendor": product.get("vendor", ""),
            "Type": product.get("type", ""),
            "Tags": tags,
            "Published": "TRUE",
            "Option1 Name": "Title",
            "Option1 Value": variant.get("option1", "Default Title"),
            "Variant SKU": variant.get("sku", ""),
            "Variant Grams": variant.get("grams", 0),
            "Variant Inventory Tracker": "shopify",
            "Variant Inventory Qty": variant.get("inventory_quantity", 0),
            "Variant Inventory Policy": "deny",
            "Variant Fulfillment Service": "manual",
            "Variant Price": float(variant.get("price", 0)) / 100 if variant.get("price") else 0,
            "Variant Requires Shipping": "TRUE",
            "Variant Taxable": "TRUE",
            "Variant Barcode": variant.get("barcode", ""),
            "Gift Card": "FALSE",
            "Variant Weight Unit": "g",
            "Included / Primary": "TRUE",
            "Included / International": "TRUE",
            "Status": "active"
        })

        # Attach image for first variant
        if i == 0 and media:
            row["Image Src"] = media[0].get("src", "")
            row["Image Position"] = 1

        rows.append(row)

    # Add other media images
    for m in media[1:]:
        img_row = {h: "" for h in SHOPIFY_HEADERS}
        img_row["Handle"] = product.get("handle", "")
        img_row["Image Src"] = m.get("src", "")
        img_row["Image Position"] = m.get("position", "")
        rows.append(img_row)

    return rows

# --- 5. Main driver ---
def process_product_urls(product_urls, csv_path):
    initialize_csv(csv_path)
    for url in product_urls:
        handle = url.strip().split("/")[-1]
        try:
            product = fetch_product(handle)
            print(f"Fetched: {product['title']}")
            rows = format_product_to_csv(product)
            append_to_csv(csv_path, rows)
        except Exception as e:
            print(f"Error with {handle}: {e}")

if __name__ == "__main__":
    product_urls = [
        "https://jollein.nl/products/baby-mobiel-teddy-bear",
        "https://jollein.nl/products/activiteitenkubus-animal-friends"
    ]
    process_product_urls(product_urls, "shopify_products.csv")
