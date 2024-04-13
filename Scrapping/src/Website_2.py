import requests
from bs4 import BeautifulSoup
import json
import os
import re

base_url = "https://www.lechocolat-alainducasse.com/uk/"

url_patterns = [
    "easter-chocolate",
    "chocolates",
    "chocolate-bar",
    "chocolate-gift",
    "simple-pleasures",
    "breakfast-snacks"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

product_links = []

try:
    for pattern in url_patterns:
        url = base_url + pattern
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        product_list = soup.find_all('section', class_="productMiniature__data")
        for item in product_list:
            for link in item.find_all('a', href=True):
                product_links.append((link['href'], pattern))  # Tuple of (product link, category)

    # Scraping additional information
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Find brand name
    brand_name_tag = soup.find('title')
    brand_name = brand_name_tag.get_text(strip=True) if brand_name_tag else None

    # Find brand description
    brand_description_tag = soup.find('div', class_='homeDoublePad__text')
    brand_description = '\n'.join([p.get_text(strip=True) for p in brand_description_tag.find_all('p')]) if brand_description_tag else None

    # Find image URL
    image_url_tag = soup.find('img', class_='lazyloadBox')
    image_url = image_url_tag['src'] if image_url_tag else None

    scraped_data_list = []

    for link, category in product_links:
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")

        try:
            h1_tag = soup.find('div', class_='productCard__name').find('h1', class_='productCard__title')
            name = h1_tag.get_text(separator=' ', strip=True) if h1_tag else None
        except AttributeError:
            name = None

        # Find product price
        try:
            price_button = soup.find('button', class_='productActions__addToCart')
            price_text = price_button.get_text(strip=True) if price_button else None
            price_match = re.search(r'[£€](\d+\.\d+)', price_text) if price_text else None
            price = price_match.group(1) if price_match else None
        except AttributeError:
            price = None

        # Find product image URL
        try:
            photo_wrapper = soup.find('div', class_='productMiniature__thumbnails')
            img_tag = photo_wrapper.find('img') if photo_wrapper else None
            image_url = img_tag['src'] if img_tag else None
        except (AttributeError, KeyError):
            image_url = None

        # Find product description
        try:
            description_tag = soup.find('div', class_='productAccordion__content js-tab-content',
                                        attrs={'data-content': ''})
            description = description_tag.get_text(separator=' ', strip=True) if description_tag else None
        except AttributeError:
            description = None

        # Find product subtitle
        try:
            subtitle_tag = soup.find('h2', class_='productCard__subtitle')
            subtitle = subtitle_tag.get_text(separator=' ', strip=True) if subtitle_tag else None
        except AttributeError:
            subtitle = None

        # Find allergens
        try:
            allergens_tag = description_tag.find('h3', string='Allergens')
            allergens = allergens_tag.find_next_sibling('p').get_text(strip=True) if allergens_tag else None
        except AttributeError:
            allergens = None

        # Find price per kilo
        try:
            price_per_kilo_tag = description_tag.find('h3', string='Price per kilo')
            price_per_kilo = price_per_kilo_tag.find_next_sibling('p').get_text(strip=True) if price_per_kilo_tag else None
        except AttributeError:
            price_per_kilo = None

        # Find consume advice
        try:
            consume_advice_tag = soup.find('p', class_='consumeAdvices')
            consume_advice = consume_advice_tag.get_text(separator=' ', strip=True) if consume_advice_tag else None
        except AttributeError:
            consume_advice = None

        # Find product weight
        try:
            weight_tag = soup.find('p', class_='productCard__weight')
            weight = weight_tag.get_text(separator=' ', strip=True) if weight_tag else None
        except AttributeError:
            weight = None

        # Vegan status
        try:
            vegan_tag = soup.find('h3', class_='wysiwyg-title-default', string='Vegan')
            vegan_status = vegan_tag.find_next_sibling('p').get_text(strip=True) if vegan_tag else None
        except AttributeError:
            vegan_status = None

        scraped_data = {
            'name': name,
            'price': price,
            'image_url': image_url,
            'consume_advice': consume_advice,
            'weight': weight,
            'subtitle': subtitle,
            'allergens': allergens,
            'price_per_kilo': price_per_kilo,
            'description': description,
            'category': category,  # Adding category information
            'vegan_status': vegan_status
        }

        # Remove escape characters from text data
        for key, value in scraped_data.items():
            if isinstance(value, str):
                scraped_data[key] = value.replace('\n', '').replace('\t', '').strip()

        scraped_data_list.append(scraped_data)

    output_dir = 'output'

    # Ensure the directory exists, create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    json_filename = os.path.join(output_dir, 'scraped_data_lechocolat.json')

    # Writing to JSON file
    with open(json_filename, 'w') as json_file:
        json.dump({
            "brand_info": {
                "brand_name": brand_name,
                "brand_description": brand_description,
                "image_url": image_url
            },
            "products": scraped_data_list
        }, json_file, indent=4)

except Exception as e:
    print("An error occurred:", e)
