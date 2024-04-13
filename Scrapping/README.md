# Web Scraping Project

This project involves scraping data from three different websites: ForeignFortune, Le Chocolat Alain Ducasse, and Trader Joe's. The scraped data is stored in JSON format in the `output` directory.

## Project Structure

The project has the following structure:

- **output**: Contains the JSON files with scraped data.
- **src/components**: Contains the main scraping scripts for each website.
- **setup.py**: Python script for setting up the project dependencies.
- **validation.py**: Python script for validating the scraped data.
- **requirements.txt**: Text file listing project dependencies.

## Components

### 1. `foreignfortune_scraper.py`

This script scrapes data from ForeignFortune.com and stores it in JSON format in the `output` directory.

### 2. `lechocolat_scraper.py`

This script scrapes data from LeChocolat-AlainDucasse.com (UK-based products only) and stores it in JSON format in the `output` directory.

### 3. `traderjoes_scraper.py`

This script scrapes data from TraderJoes.com and stores it in JSON format in the `output` directory.

## Validation

The `validation.py` script contains validation rules for ensuring the quality of the scraped data. It validates each JSON file against specific criteria depending on the website.


## Usage
1. Navigate to the src/components directory.
2. Run each scraper script to scrape data from the respective websites.
3. Once the scraping is complete, run the validation.py script to validate the scraped data.

## Contributors : ANKUSH WALIA