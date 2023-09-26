.. figure:: assets/dssg_banner.png
   :alt: dssg_banner


.. code:: ipython2

    # Import the data generation functions
    from data_pipeline.rplan_content_extraction.rplan_utils import extract_text_and_save_to_txt_files
    from data_pipeline.rplan_content_extraction.rplan_content_extractor import parse_rplan_directory
    from data_pipeline.rplan_content_extraction.rplan_utils import parse_result_df
    
    # Import the keyword search functions
    from data_pipeline.rplan_content_extraction.rplan_keyword_search import rplan_exact_keyword_search
    # Import the visualization function
    from visualizations.rplan_visualization import plot_keyword_search_results

Regional plans
==============

This notebook shows how to extract content from regional plans,
i.e. parse the text from the pdfs and divide them into chapters /
sections.

.. code:: ipython2

    # Set the paths to the PDF and TXT directories
    RPLAN_PDF_DIR = "../data/nrw/rplan/raw/pdfs"
    RPLAN_TXT_DIR = "../data/nrw/rplan/raw/text"
    RPLAN_OUTPUT_PATH = "../data/nrw/rplan/features/rplan_content.json"

Step 1: Generate content
------------------------

.. code:: ipython2

    extract_text_and_save_to_txt_files(pdf_dir_path=RPLAN_PDF_DIR,
                                       txt_dir_path=RPLAN_TXT_DIR)
    
    input_df = parse_rplan_directory(txt_dir_path=RPLAN_TXT_DIR, 
                                     json_output_path=RPLAN_OUTPUT_PATH)
    
    input_df = parse_result_df(df=input_df)
    
    # save df as JSON
    input_df.to_json(RPLAN_OUTPUT_PATH)

Step 2: Exact keyword search
----------------------------

Now we perform an exact keyword search on the data and plot the results.

.. code:: ipython2

    exact_result, exact_keywords = rplan_exact_keyword_search(input_df=input_df)
    plot_keyword_search_results(exact_result, keyword_columns=exact_keywords,
                                title="Exact Keyword Search Results")
