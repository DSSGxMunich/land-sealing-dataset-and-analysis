import os.path

import yaml
from utility.config_utils import read_yaml
from nrw_pdf_downloader.geojson_parser import parse_geojson
from nrw_pdf_downloader.nrw_pdf_scraper import run_pdf_downloader

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config", "geojson_config.yml")


def download_pdfs(sample_n: int = None):
    # read config yaml
    config = read_yaml(CONFIG_PATH)

    input_geojson_path = config["input_geojson_path"]

    # use geojson_parser to parse the geojson
    gdf = parse_geojson(input_geojson_path, sample_n)

    # use NRW_BP to download the links
    run_pdf_downloader(gdf, config["pdf_output_folder"])


if __name__ == '__main__':
    download_pdfs()
