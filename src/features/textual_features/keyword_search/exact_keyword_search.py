import pandas as pd
import re

from unstructured.cleaners.core import clean


def search_text_for_keywords(text: str,
                            keyword_dict: dict) -> dict:
    """ Function to find one-word or multiple-word keywords in input text.

    This function is used to search for keywords in a text. It takes as input a text and a dictionary with keywords
    and returns a dictionary with the keywords found in the text. it is case-insensitive and uses substring matching.

    Args:
        text: Input string to be searched for keywords
        keyword_dict: Dictionary listing relevant keyword values per key

    Returns:
        result: Dictionary with found keywords per input

    """
    words = re.findall(r'\w+', text.lower())
    
    # init empty dict
    result = {}

    # iterate over dictionary to get key-value pairs
    for key, keywords in keyword_dict.items():
        found_keywords = []

        # iterate over values (as there may be multiple per key)
        for keyword in keywords:
            # if one keyword consists of multiple words, split them
            if " " in keyword:
                combined_words = keyword.split()
                # search for keywords
                if all(combined_word.lower() in words for combined_word in combined_words):
                    found_keywords.append(keyword)
            else:
                # search for keywords
                if any(keyword.lower() in word for word in words):
                    found_keywords.append(keyword)
        
        # store found keywords
        if found_keywords:
            result[key] = found_keywords
        # assign None if no keywords were found
        else:
            result[key] = None
        
    return result


def search_df_for_keywords(input_df: pd.DataFrame,
                           id_column_name: str,
                           text_column_name: str,
                           keyword_dict: dict,
                           boolean: bool = False) -> pd.DataFrame:
    """ Function to process columns row by row, checking for all entries from keyword dict.

    This function is used to search for keywords in a df. It takes as input a df and a dictionary with keywords
    and returns a df with the keywords found in the text. It leverages the search_text_for_keywords function.

    Args:
        input_df: Input df to be searched for keywords
        id_column_name: Name of the identifying column (e.g., filename)
        text_column_name: Name of the column in the input df holding the relevant text
        keyword_dict: Dict of relevant keywords
        boolean: defaults to False; if True, df is returned with booleans instead of strings

    Returns:
        df: Output df holds found keywords per key (column) and id (row)

    """
    id_column = []
    result_data = []

    # extract id and content from input_df; clean content column
    input_df = input_df[[id_column_name, text_column_name]].copy()
    input_df[text_column_name] = input_df[text_column_name].astype(str).apply(lambda x: clean(x, lowercase=True, dashes=True))

    # iterate over df and find keywords
    for id, content in input_df.itertuples(index=False):
        # store id per row
        id_column.append(id)
        # find keywords per row
        keyword_presence = search_text_for_keywords(content, keyword_dict)
        result_data.append(keyword_presence)
    
    # convert to df
    result_df = pd.DataFrame(result_data)
    result_df.insert(0, id_column_name, id_column)

    if boolean:
        # preserve id column; convert + concatenate boolean columns
        boolean_df = result_df.iloc[:, 1:len(result_df)+1].notna()
        result_df = pd.concat([result_df.iloc[:, 0], boolean_df], axis = 1)

    return result_df

