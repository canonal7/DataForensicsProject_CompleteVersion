import json
import re


def standardize_prices(input_file, output_file):
    with open(input_file, "r") as file:
        data = json.load(file)

    # Process each item in the data
    for item in data:
        price = item.get("Price", "X")
        if price != "X":
            # Extract numeric value from the price string
            numeric_price = re.findall(r"\d+", price.replace(",", "").replace("$", ""))
            if numeric_price:
                # Convert the first found numeric value to integer
                item["Price"] = int(numeric_price[0])
            else:
                # If no numeric value is found, set price as 'X'
                item["Price"] = "X"

    # Save the processed data back to a new JSON file
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)
        print(f"Processed data has been saved to {output_file}")


# Call the function with the path to your combined JSON file and the output file path
standardize_prices("data/json/combined_data.json", "data/json/standardized_data.json")
