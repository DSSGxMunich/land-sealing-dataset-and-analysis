import os

import pandas as pd

from features.document_categorization.detecting_BP_and_keywords import run_bp_keyword_detector

# specify file path
INPUT_FOLDER_PATH = os.path.join("data", "nrw", "text", "nrw_final_all.csv")
INPUT_ORIGINAL_DF_PATH = os.path.join("data", "nrw", 'NRW_BP_with_links.geojson')

# specify relevant column names
ID_COLUMN = 'filename'
TEXT_COLUMN = 'content'

# specify keyword path
INPUT_KEYWORD_PATH = os.path.join("src", "features", "document_categorization", "relevant_document_keywords.json")


def test_keyword_identification():
    documents_categorized = run_bp_keyword_detector(INPUT_FOLDER_PATH, INPUT_ORIGINAL_DF_PATH, TEXT_COLUMN, ID_COLUMN,
                                                    sample_n=10)

    # assert datatypes
    assert isinstance(documents_categorized, pd.DataFrame)

    assert all(documents_categorized[col].dtype == expected_dtype
               for col, expected_dtype in [('filename', object),
                                           ('document_category', object)])

    # Check that all documents are categorized into BP/not BP
    assert not documents_categorized['document_category'].isna().any()
