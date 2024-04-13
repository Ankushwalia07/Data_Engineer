import requests
from bs4 import BeautifulSoup
import json
import os

# Common part of the URLs
common_url = "https://foreignfortune.com/collections/"

# URL patterns for varying parts
url_patterns = [
    "frontpage?page={x}",
    "men-unisex?page={x}",
    "foreign-accesories?page={x}",
    "women",
    "kids",
    "coats-hats",
    "small-logo-embroidery-t-shirts-1"
]

base_urls = []

for url_pattern in url_patterns:
    if "?" in url_pattern:
        for x in range(1, 4):
            base_urls.append((common_url + url_pattern.format(x=x), url_pattern.split('?')[0]))
    else:
        base_urls.append((common_url + url_pattern, url_pattern))

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

product_links = []
brand_name = "Foreign Fortune Clothing"
brand_description = "Foreign Fortune Clothing is a unisex clothing line that provides top quality products at affordable prices. We also do customized outfits and wholesale orders."
brand_image = "https://cdn.shopify.com/s/files/1/0094/9921/3881/products/124530F4-F4CC-45A0-A5CF-D44F6E95E59C_1242x.jpg?v=1604345903"

try:
    for url, category in base_urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        product_list = soup.find_all('div', class_="grid grid--uniform grid--view-items")
        for item in product_list:
            for link in item.find_all("a", href=True):
                product_links.append(("https://foreignfortune.com" + link['href'], category))

    scraped_data_list = []

    for link, category in product_links:
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")

        name = soup.find('h1', class_="product-single__title").text.strip()
        photo_wrapper = soup.find('div', class_='product-single__photo-wrapper')

        # Extract all available sizes
        size_select = soup.find('select', id="SingleOptionSelector-0")
        available_sizes = [size.text.strip() for size in size_select.find_all('option')] if size_select else []

        # Extract all available colors
        color_select = soup.find('select', id="SingleOptionSelector-1")
        available_colors = [color.text.strip() for color in color_select.find_all('option')] if color_select else []

        img_tag = photo_wrapper.find('img')
        try:
            image_url = img_tag['src']
        except:
            image_url = None

        variants = []
        # Extract variant details
        for color in available_colors:
            for size in available_sizes:
                variant = {
                    'color': color,
                    'size': size
                }
                variants.append(variant)

        product_data = {
            'name': name,
            'image_url': image_url,
            'variants': variants,
            'category': category  # Include category information
        }

        scraped_data_list.append(product_data)

    output_dir = 'output'

    # Ensure the directory exists, create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_filename = os.path.join(output_dir, 'scraped_data_foreignfortune.json')

    with open(json_filename, 'w') as json_file:
        json.dump({
            'brand': brand_name,
            'description': brand_description,
            'image': brand_image,
            'products': scraped_data_list
        }, json_file, indent=4)

except Exception as e:
    print("An error occurred:", e)
