# Step 7: Parallel Processing and Throttling

import concurrent.futures
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pymongo
import sqlite3

# Function to scrape product titles from a target website
def scrape_titles(url):
    # Set up Chrome WebDriver (change path to your chromedriver executable)
    webdriver_service = Service('/path/to/chromedriver')
    driver = webdriver.Chrome(service=webdriver_service)
    
    # Open the website in the browser
    driver.get(url)

    # Wait for dynamic content to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")))

    # Find and scrape product titles
    product_titles = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")

    # Clean and preprocess product titles
    cleaned_titles = []
    for title in product_titles:
        # Remove HTML tags from product title using regex
        cleaned_title = re.sub('<.*?>', '', title.get_attribute('innerHTML'))
        cleaned_titles.append(cleaned_title)

    # Close the browser
    driver.quit()

    return cleaned_titles

# Target websites for scraping
target_websites = [
    "https://www.amazon.com/",
    "https://www.ebay.com/",
    "https://www.walmart.com/"
]

# Throttle delay in seconds
throttle_delay = 2

# Store data in SQLite database
conn_sqlite = sqlite3.connect('products.db')
c = conn_sqlite.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS products
             (id INTEGER PRIMARY KEY, title TEXT)''')

# Store data in MongoDB database
client_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
db = client_mongo["eCommerceDB"]
collection = db["products"]

# Function to store data in SQLite and MongoDB
def store_data(cleaned_titles):
    for title in cleaned_titles:
        # SQLite
        c.execute("INSERT INTO products (title) VALUES (?)", (title,))
        # MongoDB
        product = {"title": title}
        collection.insert_one(product)
    conn_sqlite.commit()

# Function to scrape and store data from multiple websites
def scrape_and_store(url):
    cleaned_titles = scrape_titles(url)
    store_data(cleaned_titles)

# Throttle requests to prevent overwhelming the target websites
def throttle_requests():
    time.sleep(throttle_delay)

# Execute scraping and storing concurrently for each target website
with concurrent.futures.ThreadPoolExecutor(max_workers=len(target_websites)) as executor:
    # Submit scraping tasks
    scrape_futures = [executor.submit(scrape_and_store, url) for url in target_websites]
    
    # Throttle requests
    throttle_requests()

# Close SQLite connection
conn_sqlite.close()

# Print a message indicating successful data storage
print("Processed product data stored in SQLite database and MongoDB.")
