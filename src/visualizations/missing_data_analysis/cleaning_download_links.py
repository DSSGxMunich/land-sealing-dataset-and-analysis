import os

import pandas as pd

from data_pipeline.nrw_pdf_downloader.nrw_pdf_scraper import filtering_useful_data


def clean_processing_errors(scraped_bp_errors):
    """This function takes as input a dataframe with the links to the PDFs and downloads them to the output folder.


    Args:
        scraped_bp_errors (pd.DataFrame): DataFrame that contains the links to the PDFs, with the columns
            "scanurl" and "objectid"

    Returns:
        scraped_bp_errors (pd.DataFrame): DataFrame that contains the links to the PDFs, with the columns
            "scanurl" and "objectid" and "download_status"
        """
    # Add error value to identify them in merge with general links
    scraped_bp_errors["download_status"] = "error"

    # Removing duplicates
    scraped_bp_errors = scraped_bp_errors.drop_duplicates(["objectid", "scanurl"])

    return scraped_bp_errors


def cleaning_processing_links(bp_links):
    """ Processes and cleans the links to the PDFs.

    Args:
        bp_links (pd.DataFrame): DataFrame that contains the links to the PDFs, with the columns
            "scanurl" and "objectid"

    Returns:
        bp_links (pd.DataFrame): cleaned DataFrame that contains the links to the PDFs, with the columns
            "scanurl" and "objectid" and "download_status"
    """
    # filter links <= 2012
    bp_links = filtering_useful_data(bp_links)

    # Get useful columns, we will not need geometry cols 
    bp_links = bp_links[["objectid", "kommune", "datum", "planid", "scanurl"]]

    # Create unique ID col for BP (objectid contains BP + PDF)
    bp_links['unique_id'] = bp_links['objectid'].str.split('_').str[0]

    # Removing duplicates
    bp_links = bp_links.drop_duplicates(["objectid", "scanurl"])

    return bp_links


def get_pdfs_downloaded(pdf_folder_path):
    """This function takes as input a dataframe with the links to the PDFs and downloads them to the pdf_folder_path.

    Args:
        pdf_folder_path (str): path to the folder where the PDFs are saved

    Returns:
        files (list): list of files in the folder
    """
    # List all files in the folder of downloaded pdf
    files = [f for f in os.listdir(pdf_folder_path) if os.path.isfile(os.path.join(pdf_folder_path, f))]

    files = [f.replace('.pdf', '') for f in files]

    return files


def format_merged_errors(bp_links_with_errors, pdf_folder_path):
    """ Formats the merged links and errors dataframe.


    Args:
        bp_links_with_errors (pd.DataFrame): DataFrame that contains the links to the PDFs, with the columns
            "scanurl" and "objectid"

    Returns:
        pd.DataFrame: DataFrame that contains the links to the PDFs, with the columns
            "scanurl" and "objectid" and "download_status"

  """
    files = get_pdfs_downloaded(pdf_folder_path)

    # Set them as downloaded

    bp_links_with_errors.loc[bp_links_with_errors.objectid.isin(files), 'download_status'] = 'downloaded'

    # Replace NaN values with "downloaded" in specified columns. This is the case for links that were not readable 
    # but didn't return exception, in the function is_downloadable is NRW_BP_PDF_scraper
    bp_links_with_errors["download_status"] = bp_links_with_errors["download_status"].fillna("error")

    return bp_links_with_errors


def merge_links_and_errors(bp_links, scraped_bp_errors, pdf_folder_path):
    bp_links_with_errors = pd.merge(bp_links, scraped_bp_errors, how="left", on=['objectid', 'scanurl'])

    bp_links_with_errors = format_merged_errors(bp_links_with_errors, pdf_folder_path)

    return bp_links_with_errors


def generate_clean_links(bp_links, scraped_bp_errors, pdf_folder_path):
    processed_bp_links = cleaning_processing_links(bp_links)
    processed_error_links = clean_processing_errors(scraped_bp_errors)

    final_processed_links = merge_links_and_errors(processed_bp_links, processed_error_links, pdf_folder_path)

    return final_processed_links


def export_processed_links(pdf_folder_path="../data/nrw/bplan/raw/pdfs/",
                           links_path='../data/nrw/bplan/raw/links/NRW_BP_parsed_links.csv',
                           errors_path='../data/nrw/bplan/raw/links/error_links.csv',
                           output_path='../data/nrw/bplan/raw/links/success_links.csv'):
    bp_links = pd.read_csv(links_path)
    scraped_bp_errors = pd.read_csv(errors_path)

    final_data = generate_clean_links(bp_links, scraped_bp_errors, pdf_folder_path)

    final_data.to_csv(output_path)
