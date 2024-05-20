import pandas as pd
import json


def load_data_from_json(file_path):
    # Load data from JSON file
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def calculate_products_per_market(data):
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    # Count number of products per market
    products_per_market = df["Marketplace"].value_counts().reset_index()
    products_per_market.columns = ["Marketplace", "Number of Products"]
    return products_per_market


def calculate_average_prices(data):
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    # Group data by marketplace and calculate average price
    average_prices = df.groupby("Marketplace")["Price"].mean().reset_index()
    return average_prices


def calculate_drug_type_market_share(data):
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    # Calculate market share of drug types
    drug_type_market_share = df["Type"].value_counts(normalize=True).reset_index()
    drug_type_market_share.columns = ["Type", "Market Share"]
    return drug_type_market_share


def filter_country_data(data):
    # Filter data to exclude entries with 'X' as country
    filtered_data = [entry for entry in data if entry["product_country"] != "X"]
    return filtered_data


def create_country_heatmap_data(data):
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    # Group data by country and count the number of products in each country
    country_counts = df["product_country"].value_counts().reset_index()
    country_counts.columns = ["Country", "Number of Products"]
    return country_counts


def filter_data(data, marketplace):
    # Filter data based on selected marketplace and exclude entries with 'X' as seller
    filtered_data = [
        entry
        for entry in data
        if entry["Marketplace"] == marketplace and entry["product_seller"] != "X"
    ]
    return filtered_data


def calculate_products_per_seller(data):
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    # Group data by seller and count the number of products per seller
    seller_counts = df["product_seller"].value_counts().reset_index()
    seller_counts.columns = ["Seller", "Number of Products"]
    return seller_counts
