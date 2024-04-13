import json
import os

class Validation:
    @staticmethod
    def validate_foreignfortune(data):
        errors = []
        # Add validation rules specific to foreignfortune.com
        for product in data:
            # Check if each product has a name, image URL, and belongs to a category
            if 'name' not in product:
                errors.append("Title is missing for product: {}".format(product.get('price', 'Unknown')))
            if 'image_url' not in product:
                errors.append("Image URL is missing for product: {}".format(product.get('name', 'Unknown')))
            if 'category' not in product:
                errors.append("Category is missing for product: {}".format(product.get('name', 'Unknown')))
            # Additional checks for variants
            if 'variants' in product:
                for variant in product['variants']:
                    if 'color' not in variant or 'size' not in variant:
                        errors.append("Variant information incomplete for product: {}".format(product.get('name', 'Unknown')))
        return errors

    @staticmethod
    def validate_lechocolat(data):
        errors = []
        # Add validation rules specific to lechocolat-alainducasse.com
        for product in data:
            # Check if each product has a name, price, image URL, and consume advice
            if 'name' not in product:
                errors.append("Title is missing for product: {}".format(product.get('price', 'Unknown')))
            if 'price' not in product:
                errors.append("Price is missing for product: {}".format(product.get('name', 'Unknown')))
            if 'image_url' not in product:
                errors.append("Image URL is missing for product: {}".format(product.get('name', 'Unknown')))
            if 'consume_advice' not in product:
                errors.append("Consume advice is missing for product: {}".format(product.get('name', 'Unknown')))
            # Additional checks for weight and allergens
            if 'weight' not in product:
                errors.append("Weight is missing for product: {}".format(product.get('name', 'Unknown')))
            if 'allergens' not in product:
                errors.append("Allergens information is missing for product: {}".format(product.get('name', 'Unknown')))
        return errors

    @staticmethod
    def validate_traderjoes(data):
        errors = []
        # Add validation rules specific to traderjoes.com
        for product in data:
            # Check if each product has a name, category, and price
            if 'Product Name' not in product:
                errors.append("Name is missing for product: {}".format(product.get('Category', 'Unknown')))
            if 'Category' not in product:
                errors.append("Category is missing for product: {}".format(product.get('Product Name', 'Unknown')))
            if 'Price' not in product:
                errors.append("Price is missing for product: {}".format(product.get('Product Name', 'Unknown')))
        return errors

# Load scraped data from JSON files
output_dir = 'output'
json_files = [
    'scraped_data_foreignfortune.json',
    'scraped_data_lechocolat.json',
    'scraped_data_traderjoes.json'
]

validation_errors = {}

for json_file in json_files:
    file_path = os.path.join(output_dir, json_file)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Determine which validation method to use based on the file name
        if 'foreignfortune' in json_file:
            validation_errors[json_file] = Validation.validate_foreignfortune(data)
        elif 'lechocolat' in json_file:
            validation_errors[json_file] = Validation.validate_lechocolat(data)
        elif 'traderjoes' in json_file:
            validation_errors[json_file] = Validation.validate_traderjoes(data)
    else:
        print("File {} does not exist.".format(json_file))

# Print validation errors
for file, errors in validation_errors.items():
    print("Validation errors for {}:".format(file))
    if errors:
        for error in errors:
            print("- ", error)
    else:
        print("No validation errors found for {}.".format(file))
