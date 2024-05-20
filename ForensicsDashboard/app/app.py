from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from data import (
    load_data_from_json,
    calculate_products_per_market,
    calculate_average_prices,
    calculate_drug_type_market_share,
    filter_country_data,
    create_country_heatmap_data,
    filter_data,
    calculate_products_per_seller,
)


df = load_data_from_json("data/json/standardized_data.json")

products_per_market = calculate_products_per_market(df)

filtered_data = filter_country_data(df)

dfPrices = pd.DataFrame(df)
total_by_seller = dfPrices.groupby("product_seller")["Price"].sum().reset_index()
total_by_marketplace = dfPrices.groupby("Marketplace")["Price"].sum().reset_index()

# Calculate number of products per country
country_counts = create_country_heatmap_data(filtered_data)

# Calculate average prices
average_prices = calculate_average_prices(df)

available_markets = products_per_market["Marketplace"].tolist()

fig_sellers = px.bar(
    total_by_seller,
    x="product_seller",
    y="Price",
    title="Total Market Values by Seller",
)
fig_marketplaces = px.bar(
    total_by_marketplace,
    x="Marketplace",
    y="Price",
    title="Total Market Values by Marketplace",
)

app = Dash(__name__)


app.layout = html.Div(
    [
        dcc.Graph(
            id="marketplace-bar-chart",
            figure={
                "data": [
                    {
                        "x": products_per_market["Marketplace"],
                        "y": products_per_market["Number of Products"],
                        "type": "bar",
                        "name": "Number of Products",
                        "hovertext": [
                            f"Avg Price: ${average_prices[average_prices['Marketplace'] == market]['Price'].values[0]:.2f}"
                            for market in products_per_market["Marketplace"]
                        ],
                    }
                ],
                "layout": {
                    "title": "Number of Products per Marketplace",
                    "xaxis": {"title": "Marketplace"},
                    "yaxis": {"title": "Number of Products"},
                },
            },
        ),
        dcc.Dropdown(
            id="marketplace-dropdown",
            options=[
                {"label": market, "value": market} for market in available_markets
            ],
            value=available_markets[0],
        ),
        dcc.Graph(id="pie-chart"),
        dcc.Graph(id="choropleth-map"),
        dcc.Graph(id="seller-price-bar-chart", figure=fig_sellers),
        dcc.Graph(id="marketplace-price-bar-chart", figure=fig_marketplaces),
        dcc.Dropdown(
            id="seller-dropdown",
            options=[
                {"label": "Cocorico", "value": "Cocorico"},
                {"label": "Revolution", "value": "Revolution"},
            ],
            value=available_markets[0],
        ),
        dcc.Graph(id="seller-bar-chart"),
    ]
)


# Define callback to update bar chart based on dropdown selection
@app.callback(
    Output("seller-bar-chart", "figure"),
    [Input("seller-dropdown", "value")],
)
def update_bar_chart(selected_market):
    # Filter data for the selected marketplace and exclude entries with seller name 'X'
    filtered_data = filter_data(df, selected_market)
    # Calculate number of products per seller for the selected marketplace
    seller_counts = calculate_products_per_seller(filtered_data)

    # Create bar chart using Plotly Express
    fig = px.bar(
        seller_counts,
        x="Seller",
        y="Number of Products",
        title=f"Number of Products per Seller in {selected_market}",
        labels={"Seller": "Seller", "Number of Products": "Number of Products"},
    )

    return fig


@app.callback(Output("pie-chart", "figure"), [Input("marketplace-dropdown", "value")])
def update_pie_chart(selected_market):
    # Filter data for the selected marketplace
    marketplace_data = [
        entry for entry in df if entry["Marketplace"] == selected_market
    ]
    # Calculate market share of drug types for the selected marketplace
    drug_type_market_share = calculate_drug_type_market_share(marketplace_data)

    # Create pie chart
    fig = {
        "data": [
            {
                "labels": drug_type_market_share["Type"],
                "values": drug_type_market_share["Market Share"],
                "type": "pie",
                "hoverinfo": "label+percent",
                "textinfo": "value",
                "textposition": "inside",
                "hole": 0.4,
            }
        ],
        "layout": {"title": f"Market Share of Drug Types in {selected_market}"},
    }
    return fig


@app.callback(
    Output("choropleth-map", "figure"), [Input("choropleth-map", "hoverData")]
)
def update_choropleth_map(hoverData):
    # Create choropleth map using Plotly Express
    fig = px.choropleth(
        country_counts,
        locations="Country",
        locationmode="country names",
        color="Number of Products",
        color_continuous_scale="Viridis",
        labels={"Number of Products": "Number of Products"},
        title="Number of Products per Country",
        hover_name="Country",
    )

    fig.update_geos(showcoastlines=True, projection_type="equirectangular")

    return fig


if __name__ == "__main__":
    app.run(debug=True)
