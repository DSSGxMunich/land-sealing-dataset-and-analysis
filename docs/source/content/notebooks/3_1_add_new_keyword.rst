.. figure:: assets/dssg_banner.png
   :alt: dssg_banner


.. code:: ipython3

    import os
    import pandas as pd
    
    from features.textual_features.keyword_search.contextual_fuzzy_search import search_df_for_best_matches
    
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

Create keyword table
====================

What keyword are you interested in? Choose your keyword here:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    keyword = 'lichtemissionen'

All other variables may remain the same, but you can also change them as you wish.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    id_column_name = 'filename'
    text_column_name = 'content'
    
    input_df = pd.read_csv(os.path.join("..", "data", "nrw", "bplan", "raw", "text",  "document_texts.csv"), header=0)
    
    threshold = 99
    context_words = 10

Some explanation:
^^^^^^^^^^^^^^^^^

-  ``id_column_name``: ‘filename’
-  ``text_column_name``: ‘content’

These two variables refer to columns in the ``input_df``, which is set
to ‘nrw_document_texts.csv’. If you change the input data, make sure to
update the column names too.

-  ``threshold``: 99

The search finds keyword matches according to a similarity threshold. If
set to 99, only exact matches are found. Choose a lower threshold if you
want to find ‘fuzzy’ matches too, e.g. to account for declination of
words, spelling errors or partial extraction from the original PDFs.

-  ``context_words``: 10

Setting this parameter allows to get the surrounding content and not
only the keyword itself. The specified number of words is extracted
before and after the keyword to place it in its context.

Here you can perform the search (no changes needed, just run this cell):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    all_matches = search_df_for_best_matches(input_df=input_df,
                                             id_column_name=id_column_name,
                                             text_column_name=text_column_name,
                                             keyword=keyword,
                                             threshold=threshold,
                                             context_words=context_words)

Check out the results
^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

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
          <th>lichtemissionen</th>
        </tr>
        <tr>
          <th>id</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>116995_4.pdf</th>
          <td>fledermaus vorkommen und brutstätten von vögeln zu untersuchen. lärm und lichtemissionen lärm und lichtemissionen sind so weit wie möglich zu begrenzen. ;;; brutstätten von vögeln zu untersuchen. lärm und lichtemissionen lärm und lichtemissionen sind so weit wie möglich zu begrenzen. die beleuchtung mit</td>
        </tr>
        <tr>
          <th>116995_8.pdf</th>
          <td>fledermaus vorkommen und brutstätten von vögeln zu untersuchen. lärm und lichtemissionen sind so weit wie möglich zu begrenzen. die beleuchtung mit</td>
        </tr>
        <tr>
          <th>2240212_1.pdf</th>
          <td>der beleuchtung sind insekten und fledermausfreundliche leuchtmittel zu bevorzugen und lichtemissionen (insbesondere streulicht) sind durch fachgerechte planung zu reduzieren. ein anstrahlen</td>
        </tr>
        <tr>
          <th>2368027_2.pdf</th>
          <td>stunden pro jahr und 30 minuten pro tag zu begrenzen. lichtemissionen zur vermeidung von lichtreflexionen sind die rotorblätter mit einem matten</td>
        </tr>
        <tr>
          <th>2368027_3.pdf</th>
          <td>bebauungsplan nr. 9 vdh projektmanagement gmbh erkelenz stand:juli 2013 60 lichtemissionen zur vermeidung von lichtreflexionen sind die rotorblätter mit einem matten</td>
        </tr>
        <tr>
          <th>2368044_1.pdf</th>
          <td>tatsächliche beschattungsdauer gemäß den vom lai empfohlenen beurteilungskriterien zu begrenzen. lichtemissionen zur vermeidung von lichtreflexionen sind die rotorblätter mit einem matten</td>
        </tr>
        <tr>
          <th>2368056_5.pdf</th>
          <td>stunden pro jahr und 30 minuten pro tag zu begrenzen. lichtemissionen zur vermeidung von lichtreflexionen sind die rotorblätter mit einem matten</td>
        </tr>
        <tr>
          <th>2369290_4.pdf</th>
          <td>änderung der bestehenden lichtverhältnisse auszugehen. eine erhebliche beeinträchtigung durch mögliche lichtemissionen (aus dem gebiet heraus) ist allerdings bei ent sprechender ausrichtung</td>
        </tr>
        <tr>
          <th>2369334_2.pdf</th>
          <td>die erschütterungen sind bauzeitenbedingt und damit temporär. 2.cc 4 licht lichtemissionen sind durch eine beleuchtung der straßen und stellplätze bereits vorhanden</td>
        </tr>
        <tr>
          <th>2369376_6.pdf</th>
          <td>versiegelt und zur sicherung des betriebsablaufes bei bedarf ausgeleuchtet. die lichtemissionen werden sich im verhältnis zu den bestehenden nicht wesentlich erhöhen. ;;; der lebensräume durch verkehrswege emissionen des transport und straßenverkehrs bestehende lichtemissionen im bereich des bestehenden gewerbegebietes 1.2.1.2 wirkfaktoren des vorhabens folgende ;;; der bauzeit � kollisionseffekte durch verkehrsbewegungen sind zu vernachlässigen die lichtemissionen werden sich im verhältnis zu den bestehenden dauerhaft nicht wesentlich</td>
        </tr>
        <tr>
          <th>2369623_1.pdf</th>
          <td>anzahl der lichtpunkte etc. ist zu achten, so dass zukünftige lichtemissionen nur unsensible bereiche bestrahlen und die obere baumkronenhälfte als dunkelraum</td>
        </tr>
        <tr>
          <th>2369671_3.pdf</th>
          <td>/ 59 200) ist zu verständigen. 5. 6. hinweis zu lichtemissionen auf privaten grundstücken: zur reduzierung von belastungen des umfelds (insbesondere</td>
        </tr>
        <tr>
          <th>2369672_1.pdf</th>
          <td>/ 59 200) ist zu verständigen. 5. 6. hinweis zu lichtemissionen auf privaten grundstücken: zur reduzierung von belastungen des umfelds (insbesondere</td>
        </tr>
        <tr>
          <th>2369687_0.pdf</th>
          <td>sie müssen regelungsbestandteil des durchführungsvertrages werden. 4. sonstige festsetzungen 4.1 lichtemissionen außerhalb der zulässigen gebäude dürfen auf dem baugrundstück nur umweltfreundliche</td>
        </tr>
        <tr>
          <th>2370690_14.pdf</th>
          <td>gestört. bei einer umsetzung der planung ist eine zunahme der lichtemissionen durch gebäude und weg beleuchtung möglich. um potenzielle beeinträchtigungen gering</td>
        </tr>
      </tbody>
    </table>
    </div>



Save to other keywords
^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    OUTPUT_FILE_PATH = os.path.join("..", "data", "nrw", "bplan", "features", "keywords", "fuzzy_search", "fuzzy_search_")
    
    all_matches.to_csv(os.path.join(OUTPUT_FILE_PATH + keyword + ".csv"), header=True)
