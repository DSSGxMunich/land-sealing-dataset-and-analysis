import json
import re

import numpy as np
import pandas as pd
from tqdm import tqdm


def open_keywords_json_as_dict(path_to_keywords: str) -> dict:
    """ Open, read and return the json with keywords into dict format.

    Args:
        path_to_keywords (str): path to the json file

    Returns:
        dict: dictionary with keywords
    """

    with open(path_to_keywords, 'r') as json_file:
        # Parse the JSON data into a dictionary
        keyword_dictionary = json.load(json_file)

    return keyword_dictionary


def preprocess_text(df: pd.DataFrame,
                    text_column: str) -> pd.DataFrame:
    """
    Processes text for keyword and regex identification. Converts string to lower, removes tabs.

    Args:
        df (pd.Dataframe): _dataframe with filename and text_
        text_column (str): _name of the column with the text_

    Returns:
        pd.Dataframe: _dataframe with filename and text_
    """

    df[text_column] = df[text_column].str.replace('\n', ' ')
    df[text_column] = df[text_column].str.replace('\t', ' ')

    df[text_column] = df[text_column].str.lower()

    return df


def _search_text_for_bp_pattern(text: str) -> str:
    """
    Function that takes as input a string and searches for the pattern bebauungsplan nr. and digits,
    returns if there is a match found or not.

    Args:
        text (str): _text to search for pattern_
    Returns:
        _string_: _value is a BP/other_
    """

    words = text.lower()

    pattern = r'bebauungsplan\s*nr\.\s*\d+'

    match = re.search(pattern, words)

    if match:
        result = 'BP'
    else:
        result = 'Other'

    return result


def detect_bp_pattern(df: pd.DataFrame,
                      text_column: str,
                      id_column: str) -> pd.DataFrame:
    """
    
    Function that takes as input a dataframe with processed text and searches or the keywords defined in the dictionary,
    for the BP pattern and returns the type of document and if the keywords were found.

    Args:
        df (pd.Dataframe): dataframe with filename and text
        text_column (str): name of the column with the text
        id_column (str): name of the column with the unique file identifier

    Returns:
        pd.DataFrame: dataframe with columns filename, document_category and the keywords that were searched for.
    """

    results = []

    for index, row in tqdm(df.iterrows()):

        object_id = row[id_column]
        content = row[text_column]

        if isinstance(content, (float, np.floating)):
            doc_match = {'document_category': 'Unreadable', 'filename': object_id}
        else:
            doc_match = {'document_category': _search_text_for_bp_pattern(content), 'filename': object_id}

        results.append(doc_match)

    to_data = pd.DataFrame(results)

    return to_data


def _extract_category_bp(path: str) -> 'pd.DataFrame':
    """Extract the category from the original dataset."""
    df = pd.read_csv(path, dtype='unicode')
    df = df[['objectid', 'planart', 'verfahren']]
    df['filename'] = df['objectid'] + '.pdf'

    return df


def _encode_legal_procedure(df: pd.DataFrame):
    """Encode the legal_procedure.
    """
    code_to_encoding = {1000: 'Normal',
                        2000: 'Parag13',
                        3000: 'Parag13a',
                        4000: 'Parag13b'}

    df['legal_procedure_code__parcel'] = pd.to_numeric(df['legal_procedure_code__parcel'], errors='coerce')
    df['legal_procedure__parcel'] = df['legal_procedure_code__parcel'].map(code_to_encoding)

    return df


def encode_plan_type(df: pd.DataFrame):
    """Encode the plan_type.
    """
    code_to_encoding = {9999.0: 'Plan ohne Angabe der Planart',

                        1000: 'BPlan',
                        10000: 'Einfacher BPlan',
                        10001: 'Qualifizierter BPlan',
                        10002: 'Sektoraler BPlan',
                        1100: 'Veränderungssperre',
                        1200: 'Fluchtlinienplan',

                        3000: 'Vorhabenbezogener BPlan',
                        3100: 'Vorhaben- und Erschließungsplan',

                        4000: 'Innenbereichssatzung ',
                        40000: 'KlarstellungsSatzung ',
                        40001: 'EntwicklungsSatzung  ',
                        40002: 'ErgaenzungsSatzung ',

                        5000: 'Außenbereichssatzung',

                        7000: 'Örtliche Bauvorschrift',

                        8000: 'Stb. Entwicklungsmaßnahme (-satzung)',

                        8500: 'Flächennutzungsplan',

                        9000: 'Gestaltungssatzung',

                        8888: 'Sonstiges'}

    df['plan_type_code__parcel'] = pd.to_numeric(df['plan_type_code__parcel'], errors='coerce')
    df['plan_type__parcel'] = df['plan_type_code__parcel'].map(code_to_encoding)

    return df


def run_bp_keyword_detector(text_file_path: str,
                            original_files_path: str,
                            text_column: str = 'content',
                            id_column: str = 'filename',
                            sample_n: int = None) -> 'pd.DataFrame':
    """Run the BP and keyword detector.

    Checks if the text contains the BP pattern and if the keywords are found. Also adds the categorization from the
    original dataframe.

    Args:
        text_file_path (str): path to the text file
        original_files_path (str): path to the original files
        text_column (str): name of the column with the text
        id_column (str): name of the column with the unique file identifier
        sample_n (int): number of rows to sample

    Returns:
        pd.DataFrame: dataframe with columns filename, document_category and the unique document id.
    """
    # Reading file
    text_df = pd.read_csv(text_file_path, names=[id_column, text_column])

    # Running prepro of text column
    text_df = preprocess_text(text_df, text_column)

    if sample_n:
        text_df = text_df.sample(n=sample_n, random_state=912)

    # NRW geoportal dataset
    original_df = _extract_category_bp(original_files_path)

    # Running BP and keyword detection
    df_document_and_keywords = detect_bp_pattern(text_df, text_column, id_column)

    # Add categorization from the original dataset
    df_document_and_keywords = df_document_and_keywords.merge(original_df)

    df_document_and_keywords = df_document_and_keywords.rename(columns={'objectid': 'document_id',
                                                                        'planart': 'plan_type_code__parcel',
                                                                        'verfahren': 'legal_procedure_code__parcel'})

    # classify plan_type and legal_procedure
    df_document_and_keywords = encode_plan_type(df_document_and_keywords)
    df_document_and_keywords = _encode_legal_procedure(df_document_and_keywords)

    # reorder columns
    desired_order = ['filename', 'document_id', 'document_category', 'plan_type_code__parcel', 'plan_type__parcel',
                     'legal_procedure_code__parcel']
    df_document_and_keywords = df_document_and_keywords[
        desired_order + [col for col in df_document_and_keywords.columns if col not in desired_order]]

    df_document_and_keywords = df_document_and_keywords.drop_duplicates()

    return df_document_and_keywords
