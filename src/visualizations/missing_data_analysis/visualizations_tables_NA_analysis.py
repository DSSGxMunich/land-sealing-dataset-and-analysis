import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def parse_date(date_string):
    if isinstance(date_string, str):
        try:
            return pd.to_datetime(date_string, format='%Y-%m-%dT%H:%M:%S')
            # return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return np.nan


def filtering_useful_data(data: gpd.GeoDataFrame):
    """
    Takes as input NRW geodataframe, parses the dates, filters BP from 2012 and onwards and keeps only PDF files. 
    """

    # Parse date column into date format
    data["datum"] = data["datum"].apply(parse_date)

    # Define the start date for filtering
    start_date = pd.to_datetime('1900-12-31')

    # Filter rows which the date is 2012 and onwards
    filtered_data = data[data["datum"] > start_date]

    return (filtered_data)


def prepro_original_BP(BP_geo_path="../data/NRW/NRW_BP.geojson"):
    BP_geo = gpd.read_file(BP_geo_path)

    # BP_geo['datum'] = BP_geo["datum"].apply(parse_date)

    BP_geo = filtering_useful_data(BP_geo)

    return (BP_geo)


def get_unique_BP(BP_df, column_name='objectid'):
    unique_bp = BP_df[column_name].nunique()

    print("Unique BP by objectid in the NRW dataframe:", unique_bp)


def histogram_BP_date(BP_geo_path="../data/NRW/NRW_BP.geojson", date_col='datum'):
    BP_geo = prepro_original_BP()

    sns.set(style="whitegrid")  # Optional: Set a white grid background

    plt.figure(figsize=(12, 5))  # Adjust the figure size to control width and height

    # Create the bar plot using Seaborn
    fig2 = sns.histplot(x=date_col, data=BP_geo, stat='count')

    plt.title('NRW Bebauungspläne')
    plt.xlabel('Year')
    plt.ylabel('Count')

    # Show the plot
    plt.show()
    plt.savefig('../plots/01_total_BP_years.png')


def get_unique_BP_downloads(data_path="../data/NRW/clean_downloaded_links.csv"):
    df = pd.read_csv(data_path)

    subset = df[['unique_id', 'scanurl', 'datum', 'download_status']]

    subset = subset.drop_duplicates(subset='unique_id', keep='last')

    return (subset)


def get_count_BP_downloaded(normalized=True):
    data = get_unique_BP_downloads()

    print(data['download_status'].value_counts(normalize=normalized))


def get_count_BP_downloaded_year():
    df = get_unique_BP_downloads()

    df['year'] = df['datum'].str[:4]

    df['year'] = df['year'].astype("Int64")

    df = df[(df['year'] > 1900) & (df['year'] < 2023)]

    year_errors_count = df.groupby(["year", "download_status"]).size().reset_index(name='count')

    # Calculate the total count for each 'kommune'
    years_total = year_errors_count.groupby('year')['count'].transform('sum')

    return (year_errors_count)


def plot_BP_downloads():
    data = get_unique_BP_downloads()

    # Set the style for Seaborn (optional but can improve the aesthetics)
    sns.set(style="whitegrid")  # Optional: Set a white grid background

    fig2 = sns.countplot(x='download_status', data=data)

    fig2.set(xlabel="Download status", ylabel="Count")
    plt.savefig('../plots/02_total_downloads.png')


def plot_BP_downloads_year():
    data = get_count_BP_downloaded_year()

    # Set the style for Seaborn (optional but can improve the aesthetics)
    sns.set(style="whitegrid")  # Optional: Set a white grid background

    plt.figure(figsize=(12, 5))  # Adjust the figure size to control width and height

    # Create the bar plot using Seaborn
    fig3 = sns.barplot(data=data, x="year", y="count", hue='download_status')

    plt.title('Downloaded Bebauungspläne PDFs')
    plt.xlabel('Year')
    plt.ylabel('Count')

    # Show the plot
    plt.show()
    plt.savefig('../plots/03_downloads_per_year.png')
