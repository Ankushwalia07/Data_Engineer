# Step 5: Relational Database Storage

import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Set up Chrome WebDriver (change path to your chromedriver executable)
webdriver_service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=webdriver_service)

# URL of the target website (Amazon in this example)
url = "https://www.amazon.com/"

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

# Store data in SQLite database
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Create a table for products
c.execute('''CREATE TABLE IF NOT EXISTS products
             (id INTEGER PRIMARY KEY, title TEXT)''')

# Insert cleaned product titles into the database
for title in cleaned_titles:
    c.execute("INSERT INTO products (title) VALUES (?)", (title,))

# Commit changes and close connection
conn.commit()
conn.close()

# Print a message indicating successful data storage
print("Processed product data stored in SQLite database.")

# Close the browser
driver.quit()



""""
For Nosql Database (MangoDB)

# Step 6: NoSQL Database Storage

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pymongo

# Set up Chrome WebDriver (change path to your chromedriver executable)
webdriver_service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=webdriver_service)

# URL of the target website (Amazon in this example)
url = "https://www.amazon.com/"

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

# Store data in MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["eCommerceDB"]
collection = db["products"]

# Insert cleaned product titles into the database
for title in cleaned_titles:
    product = {"title": title}
    collection.insert_one(product)

# Print a message indicating successful data storage
print("Processed product data stored in MongoDB.")

# Close the browser
driver.quit()

"""