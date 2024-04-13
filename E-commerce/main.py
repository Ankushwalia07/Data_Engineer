# main.py

from src.scraping.scrape import scrape_and_store
from src.scraping.clean import clean_data
from src.scraping.store_sqlite import store_in_sqlite
from src.scraping.store_mongodb import store_in_mongodb
from src.utils.throttle import throttle_requests

# Target websites for scraping
target_websites = [
    "https://www.amazon.com/",
    "https://www.ebay.com/",
    "https://www.walmart.com/"
]

# Throttle delay in seconds
throttle_delay = 2

def main():
    # Execute scraping and storing concurrently for each target website
    for url in target_websites:
        # Scrape and store data
        scrape_and_store(url)

        # Throttle requests
        throttle_requests(throttle_delay)

    # Clean the scraped data
    clean_data()

    # Store the cleaned data in SQLite database
    store_in_sqlite()

    # Store the cleaned data in MongoDB database
    store_in_mongodb()

    print("Processed product data stored in SQLite database and MongoDB.")

if __name__ == "__main__":
    main()
