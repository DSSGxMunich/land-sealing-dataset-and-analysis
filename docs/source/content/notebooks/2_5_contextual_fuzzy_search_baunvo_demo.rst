.. figure:: assets/dssg_banner.png
   :alt: dssg_banner


.. code:: ipython3

    import os
    import pandas as pd
    
    from features.textual_features.keyword_search.contextual_fuzzy_search import search_df_for_best_matches
    
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

Contextual fuzzy keyword search
===============================

| **Why contextual?** To get surrounding content rather than keyword
  only.
| **Why fuzzy?** To allow non-exact keyword matching based on a
  similarity search, e.g. to account for spelling errors or partial
  extraction from the original PDFs.

Prepare data
------------

-  **Change the folder path** in the code block below to read in the
   data.
-  **Specify the relevant column names.** The function that is used in
   the following expects the input data frame to have (at least) two
   columns, i.e., one id and one content column. Here, the columns are
   called ``filename`` and ``content``. If named differently, change the
   column names in the code below.

.. code:: ipython3

    # specify file path
    INPUT_FOLDER_PATH = os.path.join("..", "data", "nrw", "bplan", "raw", "text", "bp_text.csv")
    OUTPUT_FILE_PATH = os.path.join("..", "data", "nrw", "bplan", "features", "keywords", "fuzzy_search", "fuzzy_search_")
    
    # specify relevant column names
    ID_COLUMN='filename'
    TEXT_COLUMN='content'
    
    # read in data
    input_df = pd.read_csv(INPUT_FOLDER_PATH, names=[ID_COLUMN, TEXT_COLUMN])

Apply fuzzy keyword search to keyword of choice and extract the best matches
----------------------------------------------------------------------------

-  Adjust ``keyword``
-  Adjust ``threshold``: minimum similarity score
-  Adjust ``context_words``: number of words extracted to contextualise
   keyword

Note: To apply the fuzzy search to multiple keywords at once,
``contextual_fuzzy_search_parallelised.py`` can be run. Only adjust the
file paths and variables in lines 13 to 22. The corresponding dictionary
is ``keyword_dict_fuzzy`` and can easily be adapted if necessary.

.. code:: ipython3

    KEYWORD='minimale gebäudehöhe'
    THRESHOLD=90
    CONTEXT_WORDS=15

.. code:: ipython3

    all_matches = search_df_for_best_matches(input_df=input_df,
                                             id_column_name=ID_COLUMN,
                                             text_column_name=TEXT_COLUMN,
                                             keyword=KEYWORD,
                                             threshold=THRESHOLD,
                                             context_words=CONTEXT_WORDS)
    
    all_matches.head(15)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th>keyword</th>
          <th>minimale gebäudehöhe</th>
        </tr>
        <tr>
          <th>id</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2408410_1.pdf</th>
          <td>deshalb ist bei der errichtung eines geneigten daches von 6° bis einschließlich 25° dachneigung eine minimale gebäudehöhe von 6,00 metern und eine maximale gebäudehöhe von 8,00 metern einzuhalten. diese festsetzung ermöglicht besonders ;;; dies ist nicht ziel der städtebaulichen entwicklung. daher wird zusätzlich festgesetzt, dass für pultdächer eine minimale gebäudehöhe von 5,00 metern und eine maximale von 7,00 metern gilt. 5 durch die zulässigkeit von</td>
        </tr>
        <tr>
          <th>2408419_1.pdf</th>
          <td>zu können. deshalb ist bei der errichtung eines geneigten daches bis einschließlich 25° dachneigung eine minimale gebäudehöhe von 6,00 metern und eine maximale gebäudehöhe von 8,00 metern einzuhalten. diese festsetzung ermöglicht besonders ;;; nicht ziel der städtebaulichen entwicklung. daher wird zusätzlich festgesetzt, dass 6 für einhüftige pultdächer eine minimale gebäudehöhe von 5,00 metern und eine maximale von 7,00 metern gelten. durch v.g. vorgaben, die zulässigkeit</td>
        </tr>
        <tr>
          <th>2408438_1.pdf</th>
          <td>bei der errichtung eines geneigten daches mit einer dachneigung von 6° bis einschließlich 25° eine minimale gebäudehöhe von 6,00 metern und eine maximale gebäudehöhe von 8,00 metern einzuhalten. diese festsetzung ermöglicht besonders ;;; nicht ziel der städtebaulichen entwicklung. daher wird zusätz lich festgesetzt, dass für einhüftige pultdächer eine minimale gebäudehöhe von 5,00 metern und eine maximale von 7,00 metern gelten. durch die zulässigkeit von einzel</td>
        </tr>
        <tr>
          <th>2408724_0.pdf</th>
          <td>rahmen erhält. zur erreichung dieser zielsetzung wird zusätzlich festgesetzt, dass für einhüftige pult dächer eine minimale gebäudehöhe von 5,00 metern und eine maximale von 7,00 metern gelten. der zur ermittlung der höhe</td>
        </tr>
        <tr>
          <th>2408724_8.pdf</th>
          <td>rahmen erhält. zur erreichung dieser zielsetzung wird zusätzlich festgesetzt, dass für einhüftige pult dächer eine minimale gebäudehöhe von 5,00 metern und eine maximale von 7,00 metern gelten. der zur ermittlung der höhe</td>
        </tr>
        <tr>
          <th>2408729_1.pdf</th>
          <td>zu können. deshalb ist bei der errichtung eines geneigten daches bis einschließlich 25° dachneigung eine minimale gebäudehöhe von 6,00 metern und eine maximale gebäudehöhe von 8,00 metern einzuhalten. diese festsetzung soll der</td>
        </tr>
        <tr>
          <th>2408758_1.pdf</th>
          <td>zu können. deshalb ist bei der errichtung eines geneigten daches bis einschließlich 25° dachneigung eine minimale gebäudehöhe von 6,00 metern und eine maximale gebäudehöhe von 8,00 metern einzuhalten. diese festsetzung ermöglicht besonders</td>
        </tr>
        <tr>
          <th>2408762_1.pdf</th>
          <td>ist nicht ziel der städtebaulichen entwicklung. daher wird zusätzlich festgesetzt, dass für einhüftige pultdächer eine minimale gebäudehöhe von 5,00 metern und eine maximale ge bäudehöhe von 7,00 metern gelten. die überbaubare grundstücksfläche</td>
        </tr>
        <tr>
          <th>2408772_1.pdf</th>
          <td>zur erreichung dieser zielsetzung wird zusätzlich festgesetzt, dass für einhüftige pultdächer sowie für flachdächer eine minimale gebäudehöhe von 5,00 metern und eine maximale von 7,00 metern gelten. der zur ermittlung der v.g</td>
        </tr>
      </tbody>
    </table>
    </div>



Write results to csv
====================

.. code:: ipython3

    all_matches.to_csv(os.path.join(OUTPUT_FILE_PATH + KEYWORD + ".csv"), header=True)


.. parsed-literal::

    The history saving thread hit an unexpected error (OperationalError('database is locked')).History will not be written to the database.

