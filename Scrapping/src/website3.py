import os
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

# Define base URL
base_url = "https://www.traderjoes.com"

# Define URL patterns
url_patterns = [
    '/home/products/category/bakery-11?filters=%7B"page"%3A{x}%7D',
    '/home/products/category/cheese-29?filters=%7B"page"%3A{x}%7D',
    # '/home/products/category/dairy-and-eggs-44?filters=%7B"page"%3A{x}%7D',
    # '/home/products/category/fresh-prepared-foods-80?filters=%7B"page"%3A{x}%7D',
    # '/home/products/category/from-the-freezer-95?filters=%7B"page"%3A{x}%7D',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

# Initialize the webdriver
driver = webdriver.Chrome()

try:
    # Initialize list to store scraped data
    scraped_data_list = []

    # Iterate over URL patterns
    for pattern in url_patterns:
        # Initialize list to store product links for each pattern
        product_links = []

        # Iterate over pages
        for x in range(1, 3):
            url = base_url + pattern.format(x=x)
            driver.get(url)

            # Wait for the page to load
            wait = WebDriverWait(driver, 10)
            try:
                product_list_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.ProductCard_card__4WAOg"))
                wait.until(product_list_present)
            except TimeoutError:
                print("Timeout: Product list not found on", url)
                continue

            # Get the page source after the JavaScript has rendered everything
            page_source = driver.page_source

            # Parse the HTML content
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find all product listings
            product_list = soup.find_all('section', class_="ProductCard_card__4WAOg")
            for item in product_list:
                for link in item.find_all('a', href=True):
                    product_links.append(base_url + link['href'])

            # Loop through each product listing and extract information
            for link in product_links:
                try:
                    driver.get(link)

                    # Wait for the product details to load
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.ProductDetails_main__title__14Cnm")))

                    # Get the page source after the JavaScript has rendered everything
                    page_source = driver.page_source

                    # Parse the HTML content
                    soup = BeautifulSoup(page_source, 'html.parser')

                    # Extract product details
                    product_title = soup.find('h1', class_="ProductDetails_main__title__14Cnm").text.strip()

                    description_div = soup.find('div', class_='Expand_expand__container__3COzO')
                    description = description_div.get_text(strip=True) if description_div else "N/A"

                    nutrition_div = soup.find('div', class_='NutritionFacts_nutritionFacts__1Nvz0')
                    serving_size = nutrition_div.find('div', text='serving size').find_next_sibling('div').text.strip()
                    calories_per_serving = nutrition_div.find('div', text='calories per serving').find_next_sibling('div').text.strip()

                    nutrients_table = []
                    for row in nutrition_div.find('table', class_='Item_table__2PMbE').find_all('tr'):
                        columns = row.find_all('td')
                        row_data = {f"column_{i + 1}": column.get_text(strip=True) for i, column in enumerate(columns)}
                        nutrients_table.append(row_data)

                    price_div = soup.find('div')
                    price = price_div.find('span', class_='ProductPrice_productPrice__price__3-50j').get_text(strip=True)
                    unit = price_div.find('span', class_='ProductPrice_productPrice__unit__2jvkA').get_text(strip=True)

                    # Store the scraped data
                    data = {
                        "title": product_title,
                        "description": description,
                        "serving_size": serving_size,
                        "calories_per_serving": calories_per_serving,
                        "price": price,
                        "unit": unit,
                        "nutrients_table": nutrients_table
                    }
                    scraped_data_list.append(data)
                except TimeoutException as ex:
                    print("Timeout occurred while waiting for element:", ex)
except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()

    # Output directory
    output_dir = '../output'

    # Ensure the directory exists, create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # JSON filename
    json_filename = os.path.join(output_dir, 'scraped_data_traderjoes.json')

    # Write scraped data to JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(scraped_data_list, json_file, indent=4)

    print("Scraped data has been saved to:", json_filename)
