import os
import json


def combine_json_files(directory, output_file):
    all_data = []  # List to store all objects from all files

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            marketplace_name = os.path.splitext(filename)[
                0
            ]  # Extracts file name without the extension

            with open(filepath, "r") as file:
                data = json.load(file)
                if isinstance(data, list):  # Check if data is a list
                    for item in data:
                        standardized_item = standardize_data(item, marketplace_name)
                        all_data.append(standardized_item)
                elif isinstance(data, dict):  # If the JSON is a single dictionary
                    standardized_item = standardize_data(data, marketplace_name)
                    all_data.append(standardized_item)

    # Write all combined data to a new JSON file
    with open(output_file, "w") as file:
        json.dump(all_data, file, indent=4)
        print(f"All data has been combined and saved to {output_file}")


def standardize_data(item, marketplace_name):
    # Define the attributes with default value 'X' if not found in the item
    attributes = {
        "Product": item.get("Product", "X"),
        "Price": item.get("Price", "X"),
        "Type": item.get("Type", "X"),
        "product_seller": item.get("product_seller", "X"),
        "Marketplace": marketplace_name,
        "product_country": item.get("product_country", "X"),
    }
    return attributes


# Call the function with the path to your 'json' folder and the desired output file path
combine_json_files("data/json", "data/json/combined_data.json")
