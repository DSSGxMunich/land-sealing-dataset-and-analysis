.. figure:: assets/dssg_banner.png
   :alt: dssg_banner


.. code:: ipython3

    import json
    import os
    import pandas as pd
    
    from features.textual_features.keyword_search.contextual_fuzzy_search import search_best_matches_dict
    
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.max_rows', None)

Contextual fuzzy keyword search for flooding-related keywords
=============================================================

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
    OUTPUT_FILE_PATH = os.path.join("..", "data", "nrw", "bplan", "features", "keywords", "fuzzy_search", "fuzzy_search_hochwasser_")
    
    # specify relevant column names
    ID_COLUMN='filename'
    TEXT_COLUMN='content'
    
    # read in data
    input_df = pd.read_csv(INPUT_FOLDER_PATH,
                           names=[ID_COLUMN, TEXT_COLUMN])

Apply fuzzy keyword search to keyword of choice and extract the best matches
----------------------------------------------------------------------------

-  Adjust ``keyword_dict``
-  Adjust ``threshold``: minimum similarity score
-  Adjust ``context_words``: number of words extracted to contextualise
   keyword

Note: To apply the fuzzy search to multiple keywords at once,
``contextual_fuzzy_search_parallelised.py`` can be run. Only adjust the
file paths and variables in lines 13 to 22. The corresponding dictionary
is ``keyword_dict_fuzzy`` and can easily be adapted if necessary.

.. code:: ipython3

    with open('keyword_dict_hochwasser.json') as f:
        HOCHWASSER_KEYWORDS = json.load(f)
    
    THRESHOLD=85
    CONTEXT_WORDS=15

.. code:: ipython3

    all_matches = search_best_matches_dict(input_df=input_df,
                                             id_column_name=ID_COLUMN,
                                             text_column_name=TEXT_COLUMN,
                                             keyword_dict=HOCHWASSER_KEYWORDS,
                                             threshold=THRESHOLD,
                                             context_words=CONTEXT_WORDS)

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
          <th>contextualised_keyword</th>
          <th>actual_keyword</th>
          <th>category</th>
          <th>filename</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>wasserhaushalt gebotene sparsame verwendung des wassers zu erreichen. § 51 a lwg legt fest, dass niederschlagswasser von grundstücken, die nach dem 01.01.1996 erstmals bebaut, befestigt oder an die öffentliche kanalisation angeschlossen ;;; der flächenversiegelung in größerem umfang. da bodenversiegelung und die befestigung von boden die infiltration von niederschlagswasser in den boden und somit eine anreicherung des grundwassers verhindert, wird die grund wasserdargebots und</td>
          <td>niederschlagswasser</td>
          <td>betroffen_von_überschwemmung</td>
          <td>116995_8.pdf</td>
        </tr>
        <tr>
          <th>1</th>
          <td>sie auch als besonders schutzwürdigen böden in der bodenkarte nrw ausgewiesen. für eine versickerung von niederschlagswasser sind die anstehenden böden nur bedingt geeignet. die böden der bördelandschaft sind relativ anfällig für ;;; dass die anstehenden böden nur eine bedingte eignung dafür haben. im plangebiet werden voraussichtlich die niederschlagswässer der verkehrsflächen an die öffentliche kanalisation angeschlossen. es ist zu prüfen, ob unbelastetes oberflächen wasser ;;; emissionen sowie der sachgerechte umgang mit abfällen und abwässern" ➡ die handhabung mit den anfallenden niederschlagswässern wird im weiteren verfahren geklärt. ➡ entsorgung der schmutzwässer über kanalnetz. ➡ nutzung von signalhorn</td>
          <td>niederschlagswasser</td>
          <td>betroffen_von_überschwemmung</td>
          <td>1691739_2.pdf</td>
        </tr>
        <tr>
          <th>2</th>
          <td>den grundwas serschutz ist eine gewisse beeinträchtigung gegeben, da durch die versiegelung im plange biet niederschlagswasser nicht mehr ungehindert versickern und zur grundwasseranreiche rung beitragen kann. allerdings wäscht der niederschlag die ;;; hinblick auf den grundwasserschutz eine gewisse schutzwirkung gegeben, da durch die ausbleibende versiegelung im plangebiet niederschlagswasser versickern und zur grundwasseranreicherung beitragen kann. planung: durch die umsetzung der planung wird zusätzlicher boden ;;; umsetzung der planung wird zusätzlicher boden versiegelt, was auswirkungen auf die grundwasserneubildung hat, da das niederschlagswasser im plangebiet nicht mehr umweltbericht flächennutzungsplanänderung nr. 5 feuerwehrgerätehaus giesendorf 17 ungehindert versickern kann. allerdings ;;; 5 feuerwehrgerätehaus giesendorf 17 ungehindert versickern kann. allerdings ist gemäß § 51a lwg nw das niederschlagswasser von grundstücken, die nach dem 1. januar 1996 erstmals bebau...</td>
          <td>niederschlagswasser</td>
          <td>betroffen_von_überschwemmung</td>
          <td>1691740_2.pdf</td>
        </tr>
        <tr>
          <th>3</th>
          <td>hinblick auf den grundwasserschutz eine gewisse schutzwirkung gegeben, da durch die ausbleibende versiegelung im plangebiet niederschlagswasser versickern und zur grundwasseranreicherung beitragen kann. aller dings wäscht der niederschlag die durch düngung bedingten ;;; umsetzung der planung wird zusätzlicher boden versiegelt, was auswirkungen auf die grundwasserneubildung hat, da das niederschlagswasser im plangebiet nicht mehr ungehindert versickern kann. allerdings ist gemäß § 51a lwg nw das ;;; im plangebiet nicht mehr ungehindert versickern kann. allerdings ist gemäß § 51a lwg nw das niederschlagswasser von grundstücken, die nach dem 1. januar 1996 erstmals bebaut, befestigt oder an die öffentliche ;;; der allgemeinheit möglich ist. aufgrund der gesetzgebung ist sichergestellt, dass zumindest ein beachtlicher anteil des niederschlagswassers dem natürlichen wasserhaushalt wieder zugeführt wird und so der grundwasserneubildung dient. infolgedessen ergeben sich in</td>
          <td>niederschlagswasser</td>
          <td>betroffen_von_überschwemmung</td>
          <td>1691744_1.pdf</td>
        </tr>
        <tr>
          <th>4</th>
          <td>bestehende mischwasserkanalisation. aufgrund der nur geringfügig erhöhten abwassermenge ist die vorhandene entwässerungsinfrastruktur ausreichend. das unverschmutzte niederschlagswasser kann grundsätzlich in zisternen aufgefan gen werden und als brauchwasser zur toilettenspülung, gartenbewässerung o.ä. verwendung</td>
          <td>niederschlagswasser</td>
          <td>betroffen_von_überschwemmung</td>
          <td>1691766_1.pdf</td>
        </tr>
        <tr>
          <th>5</th>
          <td>bestehende mischwasserkanalisation. aufgrund der nur geringfügig erhöhten abwassermenge ist die vorhandene entwässerungsinfrastruktur ausreichend. das unverschmutzte niederschlagswasser kann grundsätzlich in zisternen aufgefan gen werden und als brauchwasser zur toilettenspülung, gartenbewässerung o.ä. verwendung</td>
          <td>niederschlagswasser</td>
          <td>betroffen_von_überschwemmung</td>
          <td>1691842_1.pdf</td>
        </tr>
        <tr>
          <th>6</th>
          <td>möglichkeiten der entwicklung der gemeinde insbesondere durch wiedernutzbarmachung von flächen, nachverdichtung und andere maßnahmen zur innenentwicklung zu nutzen (§1a abs.2). bundesnaturschutzgesetz (bnatschg) / landschaftsgesetz nw (lg nw) das bundesnaturschutzgesetz (bnatschg) schreibt</td>
          <td>innenentwicklung</td>
          <td>innenentwicklung</td>
          <td>116995_8.pdf</td>
        </tr>
        <tr>
          <th>7</th>
          <td>möglichkeiten der entwicklung der gemeinde insbesondere durch wiedernutzbarmachung von flächen, nachverdichtung und andere maßnahmen zur innenentwicklung zu nutzen sowie bodenversiegelungen auf das notwendige maß zu begrenzen. die notwendigkeit der umwandlung landwirtschaftlich ;;; oder als wald genutzter flächen soll begründet werden; dabei sollen ermittlungen zu den möglichkeiten der innenentwicklung zugrunde gelegt werden, zu denen insbesondere brachflächen, gebäudeleerstand, baulücken und andere nachverdichtungsmöglichkeiten zählen können. begründung</td>
          <td>innenentwicklung</td>
          <td>innenentwicklung</td>
          <td>1691739_1.pdf</td>
        </tr>
        <tr>
          <th>8</th>
          <td>sparsamer und schonender umgang mit grund und boden durch wiedernutz barmachung von flächen, nachverdichtung und innenentwick lung zur verringerung zusätzlicher inanspruchnahme von bö den  landwirtschaftlich, als wald oder für wohnungszwecke</td>
          <td>innenentwicklung</td>
          <td>innenentwicklung</td>
          <td>1691740_2.pdf</td>
        </tr>
        <tr>
          <th>9</th>
          <td>sparsamer und schonender umgang mit grund und boden durch wiedernutz barmachung von flächen, nachverdichtung und innenentwick lung zur verringerung zusätzlicher inanspruchnahme von bö den  landwirtschaftlich, als wald oder für wohnungszwecke</td>
          <td>innenentwicklung</td>
          <td>innenentwicklung</td>
          <td>1691744_1.pdf</td>
        </tr>
        <tr>
          <th>10</th>
          <td>möglichkeiten der entwicklung der gemeinde insbesondere durch wiedernutzbarmachung von flächen, nachverdichtung und andere maßnahmen zur innenentwicklung zu nutzen sowie bodenversiegelungen auf das notwendige maß zu begrenzen. die notwendigkeit der umwandlung landwirtschaftlich ;;; oder als wald genutzter flächen soll begründet werden; dabei sollen ermittlungen zu den möglichkeiten der innenentwicklung zugrunde gelegt werden, zu denen insbesondere brachflächen, gebäudeleerstand, baulücken und andere nachverdichtungsmöglichkeiten zählen können. diesbezüglich ;;; die sonderregeln des § 246 abs. 10 baugb ( sonderreglung für flüchtlingsunterkünfte) nicht geeignet eine innenentwicklung umzusetzen, da die sonderregelung lediglich befristet bis zum 31.12.2019 in kraft ist, die stadt elsdorf ;;; im hinblick auf eine mögliche errichtung von flüchtlingsunterkünften untersucht worden. standorte im innenbereich, die einer innenentwicklung.im sinne des o.g. gesetzes darstellen, stehen aufgrund ...</td>
          <td>innenentwicklung</td>
          <td>innenentwicklung</td>
          <td>1691744_2.pdf</td>
        </tr>
        <tr>
          <th>11</th>
          <td>voll umfänglich im beplanten innenbereich gem. § 34 baugb. die beabsichtigte städtebauliche zielsetzung dient der innenentwicklung i.s.d. § 1a abs. 2 baugb. stadt elsdorf, bebauungsplan nr. 75 „niederembt, embestraße“, 1. änderung</td>
          <td>innenentwicklung</td>
          <td>innenentwicklung</td>
          <td>1691766_1.pdf</td>
        </tr>
        <tr>
          <th>12</th>
          <td>aus der deutschen grundkarte mit geltungsbereich unter abschnitt 2). die beabsichtigte städtebauliche zielsetzung dient der innenentwicklung i.s.d. § 1a abs. 2 baugb. die beabsichtigte bebauungsplanung entspricht der geordneten städtebauli chen entwicklung</td>
          <td>innenentwicklung</td>
          <td>innenentwicklung</td>
          <td>1691842_1.pdf</td>
        </tr>
      </tbody>
    </table>
    </div>



Write results to csv and json
=============================

.. code:: ipython3

    # write to csv
    all_matches.to_csv(os.path.join(OUTPUT_FILE_PATH + ".csv"), header=True, index=False)
    
    # write to json
    all_matches_json = all_matches.to_json(orient='records')
    with open(OUTPUT_FILE_PATH + ".json", 'w') as outputfile:
        outputfile.write(all_matches_json)
