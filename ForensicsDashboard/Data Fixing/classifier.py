from openai import OpenAI
import json
import os

client = OpenAI()


def classify_product(product_name):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Please enter the product name from the list below, and I will classify it into the correct drug category based on its characteristics. The available categories include Opioids, Stimulants, Cannabinoids, Depressants, Hallucinogens, Dissociatives, Inhalants, and Others JUST REPLY WITH ONE TYPE, DO NOT SAY ANYTHING ELSE OTHER THAN THE TYPE, IF YOU CANT CLASSIFY JUST SAY OTHERS.",
            },
            {
                "role": "user",
                "content": product_name,
            },
        ],
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def update_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r+") as file:
                data = json.load(file)
                if isinstance(data, list):  # Check if data is a list
                    for item in data:  # Process each item in the list
                        product_name = item.get("Product")
                        if product_name:
                            drug_type = classify_product(product_name)
                            item["Type"] = (
                                drug_type  # Adding the classified drug type to the item
                            )
                            print(
                                f'Updated item with product "{product_name}" with drug type {drug_type}'
                            )
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                else:
                    print(f"No list found in file {filename}")


update_json_files("data/json")
