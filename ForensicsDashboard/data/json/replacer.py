import json

# Step 1: Load the existing data from the file
with open("MidlandCity.json", "r") as file:
    data = json.load(file)

# Step 2: Prepare the new data format
new_data = []

# Assuming the number of items can be inferred from the keys
product_count = len([key for key in data if key.startswith("Product")])

for i in range(product_count):
    product_key = f"Product{i}"
    price_key = f"Price{i}"
    if product_key in data and price_key in data:
        new_item = {"Product": data[product_key], "Price": data[price_key]}
        new_data.append(new_item)

# Step 3: Overwrite the old file with the new data
with open("MidlandCity.json", "w") as file:
    json.dump(new_data, file, indent=4)

print("The file has been updated successfully.")
