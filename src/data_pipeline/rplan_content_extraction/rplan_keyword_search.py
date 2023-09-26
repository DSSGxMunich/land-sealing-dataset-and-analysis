import json
import os.path

import pandas as pd
from loguru import logger

from features.textual_features.keyword_search.contextual_fuzzy_search import \
    search_df_for_best_matches_keyword_dict
from features.textual_features.keyword_search.exact_keyword_search import search_df_for_keywords
from utility.config_utils import get_data_path, get_source_path
from visualizations.rplan_visualization import plot_keyword_search_results

rplan_content_path = os.path.join(get_data_path(), "nrw", "extracted_rplan_content.json")

keyword_path = get_source_path() + "/data_pipeline/rplan_content_extraction/keywords"
rplan_exact_keyword_dict_path = os.path.join(keyword_path, "exact_keyword_dict_rplans.json")
rplan_fuzzy_keyword_dict_path = os.path.join(keyword_path, "fuzzy_keyword_dict_rplans.json")
rplan_negate_keyword_dict_path = os.path.join(keyword_path, "negate_keyword_dict_rplans.json")


def rplan_exact_keyword_search(input_df: 'pd.DataFrame', save_path: str = None, drop_false_rows=False):
    """ Function to search for keywords in a df.

    This function uses excat matching to find the best matches for the keywords. It uses the extracted content from
    the rplan pdfs as input. The keywords are stored in a json file. It basically uses the search_df_for_keywords
    function from the contextual_exact_search module.


    Args:
        input_df: Input df to be searched for keywords
        save_path: defaults to None; if None, the result is not saved
        drop_false_rows: defaults to False; if True, rows with all False values are dropped

    Returns:
        pd.DataFrame: Result df of the keyword search
    """
    index_column_name, input_df, rplan_keywords, text_column_name = _prepare_rplan_df(input_df,
                                                                                      rplan_exact_keyword_dict_path)

    result_df = search_df_for_keywords(input_df,
                                       id_column_name=index_column_name,
                                       text_column_name=text_column_name,
                                       keyword_dict=rplan_keywords,
                                       boolean=True
                                       )

    result_df = save_rplan_keyword_search(input_df, result_df, drop_false_rows=drop_false_rows,
                                          saving_filename=save_path)
    return result_df, rplan_keywords.keys()


def rplan_fuzzy_keyword_search(input_df: 'pd.DataFrame', save_path: str = None, drop_false_rows=False):
    """ Function to search for keywords in a df.

    This function uses fuzzy matching to find the best matches for the keywords. It uses the extracted content from
    the rplan pdfs as input. The keywords are stored in a json file. It basically uses the search_df_for_best_matches_keyword_dict
    function from the contextual_fuzzy_search module.

    Args:
        input_df: Input df to be searched for keywords
        save_path: defaults to None; if None, the result is not saved
        drop_false_rows: defaults to False; if True, rows with all False values are dropped

    Returns:
        pd.DataFrame: Result df of the keyword search
        rplan_keywords.keys(): List of keywords used for the search
    """
    index_column_name, input_df, rplan_keywords, text_column_name = _prepare_rplan_df(input_df,
                                                                                      rplan_fuzzy_keyword_dict_path)

    result_df = search_df_for_best_matches_keyword_dict(input_df=input_df,
                                                        id_column_name=index_column_name,
                                                        text_column_name=text_column_name,
                                                        keyword_dict=rplan_keywords,
                                                        default_threshold=70,
                                                        context_words=3)

    result_df = save_rplan_keyword_search(input_df, result_df,
                                          drop_false_rows=drop_false_rows,
                                          saving_filename=save_path)
    return result_df, rplan_keywords.keys()


def _prepare_rplan_df(input_df: 'pd.DataFrame',
                      keyword_dict_path):
    """ Function to prepare the input df for the keyword search.

    Args:
        input_df: Input df to be searched for keywords
        keyword_dict_path: Path to the keyword dict

    Returns:
        index_column_name: Name of the index column
        input_df: Input df to be searched for keywords
        rplan_keywords: Dict of relevant keywords
        text_column_name: Name of the column in the input df holding the relevant text

    """
    input_df = input_df.reset_index()  # add index column
    index_column_name = "index"
    text_column_name = "section"
    with open(keyword_dict_path) as f:
        rplan_keywords = json.load(f)
    return index_column_name, input_df, rplan_keywords, text_column_name


def save_rplan_keyword_search(input_df,
                              result_df,
                              drop_false_rows=False,
                              saving_filename: str = None):
    """ Function to save the result of the keyword search to a json file.


    Args:
        input_df: Input df to be searched for keywords
        result_df: Result df of the keyword search
        drop_false_rows: defaults to False; if True, rows with all False values are dropped
        saving_filename: defaults to "rplan_exact_keyword_search_result.json"; filename of the saved result

    Returns:
        pd.DataFrame: Result df of the keyword search with additional columns from the input df

    """
    if drop_false_rows:
        result_df = result_df[result_df.drop(columns=["index"]).any(axis=1)].copy()
    result_df["index"] = result_df["index"].astype('int64')
    # for every entry get the section and chapter from the input df and append to result df
    result_df = input_df.merge(result_df, on="index")
    if saving_filename and saving_filename.endswith(".json"):
        result_df.to_json(saving_filename)

    return result_df


def negate_keyword_search(input_df: 'pd.DataFrame',
                          negate_keyword_dict_path: str,
                          keyword_column: str = 'section'):
    """ Function to negate the result of the keyword search.

    This function removes rows from the input df if the negate keywords are found in the text. It is a simple
    exact matching search.

    Args:
        input_df: Input df to be searched for keywords
        keyword_column: Name of the column in the input df holding the relevant text
        negate_keyword_dict_path: Path to the negate keyword dict

    Returns:
        pd.DataFrame: Result df of the keyword search with additional columns from the input df

    """
    with open(negate_keyword_dict_path) as f:
        negate_keywords = json.load(f)
    logger.info(f"Negate keywords: {negate_keywords}")
    tmp_len = len(input_df)
    for negate_keyword in negate_keywords:
        for index, row in input_df[[keyword_column]].iterrows():
            text = row["section"]
            if negate_keyword in text:
                # remove row
                input_df = input_df.drop(index)
    logger.info(f"Removed {tmp_len - len(input_df)} rows with negate keywords")
    return input_df


if __name__ == '__main__':
    input_df = pd.read_json(rplan_content_path)
    input_df = negate_keyword_search(input_df, negate_keyword_dict_path=rplan_negate_keyword_dict_path)

    exact_result, exact_keywords = rplan_exact_keyword_search(input_df)
    plot_keyword_search_results(exact_result, keyword_columns=exact_keywords, title="Exact Keyword Search Results")

    fuzzy_result, fuzzy_keywords = rplan_fuzzy_keyword_search(input_df)
    plot_keyword_search_results(fuzzy_result, keyword_columns=fuzzy_keywords, title="Fuzzy Keyword Search Results")
