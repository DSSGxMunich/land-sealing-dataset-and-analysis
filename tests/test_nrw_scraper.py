import os
import tempfile

from data_pipeline.nrw_pdf_downloader.geojson_parser import parse_geojson
from data_pipeline.nrw_pdf_downloader.nrw_pdf_scraper import run_pdf_downloader

SAMPLE_TEST_DF = os.path.join(os.path.dirname(__file__), "test_data", "test_15__rows.geojson")


def test_parser():
    sample_size = 10

    # create temp folder to store the pdfs
    with tempfile.TemporaryDirectory() as folder_output_path:
        gdf = parse_geojson(SAMPLE_TEST_DF, sample_n=sample_size, output_path=folder_output_path + "/tmp.csv")

        # use NRW_BP to download the links
        run_pdf_downloader(gdf, folder_output_path)

        # Check if the folder exists
        assert os.path.exists(folder_output_path), f"Folder '{folder_output_path}' does not exist"

        # Check if the folder contains any files or subdirectories
        assert os.listdir(folder_output_path), f"Folder '{folder_output_path}' is empty"
