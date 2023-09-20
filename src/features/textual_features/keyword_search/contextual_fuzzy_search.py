import pandas as pd

from loguru import logger
from thefuzz import fuzz
from unstructured.cleaners.core import clean


def find_best_matches(id: str,
                      content: str,
                      keyword: str,
                      threshold: int,
                      context_words: int) -> list:
    """
    Function that finds best matches for a given keyword / keyword combination in the input string.

    Args:
        id: identifier of the content (e.g.,filename)
        content: textual input to be searched for keyword
        keyword: one or multiple word input of interest
        threshold: for similarity search between input and keyword
        context_words: get surrounding context of -x and +x words

    Returns:
        best_matches: list of dictionaries containing
            - id,
            - keyword,
            - matched_phrase, and
            - similarity score per match

    """
    # split content string into words, get no. of words in content string
    words = content.split()
    content_length = len(words)

    # get no. of keywords in keyword string
    key_length = len(keyword.split())
    
    # init
    best_matches = []

    # iterate through text input in stepsize of key_length
    for i in range(0, content_length+1, key_length):
        
        # generate phrases and get similarity between phrase + keyword
        phrase = " ".join(words[i:i+key_length])
        similarity_score = fuzz.ratio(phrase, keyword)

        # only get matches above threshold
        if similarity_score > threshold:
            # calculate -x and +x for context words
            start_context = max(0, i-context_words)
            end_context = min(content_length, i+context_words+key_length)

            # extract keyword and its surroundings
            context_phrase = " ".join(words[start_context:end_context])

            best_matches.append({
                'id': id,
                'keyword': keyword,
                'matched_phrase': context_phrase,
                'similarity_score': similarity_score
            })

    # sort by similarity score in descending order
    best_matches.sort(key=lambda x: x['similarity_score'], reverse=True)
    return best_matches


def search_df_for_best_matches(input_df: pd.DataFrame,
                               id_column_name: str,
                               text_column_name: str,
                               keyword: str,
                               threshold: int = 70,
                               context_words: int = 3) -> pd.DataFrame:
    """
    Function that searches df for best matches.

    Args:
        input_df: expected to have 2 columns, i.e., 'id' and 'content' (exact naming may differ)
        id_column_name: name of the identifying column (e.g., filename)
        text_column_name: name of the column holding the relevant text
        keyword: one or multiple word input of interest
        threshold: for similarity search between input and keyword
        context_words: get surrounding context of -x and +x words

    Returns:
        all_matches: df holding the best matches per id. If multiple are found,
            they are aggregated into one cell (using ';;; ' as separator).

    """
    # init empty df
    all_matches = pd.DataFrame()

    # extract id and content from input_df; clean content column
    input_df = input_df[[id_column_name, text_column_name]].copy()
    input_df.loc[:, text_column_name] = input_df[text_column_name].astype(str).apply(lambda x: clean(x, lowercase=True, dashes=True))

    for id, content in input_df.itertuples(index=False):
        # per ID, find best matches + corresponding scores for given keyword
        best_match = find_best_matches(id=id,
                                       content=content,
                                       keyword=keyword,
                                       threshold=threshold,
                                       context_words=context_words)
        
        best_match = pd.DataFrame(best_match)

        # concat to main df, holding best matches for all IDs
        all_matches = pd.concat([all_matches, best_match], axis=0)

    if len(all_matches) < 1:
        return logger.info(f"No matches for '{keyword}' at similarity threshold of {threshold} found.")

    # long format with 1 entry per id is preferred
    # if multiple entries for one id, they are joined into one cell
    wider_df = all_matches.pivot_table(index='id',
                                        columns='keyword',
                                        values='matched_phrase',
                                        aggfunc=lambda x: ' ;;; '.join(x))

    return wider_df
    


def search_best_matches_dict(input_df: pd.DataFrame,
                            id_column_name: str,
                            text_column_name: str,
                            keyword_dict: str,
                            threshold: int,
                            context_words: int):
    """Function that enables fuzzy search with keyword_dictionary input.

    Args:
        input_df: expected to have 2 columns, i.e., 'id' and 'content' (exact naming may differ)
        id_column_name: name of the identifying column (e.g., filename)
        text_column_name: name of the column holding the relevant text
        keyword_dict: dictionary of relevant keywords
        threshold: for similarity search between input and keyword
        context_words: get surrounding context of -x and +x words

    Returns:
        all_matches: df holding the best matches per id. If multiple are found,
            they are aggregated into one cell (using ';;; ' as separator).

    """
    results = pd.DataFrame()  # store results for each key
    
    for key, keywords in keyword_dict.items():
        
        combined_df = pd.DataFrame()  # store results for the current key

        for keyword in keywords:
            try:
                df = search_df_for_best_matches(input_df,
                                                id_column_name,
                                                text_column_name,
                                                keyword,
                                                threshold,
                                                context_words)  # call existing function
                
                if len(df) > 0:
                    df = df.rename(columns={keyword : 'contextualised_keyword'})
                    df['actual_keyword'] = keyword
                    df['category'] = key
                    df[id_column_name] = df.index
                    
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
    
            except TypeError:
                pass
        
        # check if there are any results for the current key
        if len(combined_df) > 0:
            results = pd.concat([results, combined_df], ignore_index=True)
    
    results = results.reset_index(drop=True)
    return results
    

def search_df_for_best_matches_keyword_dict(input_df: pd.DataFrame,
                                        id_column_name: str,
                                        text_column_name: str,
                                        keyword_dict: dict,
                                        default_threshold: int = 70,
                                        context_words: int = 3,
                                        boolean_output: bool = True):
    """ Wrapper function to search for multiple keywords in a df.

    Args:
        input_df: expected to have 2 columns, i.e., 'id' and 'content' (exact naming may differ)
        id_column_name: name of the identifying column (e.g., filename)
        text_column_name: name of the column holding the relevant text
        keyword_dict: dict of keywords to be searched for
        default_threshold: for similarity search between input and keyword
        context_words: get surrounding context of -x and +x words
        boolean_output: defaults to True; if True, df is returned with booleans instead of strings

    Returns:
        all_matches: df holding the best matches per id. If multiple are found,
            they are aggregated into one cell (using ';;; ' as separator).

    """
    all_matches = pd.DataFrame("",
                                columns=list(keyword_dict.keys()),
                                index=input_df.index
                                )
    all_matches = all_matches.reset_index()
    for main_keyword in keyword_dict:

        searchable_keywords = keyword_dict[main_keyword]["keywords"]
        # take threshold if exists, else use default
        threshold = keyword_dict[main_keyword].get("threshold", default_threshold)
        for searchable_keyword in searchable_keywords:
            result_df = search_df_for_best_matches(input_df=input_df,
                                                    id_column_name=id_column_name,
                                                    text_column_name=text_column_name,
                                                    keyword=searchable_keyword,
                                                    threshold=threshold,
                                                    context_words=context_words)
            # rename to matched_phrase
            if result_df.empty:
                logger.warning(f"No matches found for sub keyword {searchable_keyword}")
                continue
            result_df.columns = ["matched_phrase"]
            result_df = result_df.reset_index()
            # append each entry to the corresponding column and row
            for row in result_df.itertuples(index=False):
                all_matches.loc[row.id, main_keyword] = ';;;' + row.matched_phrase

    # remove leading ';;;'
    all_matches[main_keyword] = all_matches[main_keyword].str[3:]

    if boolean_output:
        boolean_df = all_matches.iloc[:, 1:len(all_matches)] != ''
        return pd.concat([all_matches.iloc[:, 0], boolean_df], axis=1)

    return all_matches
