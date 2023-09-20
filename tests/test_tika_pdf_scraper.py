import os

import pandas as pd
import pytest

from data_pipeline.pdf_scraper.tika_pdf_scraper import pdf_parser_from_folder
from data_pipeline.pdf_scraper.tika_pdf_scraper import pdf_parser_from_path

# specify paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_PATH_TO_SUCCESS = os.path.join(BASE_DIR, "test_data", "test_pdfs", "success")
FILE_PATH_TO_SUCCESS = os.path.join(FOLDER_PATH_TO_SUCCESS, "90860_01.pdf")


def test_error_pdf_parser_from_folder():
    """Test whether ValueError is triggered if sample_size > folder contents.
    """
    # apply function
    with pytest.raises(ValueError):
        pdf_parser_from_folder(folder_path=FOLDER_PATH_TO_SUCCESS,
                               sample_size=3)


def test_success_pdf_parser_from_folder():
    """Test whether pdfs from the folder can be successfully parsed in terms of data types.
    """
    # apply function
    result_df = pdf_parser_from_folder(folder_path=FOLDER_PATH_TO_SUCCESS,
                                       sample_size=2)

    # assert datatypes
    assert isinstance(result_df, pd.DataFrame)
    assert all(result_df[col].dtype == expected_dtype
               for col, expected_dtype in [('filename', object),
                                           ('content', object),
                                           ('metadata', dict)])
    ## Asserts that not entries in the metadata column is None
    assert True not in result_df['metadata'].isnull().tolist()


def test_pdf_parser_from_path():
    """Test whether pdfs from the file path can be successfully parsed in terms of data types.
    """
    # apply function
    result_dict = pdf_parser_from_path(FILE_PATH_TO_SUCCESS)

    # assert datatypes
    assert isinstance(result_dict, dict)
