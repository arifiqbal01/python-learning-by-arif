#!/usr/bin/env python3
"""
Wix HTML -> Shopify CSV exporter

- Crawl a category (or product list) page and find product links
- Visit each product page and extract:
    - Title, Description (HTML), Images
    - Options & Variants (attempt to extract variant-level SKU/price/inventory from embedded JSON)
- Produce a Shopify-import-ready CSV with your original CSV_FIELDS and structure

Usage:
    python3 wix_to_shopify.py

Adjust START_URL (category page) or provide a list of product URLs.
"""

import requests
import csv
import time
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from itertools import product

# --- USER CONFIG ---
START_URL = "https://en.littlebrands.be/moje"   # category page or page that lists products
OUTPUT_CSV = "shopify_import_from_wix.csv"
DELAY = 1.0          # seconds between requests
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117 Safari/537.36"}

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


# --- Helpers ---
def get_soup(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser"), r.text

def find_product_links_from_category(category_url):
    """Return absolute product page URLs discovered on a category page."""
    soup, _ = get_soup(category_url)
    anchors = soup.select('[data-hook="product-item-container"], [data-hook="product-item-product-details-link"] a')
    links = set()
    # fallback: look for anchor tags inside product-list wrapper
    if not anchors:
        wrapper = soup.select_one('[data-hook="product-list-wrapper"], [data-hook="product-list"]')
        if wrapper:
            anchors = wrapper.select('a[href]')
    for a in anchors:
        href = a.get("href") or a.get("data-href")
        if href:
            links.add(urljoin(category_url, href))
    # final fallback: collect all /product-page/ links
    if not links:
        for a in soup.select('a[href*="/product-page/"]'):
            links.add(urljoin(category_url, a['href']))
    print(f"Found {len(links)} product links on {category_url}")
    return sorted(links)

def extract_json_variants_from_html(html_text):
    """
    Attempt to find embedded JSON containing variant info.
    Many Wix product pages include a JS object with variants. We'll try multiple regex strategies.
    Returns parsed JSON list of variants or None.
    """
    # Strategy 1: find "variants":[ ... ] and expand outward to a JSON object
    m = re.search(r'("variants"\s*:\s*\[.*?\])', html_text, flags=re.S)
    if m:
        # try to find the surrounding braces
        start = m.start(1)
        # try to locate the start of the object (previous {)
        obj_start = html_text.rfind('{', 0, start)
        obj_end = html_text.find('}', m.end(1))
        # if the simple approach fails, try to extract the array only
        arr_text = m.group(1)
        try:
            # build minimal JSON
            json_text = "{" + arr_text + "}"
            parsed = json.loads(json_text)
            return parsed.get("variants") or parsed.get("variants", None)
        except Exception:
            try:
                # fallback: extract the array directly
                arr = m.group(1)
                # ensure valid json array: strip "variants":
                arr_only = re.sub(r'^\s*"variants"\s*:\s*', '', arr, count=1).strip()
                parsed_arr = json.loads(arr_only)
                return parsed_arr
            except Exception:
                pass

    # Strategy 2: find a JSON block assigned to variable containing "product" and "variants"
    m2 = re.search(r'(\{[^<>]*"product"[^<>]*"variants"\s*:\s*\[.*?\][^<>]*\})', html_text, flags=re.S)
    if m2:
        try:
            parsed = json.loads(m2.group(1))
            # dig into parsed to get variants
            if isinstance(parsed, dict):
                if "product" in parsed and isinstance(parsed["product"], dict):
                    return parsed["product"].get("variants")
                return parsed.get("variants")
        except Exception:
            pass

    # Strategy 3: find any array that looks like variants: [{"id":..., "sku":...}, ...]
    m3 = re.search(r'(\[\s*\{(?:[^{}]|\{[^{}]*\}){1,}\}\s*(?:,\s*\{(?:[^{}]|\{[^{}]*\}){1,}\}\s*)*\])', html_text, flags=re.S)
    if m3:
        text = m3.group(1)
        # heuristic: does it contain "sku" and "price"?
        if "\"sku\"" in text or "'sku'" in text:
            try:
                parsed = json.loads(text)
                # ensure it's a list of dicts
                if isinstance(parsed, list):
                    # return only if looks like variants
                    if all(isinstance(x, dict) for x in parsed):
                        return parsed
            except Exception:
                pass
    return None

def safe_select_text(soup, selectors):
    """Try a list of selectors and return the first non-empty text (strip)."""
    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            text = el.get_text(strip=True)
            if text:
                return text
    return ""

def extract_product_info(product_url):
    """Return a dict containing scraped product info and variants list."""
    soup, html = get_soup(product_url)

    # handle = slug from URL or data-slug attribute
    parsed = urlparse(product_url)
    handle = parsed.path.rstrip('/').split('/')[-1]

    # Title
    title = safe_select_text(soup, [
        '[data-hook="product-page"] h1',
        '[data-hook="product-item-name"]',
        '[data-hook="product-item-product-details"] h1',
        'meta[property="og:title"]',
        'title'
    ])
    if not title:
        # try alt of main image
        img = soup.select_one('[data-hook="main-media"] img, [data-hook="ProductImageDataHook.ProductImage"] img, [data-hook="ProductMediaDataHook.Images"] img')
        if img and img.get("alt"):
            title = img.get("alt").strip()

    # Description (HTML)
    desc_el = soup.select_one('[data-hook="product-item-product-details"], [data-hook="product-description"], .product-description, [data-hook="product-page"] [itemprop="description"]')
    if desc_el:
        body_html = str(desc_el)
    else:
        # fallback to meta description
        meta_desc = soup.select_one('meta[name="description"]')
        body_html = meta_desc['content'] if meta_desc and meta_desc.get('content') else ""

    # SEO
    seo_title = soup.select_one('meta[property="og:title"]')
    seo_title = seo_title['content'] if seo_title and seo_title.get('content') else title
    seo_desc = soup.select_one('meta[name="description"]')
    seo_desc = seo_desc['content'] if seo_desc and seo_desc.get('content') else ""

    # Vendor: try to find breadcrumb or site name
    vendor = safe_select_text(soup, ['[data-hook="breadcrumbs"] a[href*="//"]', '.site-vendor', '.vendor']) or urlparse(product_url).hostname or ""

    # Type / tags: attempt from breadcrumbs or tags area
    breadcrumbs = soup.select_one('[data-hook="breadcrumbs"]')
    product_type = ""
    tags = ""
    if breadcrumbs:
        crumbs = [a.get_text(strip=True) for a in breadcrumbs.select('a') if a.get_text(strip=True)]
        # last crumb is product name, previous can be collection = type
        if len(crumbs) >= 2:
            product_type = crumbs[-2]
        tags = ", ".join(crumbs[:-1])
    # fallback tags from meta keywords
    if not tags:
        meta_kw = soup.select_one('meta[name="keywords"]')
        tags = meta_kw['content'] if meta_kw and meta_kw.get('content') else ""

    # Images: gather all product images on the product page
    images = []
    # gallery images
    for img in soup.select('[data-hook="ProductImageDataHook.ProductImage"] img, [data-hook="ProductImageDataHook.Container"] img, [data-hook="ProductMediaDataHook.Images"] img, .main-media-image-wrapper-hook img'):
        src = img.get("src") or img.get("data-src") or img.get("data-ssr-src")
        if src:
            images.append(urljoin(product_url, src.split('?')[0]))
    # dedupe while preserving order
    seen = set()
    images = [x for x in images if not (x in seen or seen.add(x))]

    # Price: try common selectors
    price = safe_select_text(soup, [
        '[data-hook*="price"]', '.price', '.product-price', '[itemprop="price"]', 'meta[itemprop=price]'
    ])
    # If meta tag numeric:
    if not price:
        meta_price = soup.select_one('meta[itemprop=price], meta[property="product:price:amount"]')
        if meta_price and meta_price.get('content'):
            price = meta_price.get('content')

    # Options & option values
    options = []   # list of {"name": "Size", "values": ["S","M"]}
    # Wix option container example: [data-hook="options-dropdown-container"]
    for opt_container in soup.select('[data-hook="options-dropdown-container"], .options, [data-hook^="options-"]'):
        # find label
        label = opt_container.select_one('label[data-hook="dropdown-label"], label')
        name = label.get_text(strip=True) if label else opt_container.get('data-option-name') or opt_container.get('data-hook')
        # find option values inside dropdown
        vals = []
        # try option elements inside a dropdown menu
        for opt in opt_container.select('[role="option"], [data-hook="dropdown-option"], option, .dropdown-option, .option'):
            txt = opt.get_text(strip=True)
            if txt:
                vals.append(txt)
        # sometimes the selected value is visible in a button span
        if not vals:
            sel = opt_container.select_one('[data-hook="dropdown-base-text"], [data-hook="dropdown-base"] .value, button[data-hook="dropdown-base"] .slIfz_k, button .slIfz_k')
            if sel and sel.get_text(strip=True):
                # can't get alternatives from catalog grid; at least capture the current selection as single value
                vals = [sel.get_text(strip=True)]
        if name and vals:
            # clean up name: remove trailing asterisk etc
            name = re.sub(r'[\*\s]+$', '', name).strip()
            options.append({"name": name, "values": vals})

    # Attempt to parse embedded JSON for variant-level data (sku, price, inventory, option combinations)
    variants_json = extract_json_variants_from_html(html)
    structured_variants = None
    if variants_json:
        # normalize to list of dicts with keys we expect
        structured_variants = []
        for v in variants_json:
            if not isinstance(v, dict):
                continue
            structured_variants.append(v)

    # Build variant combinations
    rows_variants = []
    if options:
        # build product of option values
        option_names = [o['name'] for o in options][:3]   # limit to 3 options (Shopify)
        option_values_lists = [o['values'] for o in options][:3]
        for combo in product(*option_values_lists):
            # attempt to match to structured_variants by option values if available
            matched = {}
            sku = ""
            v_price = price or ""
            inv_qty = ""
            barcode = ""
            variant_image = ""
            # try to find a structured variant by matching option values
            if structured_variants:
                for sv in structured_variants:
                    # common fields for matching: option1/option2, title, name
                    sv_options = []
                    for k in ("option1", "option2", "option3", "name", "title"):
                        if k in sv and isinstance(sv[k], str):
                            # split names on ' / ' or ' - '
                            sv_options += [s.strip() for s in re.split(r'[/\-\\]', sv[k]) if s.strip()]
                    # also check properties that might hold options list
                    if all(any(c.lower() in (s.lower() if isinstance(s,str) else "") for s in sv_options) for c in combo):
                        sku = sv.get("sku", "") or sv.get("id", "")
                        v_price = sv.get("price", v_price)
                        inv_qty = sv.get("inventory_quantity", sv.get("inventory", inv_qty))
                        barcode = sv.get("barcode", "")
                        # variant image mapping
                        variant_image = sv.get("image") or sv.get("featured_image") or ""
                        break
            # fallback to default price and no sku
            row = {
                "option_names": option_names,
                "option_values": combo,
                "sku": sku,
                "price": v_price,
                "inventory": inv_qty,
                "barcode": barcode,
                "variant_image": variant_image
            }
            rows_variants.append(row)
    else:
        # no options: create single default variant
        rows_variants.append({
            "option_names": [],
            "option_values": [],
            "sku": "",
            "price": price or "",
            "inventory": "",
            "barcode": "",
            "variant_image": ""
        })

    product_data = {
        "handle": handle,
        "title": title,
        "body_html": body_html,
        "vendor": vendor,
        "type": product_type,
        "tags": tags,
        "published": "TRUE",
        "seo_title": seo_title,
        "seo_description": seo_desc,
        "images": images,
        "variants_rows": rows_variants
    }
    return product_data

def convert_to_shopify_rows(product_data):
    """Given parsed product_data, return list of CSV rows in Shopify format (one row per variant)."""
    rows = []
    images = product_data["images"]
    # create mapping of image positions
    for idx, v in enumerate(product_data["variants_rows"]):
        # base fields
        handle = product_data["handle"]
        title = product_data["title"]
        body_html = product_data["body_html"]
        vendor = product_data["vendor"]
        type_ = product_data["type"]
        tags = product_data["tags"]
        published = product_data["published"]
        seo_title = product_data["seo_title"]
        seo_desc = product_data["seo_description"]

        # options
        opt_names = v["option_names"]
        opt_values = v["option_values"]
        # fill up to 3 options
        option1_name = opt_names[0] if len(opt_names) > 0 else ""
        option2_name = opt_names[1] if len(opt_names) > 1 else ""
        option3_name = opt_names[2] if len(opt_names) > 2 else ""
        option1_value = opt_values[0] if len(opt_values) > 0 else ""
        option2_value = opt_values[1] if len(opt_values) > 1 else ""
        option3_value = opt_values[2] if len(opt_values) > 2 else ""

        # image selection: try variant image first, else image by index
        variant_image = v.get("variant_image") or ""
        image_src = ""
        image_position = ""
        if variant_image:
            image_src = variant_image
            image_position = 1
        else:
            # try align variant index to images list position (modulo)
            if images:
                image_src = images[idx] if idx < len(images) else images[0]
                image_position = (images.index(image_src) + 1) if image_src in images else 1

        row = {
            "Handle": handle,
            "Title": title,
            "Body (HTML)": body_html,
            "Vendor": vendor,
            "Type": type_,
            "Tags": tags,
            "Published": published,
            "Option1 Name": option1_name,
            "Option1 Value": option1_value,
            "Option2 Name": option2_name,
            "Option2 Value": option2_value,
            "Option3 Name": option3_name,
            "Option3 Value": option3_value,
            "Variant SKU": v.get("sku", ""),
            "Variant Grams": "",
            "Variant Inventory Tracker": "",
            "Variant Inventory Qty": v.get("inventory", ""),
            "Variant Inventory Policy": "deny",
            "Variant Fulfillment Service": "manual",
            "Variant Price": v.get("price", ""),
            "Variant Compare at Price": "",
            "Variant Requires Shipping": "TRUE",
            "Variant Taxable": "TRUE",
            "Variant Barcode": v.get("barcode", ""),
            "Image Src": image_src,
            "Image Position": image_position,
            "Gift Card": "FALSE",
            "SEO Title": seo_title,
            "SEO Description": seo_desc,
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
            "Variant Image": v.get("variant_image", ""),
            "Variant Weight Unit": "",
            "Variant Tax Code": "",
            "Cost per item": ""
        }
        rows.append(row)

    # Also include extra image-only rows for additional product images (Shopify expects image rows with empty variant columns)
    # Shopify accepts images associated to a Handle in additional rows where Title is blank and only Image Src/Image Position are present.
    # We'll append separate rows for each extra image to ensure they are imported.
    if len(product_data["images"]) > 1:
        for pos, img in enumerate(product_data["images"], start=1):
            # create an image-only row (Title blank but Handle present). Keep variant columns empty.
            img_row = {k: "" for k in CSV_FIELDS}
            img_row["Handle"] = product_data["handle"]
            img_row["Image Src"] = img
            img_row["Image Position"] = pos
            # It's helpful to include Title only on the first image row in Shopify format. But to keep consistent, we won't duplicate content.
            rows.append(img_row)

    return rows

def save_to_csv(rows, out_path=OUTPUT_CSV):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {out_path}")

def main():
    # Step 1: gather product links from the start/category page
    product_links = find_product_links_from_category(START_URL)
    # If you already have a short list, you can replace product_links with it.
    all_csv_rows = []
    for idx, purl in enumerate(product_links, start=1):
        try:
            print(f"[{idx}/{len(product_links)}] Fetching {purl}")
            prod = extract_product_info(purl)
            rows = convert_to_shopify_rows(prod)
            all_csv_rows.extend(rows)
        except Exception as e:
            print(f"Error fetching {purl}: {e}")
        time.sleep(DELAY)

    # Save
    save_to_csv(all_csv_rows, OUTPUT_CSV)

if __name__ == "__main__":
    main()
