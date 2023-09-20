import re

import geopandas as gpd
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def _matches_url_pattern(input_string: str):
    """ Check if input string matches url pattern."""
    pattern = r'^(https:\/\/www\.o-sp\.de\/.*\/plan\b|https:\/\/gisdata\.krzn\.de\/.*)'

    return re.match(pattern, input_string)


def parse_non_downloadable_links(gdf: "pd.DataFrame") -> "pd.DataFrame":
    """ Parse non-downloadable links from gdf.

    This function parses the links from the scanurl column of the gdf. It iterates over all rows and checks if the url
    matches the pattern of a osp-plan.de link without a list format, meaning than the scan url is not directly to a pdf,
    but the pdf is contained somewhere in the html of the page. 
    
    
    If the url matches the pattern, the html of the page is
    downloaded and parsed with beautiful soup. All links that start with 
    https://www.o-sp.de/download/ are extracted
    and written to a dataframe.

    Args:
        gdf: (geo)dataframe with scanurl column and objectid column

    Returns:
        pd.DataFrame: dataframe with all links that start with https://www.o-sp.de/download/ or https://gisdata.krzn.de/
    """

    # convert objectid to string
    gdf["objectid"] = gdf["objectid"].astype(str)

    for df_index, row in tqdm(gdf.iterrows(), total=len(gdf)):
        # get content for url
        url = row["scanurl"]
        if not _matches_url_pattern(url):
            continue
        links = _get_links(url)

        # iterate over all links
        for index, link in enumerate(links):
            gdf = _parse_link(gdf, index, link, row)

        # remove the old row
        gdf = gdf.drop(index=df_index)

    # sort by objectid
    gdf = gdf.sort_values(by=["objectid"])
    return gdf


def _get_links(url):
    """ Get all links from url that start with https://www.o-sp.de/ or  https://gisdata.krzn.de/files/bplan"""
    r = requests.get(url, allow_redirects=True)
    # get content
    content = r.content
    # open in beautiful soup
    soup = BeautifulSoup(content, 'html.parser')

    links = []  # Default value is an empty list

    if "https://www.o-sp.de/" in url:
        # get all links that start with https://www.o-sp.de/download/
        links = soup.find_all('a', href=lambda value: value and
                                                      (value.startswith(
                                                          "https://www.o-sp.de/download/") or value.startswith(
                                                          "/download/")))
    elif "https://gisdata.krzn.de/" in url:
        # get all links that start with https://www.o-sp.de/download/
        links = soup.find_all('a', href=lambda value: value and
                                                      (value.startswith(
                                                          "https://gisdata.krzn.de/files/bplan")))

    return links


def _parse_link(gdf, index, link, row):
    """ Parse link and add the new url's to gdf """
    # get href
    href = link.get('href')
    # if internal link
    if href.startswith("/download/"):
        # get full url
        href = "https://www.o-sp.de" + href

    # create a new row with the information of the old row
    new_row = row.copy()

    # add the link to the new row
    new_row["scanurl"] = href

    # add the index to the objectid
    new_row["objectid"] = f"{row['objectid']}_{index}"

    # concat the new row to the matches using concatenate
    gdf = pd.concat([gdf, new_row.to_frame().T], ignore_index=True)

    return gdf


def parse_geojson(file_path,
                  output_path,
                  sample_n=None) -> 'pd.DataFrame':
    """ Parse geojson file from file_path and write it to output_path.

    This function parses the geojson file from file_path and writes it to output_path.
    If sample_n is not None, the geojson is sampled to sample_n rows.
    The function parse_non_downloadable_links is called to parse the links from the scanurl column.
    It adds all sub-links that where listed in the original dataframe and start with https://www.o-sp.de/download/
    or https://gisdata.krzn.de/files/bplan to the dataframe. The objectid is extended with the index of the link.

    Args:
        file_path: path to geojson file
        output_path: path to output file
        sample_n: number of rows to sample

    Returns:
        pd.DataFrame: dataframe with all links and sub-links
    """
    if file_path.endswith(".geojson"):
        gdf = gpd.read_file(file_path)
    elif file_path.endswith(".csv"):
        gdf = pd.read_csv(file_path)
    else:
        raise ValueError("File format not supported. Please use geojson or csv.")

    if sample_n is not None:
        gdf = gdf.sample(sample_n, random_state=912)
        gdf = gdf.reset_index()

    df = parse_non_downloadable_links(gdf)

    df.to_csv(output_path)

    return df
