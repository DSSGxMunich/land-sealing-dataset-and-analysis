import pandas as pd
import geopandas as gpd
import os

from datetime import datetime
from NRW_PDF_downloader import NRW_BP_PDF_scraper

def clean_processing_errors(scraped_BP_errors):

    # Add error value to identify them in merge with general links
    scraped_BP_errors["download_status"] = "error"

    #Removing duplicates
    scraped_BP_errors = scraped_BP_errors.drop_duplicates(["objectid", "scanurl"])

    return(scraped_BP_errors)

def cleaning_processing_links(BP_links):

    # filter links <= 2012
    BP_links = NRW_BP_PDF_scraper.filtering_useful_data(BP_links)

    # Get useful columns, we will not need geometry cols 
    BP_links = BP_links[["objectid", "kommune", "datum", "planid", "scanurl"]]

    # Create unique ID col for BP (objectid contains BP + PDF)
    BP_links['unique_id'] = BP_links['objectid'].str.split('_').str[0]

    # Removing duplicates
    BP_links = BP_links.drop_duplicates(["objectid", "scanurl"])

    return(BP_links)

def get_pdfs_downloaded(pdf_folder_path = '../data/NRW/pdfs'):

    folder_path = pdf_folder_path

    # List all files in the folder of downloaded pdf
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    files = [f.replace('.pdf','') for f in files]

    return(files)

def format_merged_errors(BP_links_with_errors):

    files = get_pdfs_downloaded()

    #Set them as downloaded

    BP_links_with_errors.loc[BP_links_with_errors.objectid.isin(files), 'download_status'] = 'downloaded'

    # Replace NaN values with "downloaded" in specified columns. This is the case for links that were not readable 
    # but didn't return exception, in the function is_downloadable is NRW_BP_PDF_scraper
    BP_links_with_errors["download_status"] = BP_links_with_errors["download_status"].fillna("error")

    return(BP_links_with_errors)


def merge_links_and_errors(BP_links, scraped_BP_errors):

    BP_links_with_errors = pd.merge(BP_links, scraped_BP_errors, how = "left", on = ['objectid','scanurl'])

    BP_links_with_errors = format_merged_errors(BP_links_with_errors)

    return(BP_links_with_errors)


def generate_clean_links(BP_links, scraped_BP_errors): 

    processed_BP_links = cleaning_processing_links(BP_links)
    processed_error_links = clean_processing_errors(scraped_BP_errors)

    final_processed_links = merge_links_and_errors(processed_BP_links, processed_error_links)

    return(final_processed_links)

    
def export_processed_links(links_path = "../data/NRW_bebauungsplane_with_download_links.geojson", errors_path = "../data/NRW/PDFS/error_links.csv"):
    
    # Read files 
    BP_links = pd.read_csv(links_path)
    scraped_BP_errors = pd.read_csv(errors_path)

    final_data = generate_clean_links(BP_links, scraped_BP_errors)

    final_data.to_csv("../data/NRW/clean_downloaded_links.csv")