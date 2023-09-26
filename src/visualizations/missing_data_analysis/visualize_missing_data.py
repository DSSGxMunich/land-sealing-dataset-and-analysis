import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def parse_date(date_string):
    """
    Parses date string into datetime format. If not possible, returns NaN.
    """
    if isinstance(date_string, str):
        try:
            return pd.to_datetime(date_string, format='%Y-%m-%dT%H:%M:%S')

        except ValueError:
            return np.nan


def filtering_useful_data(data: gpd.GeoDataFrame):
    """
    Takes as input NRW geo dataframe, parses the dates, filters BP from 2012 and onwards and keeps only PDF files.
    """

    # Parse date column into date format
    data["datum"] = data["datum"].apply(parse_date)

    # Define the start date for filtering
    start_date = pd.to_datetime('1900-12-31')

    # Filter rows which the date is 2012 and onwards
    filtered_data = data[data["datum"] > start_date]

    return filtered_data


def prepro_original_bp(bp_geo_path):
    bp_geo = gpd.read_file(bp_geo_path)

    bp_geo = filtering_useful_data(bp_geo)

    return bp_geo


def histogram_bp_date(bp_geo_path: str,
                      date_col: str,
                      output_plot_path: str = None):
    bp_geo = prepro_original_bp(bp_geo_path=bp_geo_path)

    sns.set(style="whitegrid")  # Optional: Set a white grid background

    plt.figure(figsize=(12, 5))  # Adjust the figure size to control width and height

    # Create the bar plot using Seaborn
    fig2 = sns.histplot(x=date_col, data=bp_geo, stat='count')

    plt.title('Bebauungspläne')
    plt.xlabel('Year')
    plt.ylabel('Count')

    # Save plot if wanted
    if output_plot_path:
        plt.savefig(output_plot_path)

    # Show the plot
    plt.show()


def get_unique_bp_downloads(data_path: str,
                            normalized: bool = True):
    df = pd.read_csv(data_path)

    # get unique BP downloads
    subset = df[['unique_id', 'scanurl', 'datum', 'download_status']]
    subset = subset.drop_duplicates(subset='unique_id', keep='last')

    # get count of downloaded BP
    counts = subset['download_status'].value_counts(normalize=normalized)

    return subset, counts


def get_count_bp_downloaded_year(data: pd.DataFrame):
    data['year'] = data['datum'].str[:4]

    data['year'] = data['year'].astype("Int64")
    data = data[(data['year'] > 1900) & (data['year'] < 2023)]

    year_errors_count = data.groupby(["year", "download_status"]).size().reset_index(name='count')

    return year_errors_count


def plot_bp_downloads(data: pd.DataFrame,
                      output_plot_path: str = None):
    # Set the style for Seaborn (optional but can improve the aesthetics)
    sns.set(style="whitegrid")  # Optional: Set a white grid background

    fig2 = sns.countplot(x='download_status', data=data)

    fig2.set(xlabel="Download status", ylabel="Count")

    # Save plot if wanted
    if output_plot_path:
        plt.savefig(output_plot_path)

    # Show the plot
    plt.show()


def plot_bp_downloads_year(data: pd.DataFrame,
                           output_plot_path: str = None):
    data = get_count_bp_downloaded_year(data=data)

    # Set the style for Seaborn (optional but can improve the aesthetics)
    sns.set(style="whitegrid")  # Optional: Set a white grid background

    plt.figure(figsize=(12, 5))  # Adjust the figure size to control width and height

    # Create the bar plot using Seaborn
    sns.barplot(data=data, x="year", y="count", hue='download_status')

    plt.title('Downloaded PDFs')
    plt.xlabel('Year')
    plt.ylabel('Count')

    # Save plot if wanted
    if output_plot_path:
        plt.savefig(output_plot_path)

     # Show the plot
    plt.show()


