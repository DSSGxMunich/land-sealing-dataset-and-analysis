.. figure:: assets/dssg_banner.png
   :alt: dssg_banner


.. code:: ipython3

    # necessary imports
    import json
    import os
    import pandas as pd
    
    from features.textual_features.keyword_search.exact_keyword_search import search_df_for_keywords
    
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

Exact keyword search for paragraphs from BauNVO & BauGB
=======================================================

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
    INPUT_FILE_PATH = os.path.join("..", "data", "nrw", "bplan", "raw", "text", "bp_text.csv")
    OUTPUT_FILE_PATH = os.path.join("..", "data", "nrw", "bplan", "features", "keywords", "exact_search", "exact_search.csv")
    
    # specify relevant column names
    ID_COLUMN='filename'
    TEXT_COLUMN='content'
    
    # read in data
    input_df = pd.read_csv(INPUT_FILE_PATH, names=[ID_COLUMN, TEXT_COLUMN])

Define keyword dictionary
-------------------------

Keywords are specified in a separate json file to apply the exact
keyword search more easily to different sets of keywords, simply by
reading in the relevant dictionary. The dictionary is structured so that
each keyword category (e.g. baunvo-1) can contain one or more keywords
to consider the category covered (e.g., “§1 baunvo”, “1 baunvo”, or
“allgemeine vorschriften für bauflächen und baugebiete”).

.. code:: ipython3

    with open('features/textual_features/keyword_search/keyword_dict_exact.json') as f:
        BAUNVO_KEYWORDS = json.load(f)

Apply function
==============

Exact keyword matching based on input dictionary, returns df showing
which keyword appeared in each pdf per category.

.. code:: ipython3

    result_df = search_df_for_keywords(input_df=input_df,
                                       text_column_name=TEXT_COLUMN,
                                       id_column_name=ID_COLUMN,
                                       keyword_dict=BAUNVO_KEYWORDS)
    
    result_df.head(30)




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
          <th></th>
          <th>filename</th>
          <th>baunvo-1</th>
          <th>baunvo-2</th>
          <th>baunvo-3</th>
          <th>baunvo-4</th>
          <th>baunvo-4a</th>
          <th>baunvo-5</th>
          <th>baunvo-5a</th>
          <th>baunvo-6</th>
          <th>baunvo-6a</th>
          <th>...</th>
          <th>baunvo-17</th>
          <th>baunvo-18</th>
          <th>baunvo-19</th>
          <th>baunvo-20</th>
          <th>baunvo-21</th>
          <th>baunvo-21a</th>
          <th>13b</th>
          <th>hq100</th>
          <th>hqhäufig</th>
          <th>hqextrem</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>116995_0.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>1</th>
          <td>116995_10.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>2</th>
          <td>116995_2.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>3</th>
          <td>116995_4.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>[grz]</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>4</th>
          <td>116995_6.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>5</th>
          <td>116995_8.pdf</td>
          <td>[1 baunvo]</td>
          <td>[2 baunvo]</td>
          <td>[3 baunvo, reine wohngebiete]</td>
          <td>[4 baunvo, allgemeine wohngebiete]</td>
          <td>[besondere wohngebiete]</td>
          <td>[5 baunvo]</td>
          <td>None</td>
          <td>[6 baunvo]</td>
          <td>None</td>
          <td>...</td>
          <td>[17 baunvo]</td>
          <td>[18 baunvo]</td>
          <td>[19 baunvo, grundflächenzahl, grz]</td>
          <td>[20 baunvo, vollgeschosse, gfz]</td>
          <td>[21 baunvo]</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>6</th>
          <td>1423897.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>7</th>
          <td>1427478.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>8</th>
          <td>1427479.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>9</th>
          <td>1427480.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>10</th>
          <td>1427481.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>11</th>
          <td>1427482.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>12</th>
          <td>1427483.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>13</th>
          <td>1434116.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>14</th>
          <td>1691730_0.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>15</th>
          <td>1691731_1.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>16</th>
          <td>1691739_0.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>17</th>
          <td>1691739_1.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>18</th>
          <td>1691739_2.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[besondere wohngebiete]</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>19</th>
          <td>1691740_0.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>20</th>
          <td>1691740_1.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>21</th>
          <td>1691740_2.pdf</td>
          <td>[1 baunvo]</td>
          <td>[2 baunvo]</td>
          <td>[3 baunvo]</td>
          <td>[4 baunvo]</td>
          <td>None</td>
          <td>[5 baunvo]</td>
          <td>None</td>
          <td>[6 baunvo]</td>
          <td>None</td>
          <td>...</td>
          <td>[17 baunvo]</td>
          <td>[18 baunvo]</td>
          <td>[19 baunvo]</td>
          <td>[20 baunvo]</td>
          <td>[21 baunvo]</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>22</th>
          <td>1691744_0.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>23</th>
          <td>1691744_1.pdf</td>
          <td>[1 baunvo]</td>
          <td>[2 baunvo]</td>
          <td>[3 baunvo]</td>
          <td>[4 baunvo]</td>
          <td>None</td>
          <td>[5 baunvo]</td>
          <td>None</td>
          <td>[6 baunvo]</td>
          <td>None</td>
          <td>...</td>
          <td>[17 baunvo]</td>
          <td>[18 baunvo]</td>
          <td>[19 baunvo]</td>
          <td>[20 baunvo]</td>
          <td>[21 baunvo]</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>24</th>
          <td>1691744_2.pdf</td>
          <td>[1 baunvo]</td>
          <td>[2 baunvo]</td>
          <td>[3 baunvo]</td>
          <td>[4 baunvo]</td>
          <td>None</td>
          <td>[5 baunvo]</td>
          <td>None</td>
          <td>[6 baunvo]</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>25</th>
          <td>1691766_0.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>26</th>
          <td>1691766_1.pdf</td>
          <td>[1 baunvo]</td>
          <td>[2 baunvo]</td>
          <td>[3 baunvo]</td>
          <td>[4 baunvo]</td>
          <td>None</td>
          <td>[5 baunvo]</td>
          <td>None</td>
          <td>[6 baunvo]</td>
          <td>None</td>
          <td>...</td>
          <td>[17 baunvo]</td>
          <td>[18 baunvo]</td>
          <td>[grundflächenzahl, grz]</td>
          <td>[20 baunvo, vollgeschosse]</td>
          <td>None</td>
          <td>[stellplätze]</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>27</th>
          <td>1691782_0.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>28</th>
          <td>1691782_1.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
        <tr>
          <th>29</th>
          <td>1691782_2.pdf</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
        </tr>
      </tbody>
    </table>
    <p>30 rows × 31 columns</p>
    </div>



Check results
-------------

To inspect the keyword coverage across all files:

.. code:: ipython3

    result_df.count()




.. parsed-literal::

    filename      21573
    baunvo-1       7086
    baunvo-2       7217
    baunvo-3       7259
    baunvo-4       7542
    baunvo-4a      2758
    baunvo-5       7152
    baunvo-5a       499
    baunvo-6       7370
    baunvo-6a       619
    baunvo-7       6819
    baunvo-8       7186
    baunvo-9       7105
    baunvo-10      6658
    baunvo-11      6415
    baunvo-12      6864
    baunvo-13      5701
    baunvo-13a     1985
    baunvo-14      6182
    baunvo-15      6167
    baunvo-16      6239
    baunvo-17      4991
    baunvo-18      6409
    baunvo-19      6920
    baunvo-20      6897
    baunvo-21      5249
    baunvo-21a     6129
    13b             224
    hq100           379
    hqhäufig        151
    hqextrem        242
    dtype: int64



Also, for a given pdf, one can extract all usage options listed in the
bplan:

.. code:: ipython3

    print(result_df.loc[[5]].values.tolist())


.. parsed-literal::

    [['116995_8.pdf', ['1 baunvo'], ['2 baunvo'], ['3 baunvo', 'reine wohngebiete'], ['4 baunvo', 'allgemeine wohngebiete'], ['besondere wohngebiete'], ['5 baunvo'], None, ['6 baunvo'], None, ['7 baunvo'], ['8 baunvo'], ['9 baunvo'], ['10 baunvo'], ['11 baunvo'], ['12 baunvo'], ['13 baunvo'], None, ['14 baunvo'], ['15 baunvo'], ['16 baunvo'], ['17 baunvo'], ['18 baunvo'], ['19 baunvo', 'grundflächenzahl', 'grz'], ['20 baunvo', 'vollgeschosse', 'gfz'], ['21 baunvo'], None, None, None, None, None]]


Transform to Boolean
====================

For better consecutive analysis, Boolean values may be preferred. The
optional argument ``boolean=True`` can be set. Instead of an overview of
all keyword hits per category, a dataframe will be returned that shows
whether a category was covered or not.

.. code:: ipython3

    boolean_result_df = search_df_for_keywords(input_df=input_df,
                                               text_column_name=TEXT_COLUMN,
                                               id_column_name=ID_COLUMN,
                                               keyword_dict=BAUNVO_KEYWORDS,
                                               boolean=True)

Write results to csv
====================

.. code:: ipython3

    result_df.to_csv(OUTPUT_FILE_PATH, header=True, index=False)
