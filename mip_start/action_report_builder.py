import os

import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure

from mip_start.constants import APP_OUTPUT_DIR


def _save_html_plot(fig: Figure, plot_name: str, path: str = APP_OUTPUT_DIR):
    """Save plots, as HTML, to the default directory of Mip Hub.

    When executed locally, saves the HTML file to app/output/ (default directory of Mip Hub), or to the specified path.

    Parameters
    ----------
    fig: Figure
        A figure generated with plotly, using plotly.express or plotly.graph_objects, for instance.
    plot_name: str
        Name of the plot to be saved as an HTML file and to be displayed on Mip Hub.
    path: str
        Path to the output.
    """
    # Save the file: get path first, create directory if doesn't exist and save html file
    file_path = os.path.join(f'{path}/{plot_name}.html')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    fig.write_html(file_path)


def report_builder_solve(dat, sln, path: str = APP_OUTPUT_DIR):
    buy = sln.buy.copy()
    foods_nutrients = dat.foods_nutrients.copy()
    nutrients = dat.nutrients.copy()

    # Rename columns for clarity
    buy.rename(columns={'Quantity': 'Purchase Quantity'}, inplace=True)
    foods_nutrients.rename(columns={'Quantity': 'Nutrient per unit'}, inplace=True)

    # Merge the 'buy' table with 'foods_nutrients' on Food ID
    merged = buy.merge(foods_nutrients, on='Food ID', how='left')

    # Compute contribution: (quantity purchased) * (nutrient per unit)
    merged['Contribution'] = merged['Purchase Quantity'] * merged['Nutrient per unit']

    # Merge with the nutrients table to get nutrient names
    merged = merged.merge(nutrients[['Nutrient ID', 'Nutrient Name']], on='Nutrient ID', how='left')

    # Create a stacked bar chart using Plotly Express
    fig_stacked = px.bar(
        merged,
        x="Food Name",
        y="Contribution",
        color="Nutrient Name",
        title="Stacked Bar Chart of Food-Nutrient Contributions",
        labels={"Contribution": "Nutrient Contribution"}
    )

    _save_html_plot(fig_stacked, 'stacked_bar', path)

    return sln
