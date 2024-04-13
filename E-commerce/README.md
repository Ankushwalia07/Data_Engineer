# E-Commerce Product Aggregator

This project is a Python-based web scraping tool that aggregates product information from multiple e-commerce websites. It utilizes techniques such as dynamic web scraping, data processing, and storage in both relational and NoSQL databases.

## Features

- Scrapes product information from popular e-commerce websites such as Amazon, eBay, and Walmart.
- Utilizes Selenium for dynamic web scraping and handles asynchronous JavaScript rendering.
- Cleans and preprocesses scraped product data to ensure consistency and accuracy.
- Stores processed product data in both SQLite and MongoDB databases.
- Implements parallel processing techniques for efficient scraping performance.

## Usage

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository to your local machine.
3. Install the required Python dependencies by running:

pip install -r requirements.txt

4. Download and install the appropriate Chrome WebDriver for your system and update the path to the WebDriver in the `scrape.py` script.
5. Customize the list of target websites and other parameters in the `main.py` script as needed.
6. Run the project by executing the `main.py` script: 

 python main.py