# Step 4: Data Processing and Cleaning

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

# Print the cleaned product titles
print("Cleaned Product Titles from Amazon:")
for title in cleaned_titles:
    print("-", title)

# Close the browser
driver.quit()
