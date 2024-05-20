import os
import json


def add_marketplace_to_json(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            marketplace_name = os.path.splitext(filename)[
                0
            ]  # Extracts file name without the extension
            with open(filepath, "r+") as file:
                data = json.load(file)
                if isinstance(data, list):  # Check if data is a list
                    for item in data:
                        item["Marketplace"] = (
                            marketplace_name  # Add marketplace name to each item
                        )
                elif isinstance(data, dict):  # If the JSON is a single dictionary
                    data["Marketplace"] = (
                        marketplace_name  # Add marketplace name to the dictionary
                    )
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()  # Removes remaining part of old data if new data is shorter
                print(f'Marketplace "{marketplace_name}" added to {filename}')


# Call the function with the path to your 'json' folder
add_marketplace_to_json("data/json")
