-----------------
Notebooks
-----------------

Jupyter notebooks were created to facilitate the use, reproducibility and understanding of the content and especially the results of this repository.

0. The data exploration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following notebook was used to explore the data and to get a better understanding of the data structure and content. It is not required to run the pipeline, but may be helpful to understand the data and the pipeline.

.. nbgallery::

    notebooks/explorer

1. The execute pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is the main notebook that runs the entire pipeline from data download (i.e., the pdfs of bplans in NRW) to feature extraction (e.g., keyword search) to creation of the final data tables. This notebook can be run unchanged to reproduce the pipeline and results of this repository. This notebook can also be run with new data input (e.g., other federal state) or any other desired changes, however, reproducibility is only guaranteed for unchanged data input and pipeline. Mentioned changes to data input may require slight adjustments of the pipeline.


.. nbgallery::

    notebooks/1_execute_pipeline

2. The sub-processes of the pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All the following notebooks reproduce sub-processes of the above pipeline. Each notebook contains detailed explanations of the steps taken and scope for adjustment of parameters or data input.

Downloading and processing the data
""""""""""""""""""""""""""""""""""""""""""""""""""

2.1 `Get started: PDF downloader for land parcels of Bebauungspläne`
This notebook demonstrates the process of downloading the relevant pdf files from information provided on the NRW geoportal. After the download is complete, the bplan metadata is matched with rplans to enrich resulting data table land_parcels.csv with all relevant information.

2.2 `How to: create document_texts table`
Most pdf files downloaded in the previous step are in a non-machine readable format. In order to nevertheless extract and use the textual information from the files, the pdf scraper was built. The scraper reads all pdf files from a specified folder, extracts the text and returns a csv file with all file names and corresponding text blobs.

2.3 `How to: create document_texts table`
The text blobs extracted in the previous step are enriched with information about the land parcels to which they belong. This creates the data table document_texts.csv.

.. nbgallery::

    notebooks/2_1_land_parcels_demo
    notebooks/2_2_pdf_scraper_demo
    notebooks/2_3_document_texts_demo

Extracting the keywords
""""""""""""""""""""""""""""""""""""""""""""""""""


2.4 `Exact keyword search for paragraphs from BauNVO & BauGB`:
This notebook runs the exact keyword search. The relevant keywords are specified in a separate json file to apply the exact keyword search more easily to different sets of keywords. The dictionary used in this notebook is structured so that each keyword category (e.g. baunvo-1) can contain one or more keywords to consider the category covered (e.g., “§1 baunvo”, “1 baunvo”, or “allgemeine vorschriften für bauflächen und baugebiete”). The output shows either explicitly the keywords per category found in each file or, if so specified, only True/False per category. Both options are illustrated in the notebook.

2.5 `Contextual fuzzy keyword search`:
This notebook runs the contextual (i.e., extract keyword and surrounding words), fuzzy (i.e., non-exact keyword matching based on Levenshtein distance similarity search, e.g. to account for spelling errors or non-perfect extraction from the original PDFs) keyword search for six keyword related to the baunvo (i.e., firsthöhe, traufhöhe, minimale gebäudehöhe, maximale gebäudehöhe, höhe baulicher anlagen, grundflächenzahl, geschossflächenzahl). This is especially important if we are not only interested in the mere occurrence of a certain keyword, but its context also contains valuable information. Here we want to know, for example, not only whether the different building heights were mentioned or not, but what their actual values are (see knowledge_agent_demo).

2.6 `Contextual fuzzy keyword search for flooding-related keywords`:
This particular notebook differs from 2.5 not only in the content of the input keywords, but also in their input format. While the previous notebook only uses a list of relevant words as input, this notebook works with a dictionary. This means that several keywords can be assigned to one main category. For example, the category “hq100" is covered by the terms “hq100”, “jahrhunderthochwasser”, “100-jährliches hochwasser”, and “hundertjährliches hochwasser”.

2.7 `Agentic knowledge extractor`:
Lastly, this notebook uses a Large Language Model (LLM) as an agent in order to extract knowledge from text input. Note that this shall require an OpenAI API key of your own. The text snippets extracted by the fuzzy search are here used as input to prompt the LLM. We are interested to find out the actual value of a given keyword from its context. For example, the keyword may be “Firsthöhe” (= ridge height), so we’d like to find out the actual height specified in the bplan.

.. nbgallery::

    notebooks/2_4_exact_keyword_search_demo
    notebooks/2_5_contextual_fuzzy_search_baunvo_demo
    notebooks/2_6_contextual_fuzzy_search_hochwasser_demo
    notebooks/2_7_knowledge_agent_demo

Parsing the regional plans
""""""""""""""""""""""""""""""""""""""""""""""""""

2.8 `Regional Plans`:
This notebook shows how to extract content from regional plans, i.e. parse the text from the pdfs and divide them into chapters / sections.


.. nbgallery::

    notebooks/2_8_regional_plans_demo

3. Beyond the pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The main pipeline can be extended to include new features or refined by further analyses. The following notebooks illustrate a few exemplary use cases or extensions.

`3.1 Create keyword zable`:
When interested in adding a new keyword that is not yet covered by the previous searches, this notebook can be used to facilitate the process. At the very top, the notebook asks to specify a keyword of choice. Technically, adding this new keyword is all that would be required, but the search could also be customised as desired. The notebook searches all pdf documents, displays the found matches and saves them in the relevant folder.

`3.4 Keyword Negation`:
For cases where results are to be excluded from the keyword search if they occur together with certain keywords, a negated keyword search can be performed. Using the regional plans, this notebook shows how to perform a negated keyword search to remove false positives from the search results.

.. nbgallery::

    notebooks/3_1_add_new_keyword
    notebooks/3_2_keyword_negation
