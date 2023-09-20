import json
import openai
import os
import pandas as pd

from dotenv import load_dotenv
from loguru import logger
from multiprocessing import Process

from agentic_knowledge_extractor import extract_knowledge_from_df


# set paths
BASE_DIR = os.path.join("src", "features", "textual_features", "knowledge_extraction_agent")
INPUT_FOLDER_PATH = os.path.join("data", "nrw", "features", "fuzzy_search", "parallel")
OUTPUT_FOLDER_PATH = os.path.join("data", "nrw", "features", "knowledge_extraction_agent")

# set relevant variables
ID_COLUMN = 'filename'
TEXT_COLUMN = 'content'

# set nested dictionary
with open(os.path.join(BASE_DIR, 'keyword_dict_agent.json')) as f:
    AGENT_KEYWORDS = json.load(f)

# set api key from .env file
load_dotenv()
openai.api_key=os.getenv('OPENAI_API_KEY')


# set up function per process
def process_agent_batch(id_column_name,
                        text_column_name,
                        keyword_dict):

    # read in file
    filename = keyword_dict['filename']
    input_df = pd.read_csv(f'{INPUT_FOLDER_PATH}/{filename}', names=[ID_COLUMN, TEXT_COLUMN])

    # apply function for fuzzy search
    result_df = extract_knowledge_from_df(input_df=input_df,
                                          id_column_name=id_column_name,
                                          text_column_name=text_column_name,
                                          keyword_dict=keyword_dict)
    
    # save as json
    result_json = result_df.to_json(orient='records')
    with open(os.path.join(OUTPUT_FOLDER_PATH, keyword_dict['keyword_short'] + ".json"), "w") as outputfile:
        outputfile.write(result_json)
    
    logger.info(f"Done with {keyword_dict['keyword_short']}")


# set up function to run processes in parallel
def run_agent():
    processes = []

    for keyword_dict in AGENT_KEYWORDS:
        process = Process(target=process_agent_batch, args=(ID_COLUMN, TEXT_COLUMN, keyword_dict))
        processes.append(process)
        process.start()

        # wait for all processes to complete
    for process in processes:
        process.join()


if __name__ == '__main__':
    logger.info(f"Let's go!")
    run_agent()
    logger.info(f"Agent done!")
