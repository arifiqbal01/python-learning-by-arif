import requests
import csv
import os

def get_csv_headers(filepath):
    """Reads the header row from the CSV file."""
    # Ensure the file exists before attempting to read headers
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"The file '{filepath}' was not found.")

    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Attempt to read the header row
        try:
            headers = next(reader)
        except StopIteration:
            # Handle empty file case if necessary, though a sample CSV should have headers
            raise ValueError(f"The CSV file '{filepath}' is empty or has no header row.")

    return headers

def append_products_to_csv(filepath, product_data_list, headers):
    """Appends the formatted product data to the CSV file."""
    file_exists = os.path.isfile(filepath)

    # Use 'a' to append to the file. 
    with open(filepath, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # If the file is new or empty, write the header
        if not file_exists or os.path.getsize(filepath) == 0:
            writer.writeheader()

        for product_rows in product_data_list:
            for row in product_rows:
                writer.writerow(row)

def process_product_urls(urls, csv_filepath):
    """
    Main function to process a list of product URLs and save data to a CSV.
    """
    try:
        headers = get_csv_headers(csv_filepath)
        print(f"Successfully read headers from '{csv_filepath}'.")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please make sure the sample CSV is correctly placed and contains headers.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV: {e}")
        return

    all_products_data = []

    for url in urls:
        try:
            handle = url.strip().split('/')[-1]
            if not handle: continue # Skip empty lines

            json_url = f"https://jollein.nl/products/{handle}.js"

            print(f"Fetching data for: {handle}...")
            response = requests.get(json_url)
            response.raise_for_status()

            product = response.json()
            print(f"Successfully fetched '{product.get('title', 'N/A')}'.")

            # --- Prepare data for CSV rows ---
            product_rows = []
            options = product.get('options', [])
            variants = product.get('variants', [])
            media = product.get('media', [])

            # 1. Process the first variant to create the main product row.
            if variants:
                first_variant = variants[0]

                # --- Option Names and Values (Issue 1 fix retained) ---
                option_names = [opt.get('name') for opt in options]

                opt1_name = option_names[0] if len(options) > 0 else 'Title'
                opt2_name = option_names[1] if len(options) > 1 else ''
                opt3_name = option_names[2] if len(options) > 2 else ''

                opt1_value = first_variant.get('option1') or ('Default Title' if not options else '')
                opt2_value = first_variant.get('option2', '') if opt2_name else ''
                opt3_value = first_variant.get('option3', '') if opt3_name else ''

                # --- Get Main Image Data (Issue 2 simplified) ---
                first_media = media[0] if media else {}

                main_image_src = first_media.get('src', '')
                main_image_position = first_media.get('position', 1)
                main_image_id = first_media.get('id')

                # Use the Handle if no media is present but variants exist (unlikely but safe)
                if not main_image_id and first_variant.get('featured_media'):
                     main_image_src = first_variant['featured_media'].get('src', '')
                     main_image_position = first_variant['featured_media'].get('position', 1)
                     main_image_id = first_variant['featured_media'].get('id')


                main_row = {header: '' for header in headers}
                main_row.update({
                    'Handle': product.get('handle', ''),
                    'Title': product.get('title', ''),
                    'Body (HTML)': product.get('description', ''),
                    'Vendor': product.get('vendor', ''),
                    'Type': product.get('type', ''),
                    'Tags': ', '.join(product.get('tags', [])),
                    'Published': 'TRUE' if product.get('published_at') else 'FALSE',

                    'Option1 Name': opt1_name,
                    'Option1 Value': opt1_value,
                    'Option2 Name': opt2_name,
                    'Option2 Value': opt2_value,
                    'Option3 Name': opt3_name,
                    'Option3 Value': opt3_value,

                    'Variant SKU': first_variant.get('sku', ''),
                    'Variant Grams': first_variant.get('grams', 0),
                    'Variant Inventory Tracker': 'shopify',
                    'Variant Inventory Qty': first_variant.get('inventory_quantity', 0),
                    'Variant Inventory Policy': 'deny' if not first_variant.get('inventory_management') else 'continue',
                    'Variant Fulfillment Service': 'manual',
                    'Variant Price': float(first_variant.get('price', 0)) / 100.0 if first_variant.get('price') else '',
                    'Variant Compare At Price': float(first_variant.get('compare_at_price', 0)) / 100.0 if first_variant.get('compare_at_price') else '',
                    'Variant Requires Shipping': 'TRUE' if first_variant.get('requires_shipping') else 'FALSE',
                    'Variant Taxable': 'TRUE' if first_variant.get('taxable') else 'FALSE',
                    'Variant Barcode': first_variant.get('barcode', ''),

                    'Image Src': main_image_src, # FIRST IMAGE URL ONLY
                    'Image Position': main_image_position,
                    'Image Alt Text': first_media.get('alt', ''),
                    'Gift Card': 'FALSE',
                    'Status': 'active'
                })
                product_rows.append(main_row)

                # 2. Process the rest of the variants.
                for variant in variants[1:]:
                    variant_row = {header: '' for header in headers}

                    # Logic for Option Values (Issue 1 fix)
                    opt2_value = variant.get('option2', '') if opt2_name else ''
                    opt3_value = variant.get('option3', '') if opt3_name else ''

                    # IMPORTANT CHANGE: Blank out Image Src for subsequent variants.
                    # We will rely on manually ordering images in Shopify later.
                    variant_image_src = '' 

                    variant_row.update({
                        'Handle': product.get('handle', ''),
                        'Option1 Value': variant.get('option1', ''),
                        'Option2 Value': opt2_value, 
                        'Option3 Value': opt3_value, 
                        'Variant SKU': variant.get('sku', ''),
                        'Variant Grams': variant.get('grams', 0),
                        'Variant Inventory Tracker': 'shopify',
                        'Variant Inventory Qty': variant.get('inventory_quantity', 0),
                        'Variant Inventory Policy': 'deny' if not variant.get('inventory_management') else 'continue',
                        'Variant Fulfillment Service': 'manual',
                        'Variant Price': float(variant.get('price', 0)) / 100.0 if variant.get('price') else '',
                        'Variant Compare At Price': float(variant.get('compare_at_price', 0)) / 100.0 if variant.get('compare_at_price') else '',
                        'Variant Requires Shipping': 'TRUE' if variant.get('requires_shipping') else 'FALSE',
                        'Variant Taxable': 'TRUE' if variant.get('taxable') else 'FALSE',
                        'Variant Barcode': variant.get('barcode', ''),
                        'Image Src': variant_image_src # Explicitly blank for simplicity
                    })
                    product_rows.append(variant_row)

                # 3. Add ALL remaining media links in separate rows.
                # Only exclude the single image used in the very first row.
                for media_item in media:
                    media_id = media_item.get('id')

                    # Add every media item *except* the one already used in the main product row
                    if media_id is not None and media_id != main_image_id:
                        image_row = {header: '' for header in headers}
                        image_row.update({
                            'Handle': product.get('handle', ''),
                            'Image Src': media_item.get('src', ''),
                            'Image Position': media_item.get('position', '')
                            # Note: No Image Alt Text is available for subsequent images in the CSV format unless retrieved from the media object
                        })
                        product_rows.append(image_row)

            all_products_data.append(product_rows)
            print(f"Completed processing for '{product.get('title', 'N/A')}'.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {url}. Error: {e}")

    if all_products_data:
        try:
            append_products_to_csv(csv_filepath, all_products_data, headers)
            print(f"\nData for {len(all_products_data)} products has been successfully appended to '{csv_filepath}'.")
        except Exception as e:
            print(f"An error occurred while writing to the CSV file: {e}")

if __name__ == "__main__":
    CSV_FILEPATH = 'products_sample.csv'
    PRODUCT_URLS = [
        "https://jollein.nl/products/baby-mobiel-teddy-bear",
        "https://jollein.nl/products/activiteitenkubus-animal-friends"
    ]
    process_product_urls(PRODUCT_URLS, CSV_FILEPATH)