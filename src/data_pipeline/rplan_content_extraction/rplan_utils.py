import os
import re

import pandas as pd
import geopandas as gpd

from data_pipeline.pdf_scraper.tika_pdf_scraper import pdf_parser_from_folder

RAW_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..", "..", "data", "nrw"))
RPLAN_PDF_DIR = os.path.abspath(os.path.join(RAW_DATA_DIR, "rplan_pdfs"))
RPLAN_TXT_DIR = os.path.abspath(os.path.join(RAW_DATA_DIR, "rplan_text"))

PARSED_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "nrw", ))
RPLAN_OUTPUT_PATH = os.path.abspath(os.path.join(PARSED_DATA_DIR, "extracted_rplan_content.json"))

CONFIG_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "rplan_structure.yml"))

REGIONS_MAPPING_PLAN = os.path.abspath(
    os.path.join(os.path.dirname(__file__),  "..", "..", "..", "data", "nrw", "regions_map.geojson"))

RPLAN_MATCH_DICT = {'Düsseldorf': 'duesseldorf-2018.pdf',
                    'Region Köln': 'köln-2006.pdf',
                    'Region Bonn/Rhein-Sieg': 'bonn-2009.pdf',
                    'Region Aachen': 'aachen-2016.pdf',
                    'Münsterland': 'muenster-2014.pdf',
                    'Oberbereich Paderborn': 'detmold-2007-paderborn_hoexter.pdf',
                    'Oberbereich Bielefeld': 'bielefeld-_.pdf',
                    'Kreis Soest und Hochsauerlandkreis': 'arnsberg-2012-kreis_soest_hochsauerlandkreis.pdf',
                    'Oberbereich Siegen': '',
                    'Oberbereiche Bochum/Hagen': 'arnsberg-2001-bochum_hagen.pdf',
                    'Märkischer Kreise&Kreise Olpe/Siegen-Wittgenstein': 'arnsberg-2008-siegen.pdf',
                    'Regionalverband Ruhr': 'ruhr-2021.pdf'}


def extract_text_and_save_to_txt_files(pdf_dir_path: str):
    """
    Extracts text from pdf files in input_path and saves it to output_path.
    """
    parsed_df = pdf_parser_from_folder(folder_path=pdf_dir_path)
    write_df_to_text(parsed_df)
    return parsed_df


def write_df_to_text(df, txt_dir_path=RPLAN_TXT_DIR):
    """
    Writes content from df to txt files.
    """
    for filename, content in zip(df['filename'], df['content']):
        # save content as txt file
        with open(os.path.join(txt_dir_path, filename.replace('.pdf', '.txt')), 'w+') as f:
            f.write(content)


def find_rplan_keyword_index(text, keywords, start=0, return_all=False):
    """
    Finds keywords in text and returns the index.
    """
    assert len(text) > start, "Start index is larger than text length"
    # escape all words
    words = [re.escape(word) for word in keywords.split()]
    # add regex for newline and space, such that the words can be found even if they are split by a newline
    # or a space
    words_with_split_regex = [i + j for i, j in zip(words, ['[\n ]'] * len(words))]
    # create pattern
    pattern = r''.join([word for word in words_with_split_regex])
    # find all matches
    split_text = text[start:]
    matches = list(re.finditer(pattern, split_text))
    if return_all:
        return [match.start() for match in matches]
    return matches[0].start() if matches else None

def _match_regions_to_pdf_files(df):
    regions_map_df_full = gpd.read_file(REGIONS_MAPPING_PLAN)
    # filter all rows with PLR between 5000 and 6000
    regions_map_df = regions_map_df_full[
        (regions_map_df_full['PLR'] >= 5000) & (regions_map_df_full['PLR'] <= 6000)]  # NRW only
    regions_map_df = regions_map_df.drop(columns=['geometry', 'ART', 'LND'])
    regions_map_df['filename'] = regions_map_df['Name'].map(RPLAN_MATCH_DICT)
    # remove .pdf from filename
    regions_map_df['filename'] = regions_map_df['filename'].apply(lambda x: x.replace('.pdf', ''))
    # join on filename
    df = df.merge(regions_map_df, on='filename', how='left')
    # PLR to int
    df['PLR'] = df['PLR'].astype('Int64')
    return df


def parse_result_df(df):
    """ Parses the result df from the rplan extractor.

    Args:
        df: pd.DataFrame with columns ['filename',...]

    Returns:
        pd.DataFrame with columns ['filename', ..., 'year']

    """

    # extract year from file name
    df['year'] = df['filename'].apply(lambda x: int(x.split('-')[1]) if x.split('-')[1].isnumeric() else pd.NA)
    df = _match_regions_to_pdf_files(df)
    return df
