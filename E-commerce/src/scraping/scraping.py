# Step 2: Web Scraping with Selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Set up Chrome WebDriver (change path to your chromedriver executable)
webdriver_service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=webdriver_service)

# URL of the target website (Amazon in this example)
url = "https://www.amazon.com/"

# Open the website in the browser
driver.get(url)

# Find and scrape product titles
product_titles = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")

# Print the scraped product titles
print("Scraped Product Titles from Amazon:")
for title in product_titles:
    print("-", title.text)

# Close the browser
driver.quit()
