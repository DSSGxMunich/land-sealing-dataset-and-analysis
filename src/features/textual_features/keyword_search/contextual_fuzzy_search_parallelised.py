import json
import os
import pandas as pd

from loguru import logger
from multiprocessing import Process

from contextual_fuzzy_search import search_df_for_best_matches

# specify paths
BASE_DIR = 'features/textual_features/keyword_search'
INPUT_FILE_PATH = '../data/nrw/bplan/raw/text/bp_text.json'
OUTPUT_FOLDER_PATH = "../data/nrw/bplan/features/keywords/fuzzy_search"

# set relevant variables
ID_COLUMN = 'filename'
TEXT_COLUMN = 'content'
METADATA_COLUMNS = 'metadata'
THRESHOLD = 80  # for similarity in fuzzy search
CONTEXT_WORDS = 20  # for no. of words extracted in fuzzy search

input_df = pd.read_json(INPUT_FILE_PATH)
input_df.columns = [ID_COLUMN,TEXT_COLUMN,METADATA_COLUMNS]

# define relevant keywords
with open(os.path.join(BASE_DIR, 'keyword_dict_fuzzy.json')) as f:
    FUZZY_KEYWORDS = json.load(f)


# set up to parallelize fuzzy search
def process_fuzzy_batch(input_df: pd.DataFrame,
                        id_column_name: str,
                        text_column_name: str,
                        keyword: str,
                        threshold: int,
                        context_words: int):
    """ Function to process a batch of fuzzy searches in parallel. It saves the results to a csv file

    This function is used to parallelize the fuzzy search.

    Args:
        input_df (pd.DataFrame): DataFrame with the text to search in
        id_column_name (str): name of the column with the id
        text_column_name (str): name of the column with the text
        keyword (str): keyword to search for
        threshold (int): threshold for similarity in fuzzy search
        context_words (int): number of words to extract in fuzzy search

    """
    # apply function for fuzzy search
    result_df = search_df_for_best_matches(input_df,
                                           id_column_name,
                                           text_column_name,
                                           keyword,
                                           threshold,
                                           context_words)

    result_df.to_csv(os.path.join(OUTPUT_FOLDER_PATH, keyword + ".csv"), header=True)

    logger.info(f"Done with {keyword}")


def run_fuzzy():
    """ Function to run the fuzzy search in parallel. It saves the results to multiple csv files.

    This function is used to parallelize the fuzzy search.

    Note:
        This function starts multiple processes and waits for them to complete. It is not suitable for running in a notebook.
        Also, it starts a process for each keyword, which might not be the most efficient way to parallelize the fuzzy search
        and might not be suitable if number_of_keywords > number_of_cores.
    """
    processes = [Process(target=process_fuzzy_batch, args=[input_df,
                                                           ID_COLUMN,
                                                           TEXT_COLUMN,
                                                           keyword,
                                                           THRESHOLD,
                                                           CONTEXT_WORDS]) for keyword in FUZZY_KEYWORDS]
    for process in processes:
        process.start()
    # wait for all processes to complete
    for process in processes:
        process.join()


if __name__ == '__main__':
    logger.info(f"Let's go!")
    run_fuzzy()
    logger.info(f"Fuzzy search done!")
