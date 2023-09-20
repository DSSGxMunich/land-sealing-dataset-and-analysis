import json
import os
import pandas as pd

from loguru import logger
from multiprocessing import Process

from contextual_fuzzy_search import search_df_for_best_matches


# specify paths
BASE_DIR = os.path.join("src", "features", "textual_features", "keyword_search")
INPUT_FILE_PATH = os.path.join("data", "nrw", "text", "nrw_final_all.csv")
OUTPUT_FOLDER_PATH = os.path.join("data", "nrw", "features", "fuzzy_search", "parallel")

# set relevant variables
ID_COLUMN = 'filename'
TEXT_COLUMN = 'content'
THRESHOLD = 80  # for similarity in fuzzy search
CONTEXT_WORDS = 20  # for no. of words extracted in fuzzy search

input_df = pd.read_csv(INPUT_FILE_PATH, names=[ID_COLUMN, TEXT_COLUMN])

# define relevant keywords
with open(os.path.join(BASE_DIR, 'keyword_dict_fuzzy.json')) as f:
    FUZZY_KEYWORDS = json.load(f)

# set up to parallelise fuzzy search
def process_fuzzy_batch(input_df,
                        id_column_name,
                        text_column_name,
                        keyword,
                        threshold,
                        context_words):

    # apply function for fuzzy search
    result_df = search_df_for_best_matches(input_df,
                                           id_column_name,
                                           text_column_name,
                                           keyword,
                                           threshold,
                                           context_words)
    
    result_df.to_csv(os.path.join(OUTPUT_FOLDER_PATH, keyword + ".csv"), header=True)
    
    logger.info(f"Done with {keyword}")


def run_fuzzy():
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
