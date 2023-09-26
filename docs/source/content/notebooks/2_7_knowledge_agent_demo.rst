.. figure:: assets/dssg_banner.png
   :alt: dssg_banner


.. code:: ipython3

    import chardet
    import openai
    import os
    import pandas as pd
    import numpy as np
    
    from features.textual_features.knowledge_extraction_agent.agentic_knowledge_extractor import extract_knowledge_from_df
    from dotenv import load_dotenv
    
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

Agentic knowledge extractor
===========================

This notebook uses a Large Language Model (LLM) as an agent in order to
extract knowledge from text input. The text input are the results from
the fuzzy search, which returns the keyword found embedded in its
context (words before and after the keyword). In fact, we are not
interested in the keyword itself, but in its actual value. For example,
the keyword may be “Firsthöhe” (= ridge height), so we’d like to find
out the actual height.

Get API key
-----------

To be able to use the GPT API, add a file to the project root directory
titled ``.env`` and add your API key to it: ``OPENAI_API_KEY=[KEY]``

.. code:: ipython3

    load_dotenv()
    openai.api_key=os.getenv('OPENAI_API_KEY')

Set variables
-------------

.. code:: ipython3

    INPUT_FOLDER_PATH = "../data/nrw/bplan/features/keywords/fuzzy_search/traufhöhe.csv"
    ID_COLUMN='filename'
    TEXT_COLUMN='content'

Note that ``nrows=10`` to avoid accidentally spending large amounts.
Remove the argument for a complete run.

.. code:: ipython3

    with open(INPUT_FOLDER_PATH, 'rb') as f:
        enc = chardet.detect(f.read())
    
    input_df = pd.read_csv(INPUT_FOLDER_PATH,
                           names=[ID_COLUMN, TEXT_COLUMN],
                           encoding = enc['encoding'],
                           header=None,
                           nrows=10)

Specify keyword dictionary
--------------------------

Change the keyword *values* (on the right hand side), if necessary.

.. code:: ipython3

    keyword_dict = {
        'keyword':          'traufhöhe',
        'keyword_short':    'th',
        'template_name':    'features/textual_features/knowledge_extraction_agent/prompt_templates/knowledge_extraction_th.template',
        'filename':         'traufhöhe.csv'
        }

Note that an AuthenticationError is liklez caused bz a problem with your
openAI API key.

.. code:: ipython3

    all_responses = extract_knowledge_from_df(keyword_dict=keyword_dict,
                                              input_df=input_df,
                                              id_column_name=ID_COLUMN,
                                              text_column_name=TEXT_COLUMN)


.. parsed-literal::

    [32m2023-09-21 12:45:12.505[0m | [1mINFO    [0m | [36mfeatures.textual_features.knowledge_extraction_agent.agentic_knowledge_extractor[0m:[36mextract_knowledge_from_df[0m:[36m198[0m - [1mRelevant keyword(s): traufhöhe[0m
    [32m2023-09-21 12:45:12.507[0m | [1mINFO    [0m | [36mfeatures.textual_features.knowledge_extraction_agent.agentic_knowledge_extractor[0m:[36mextract_knowledge_from_df[0m:[36m199[0m - [1mExtracting relevant info from text snippets via LLM agent.[0m
    [32m2023-09-21 12:45:19.575[0m | [1mINFO    [0m | [36mfeatures.textual_features.knowledge_extraction_agent.agentic_knowledge_extractor[0m:[36mextract_knowledge_from_df[0m:[36m217[0m - [1mInfo extracted. Extracting numerical value from info.[0m
    [32m2023-09-21 12:45:19.576[0m | [1mINFO    [0m | [36mfeatures.textual_features.knowledge_extraction_agent.agentic_knowledge_extractor[0m:[36mextract_knowledge_from_df[0m:[36m223[0m - [1mNumerical values extracted. Validating their occurrence in input text.[0m
    [32m2023-09-21 12:45:19.578[0m | [1mINFO    [0m | [36mfeatures.textual_features.knowledge_extraction_agent.agentic_knowledge_extractor[0m:[36mextract_knowledge_from_df[0m:[36m232[0m - [1mReturning results for th.[0m


.. code:: ipython3

    all_responses.head(10)




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
          <th>id</th>
          <th>th_input</th>
          <th>th_agent_response</th>
          <th>th_extracted_value</th>
          <th>validation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>id</td>
          <td>traufhöhe</td>
          <td>None</td>
          <td>NaN</td>
          <td>True</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1956227.pdf</td>
          <td>/ fh 9,5 m bei gebäuden mit zwei vollgeschossen: th 6,5 m / fh 8,5 m bestimmung der traufhöhe: die traufhöhe wird durch den äußeren schnittpunkt des aufgehenden mauerwerks mit der dachhaut gebildet. bestimmung der firsthöhe: die firsthöhe wird durch den ;;; grz 0,3 grundflächenzahl ii zahl der vollgeschosse als höchstmaß 2 wo höchstzulässige zahl der wohnungen in wohngebäuden th 00,0 m traufhöhe als höchstmaß fh 00,0 m firsthöhe als höchstmaß 00,00 m unterer bezugspunkt zur bemessung der trauf und firsthöhen bauweise, baulinien, ;;; 4,3 m / fh 9,5 m bei gebäuden mit zwei vollgeschossen: th 6,5 m / fh 8,5 m bestimmung der traufhöhe: die traufhöhe wird durch den äußeren schnittpunkt des aufgehenden mauerwerks mit der dachhaut gebildet. bestimmung der firsthöhe: die firsthöhe wird</td>
          <td>th: 6,5 m</td>
          <td>6.50</td>
          <td>True</td>
        </tr>
        <tr>
          <th>2</th>
          <td>1956230.pdf</td>
          <td>anderes material zulässig. 2 dächer zulässig sind satteldächer mit einer neigung von 30° 40°. bei aneinandergebauten gebäuden sind dachneigung und traufhöhe einander anzupassen. dachaufbauten (gauben) dürfen 1/2 der gesamtdachlänge nicht überschreiten die traufe der gaube darf nicht höher als 1,20 m</td>
          <td>None</td>
          <td>NaN</td>
          <td>True</td>
        </tr>
        <tr>
          <th>3</th>
          <td>2112722.pdf</td>
          <td>zulhsige grundflächenzahl (grz) (gern.§ 16 (2) nr.1 baunvo) offene bauweise (gern.§ 9 (1) nr. 2 baugb und§ 22 baunvo) ma,c. traufllöhe (gern.§ 9 (1) nr. 1 baugb u. § 16 (2) nr. 4 baunvo) m;1x. firsthöhe (gern.§ 9 (1) nr. 1</td>
          <td>None</td>
          <td>NaN</td>
          <td>True</td>
        </tr>
        <tr>
          <th>4</th>
          <td>2112808.pdf</td>
          <td>der außenflächen der außenwand mit der dachhaut. untergeordnete bauteile (vorbauten, erker, zwerchgiebel) dürfen auf maximal 1/3 der baukörperlänge die maximale traufhöhe überschreiten. die maximal zulässige firsthöhe wird am fertiggestellten gebäude am schnittpunkt der außenflächen der dachhaut gemessen. maximal zulässige traufhöhe in ;;; maximale traufhöhe überschreiten. die maximal zulässige firsthöhe wird am fertiggestellten gebäude am schnittpunkt der außenflächen der dachhaut gemessen. maximal zulässige traufhöhe in metern th 5,00m auf flächen gem. § 9 (1) ziffer 25a baugb sind heimische sträucherund heister der qualität str.</td>
          <td>th: 5,00 m</td>
          <td>5.00</td>
          <td>True</td>
        </tr>
        <tr>
          <th>5</th>
          <td>2220395_4.pdf</td>
          <td>der bebauungsplan den festsetzungen des ehemaligen bebauungsplanes nr. 5 und entspricht ebenso der derzeitigen bestandssituation. 7.4 höhe baulicher anlagen die traufhöhe für das eingeschossige gebäude wird mit maximal 4,75 m über der an grenzenden vorhandenen erschließungsstraße festgesetzt. damit wird gewährleistet, dass</td>
          <td>th: 4,75 m</td>
          <td>4.75</td>
          <td>True</td>
        </tr>
        <tr>
          <th>6</th>
          <td>2220407_6.pdf</td>
          <td>parallel zur öffentlichen verkehrsfläche auszubilden. form und höhe der vorhandenen attika zur öffentlichen verkehrsfläche sind beim satteldach zu übernehmen; die traufenhöhe wird auf 42.54 m ü. n.n. begrenzt. 3. auf den gebäudeschenkeln (anbauten) sind ausschließlich sattel und pultdächer zulässig. bei den ;;; und pultdächer zulässig. bei den pult und satteldächern sind form und höhe der vorhandenen attika entlang der grundstücksgrenzen einzuhalten. die traufenhöhe entlang der grundstücksgrenzen von anbauten wird auf 42.54 m ü. n.n. begrenzt. walm und krüppelwalmdächer sind ausgeschlossen. 4. dachüberstände sind</td>
          <td>None</td>
          <td>NaN</td>
          <td>True</td>
        </tr>
        <tr>
          <th>7</th>
          <td>2220409_1.pdf</td>
          <td>41,5 m über nhn festgesetzt, was einem maß von rund 9,50 m über dem ge ländeniveau entspricht. die maximal zulässige traufhöhe beträgt 38,5 m über nhn, was rund 6,50 m über dem geländeniveau entspricht. es ist eine maximale zweigeschossige bebauung festgesetzt</td>
          <td>th: 9,50 m\nth: 6,50 m\nNone</td>
          <td>9.50</td>
          <td>True</td>
        </tr>
        <tr>
          <th>8</th>
          <td>2220409_3.pdf</td>
          <td>passen sich an die umliegenden bestandsgebäude und ermöglichen eine flexib le anordnung und ausgestaltung neuer baukörper. zahl der vollgeschosse / traufhöhe (th) und firsthöhe (fh) für den gesamten geltungsbereich des vorhabenbezogenen bebauungsplans werden zwei vollgeschosse festgesetzt. die festsetzung leitet sich aus ;;; von 41,5 m über nhn festgesetzt, was einem maß von rund 9,50 m über dem geländeniveau entspricht. die maximal zulässige traufhöhe beträgt 38,5 m über nhn, was rund 6,50 m über dem geländeniveau entspricht. damit wird eine in hinblick auf die</td>
          <td>th: 6,50 m</td>
          <td>6.50</td>
          <td>True</td>
        </tr>
        <tr>
          <th>9</th>
          <td>2220438_2.pdf</td>
          <td>geschoßflächenzahl mass der baul. nutzungart der baul. nutzung flurstücksnummer flurstücksgrenze flurgrenze gewerbegebiete gemischte bauflächen ge 1,8 fh th grz firsthöhe traufhöhe bauweise, baugrenzen offene bauweise abweichende bauweisea o baugrenze straßenbegrenzungslinie straßenverkehrsfläche aufteilung als hinweis verkehrsflächen natur und landschaft plangebietsgrenze sonstige planzeichen ;;; mit rank , kletter oder schlingpflanzen vorzusehen. die pflanzung ist dauerhaft zu unterhalten. werbeanlagen sind nur an gebäudeteilen unterhalb der traufhöhe (auch an giebeln) zulässig. an einfriedungen und auf dachflächen sind sie nicht zulässig. je gewerbebetrieb ist die firmenbezeichnung als beleuchtete</td>
          <td>None</td>
          <td>NaN</td>
          <td>True</td>
        </tr>
      </tbody>
    </table>
    </div>



Reset if validation unsuccessful
--------------------------------

If validation wasn’t successful (= False), the extracted_value column
should be set back to NaN.

.. code:: ipython3

    column_name = f"{keyword_dict['keyword_short']}_extracted_value"
    all_responses.loc[all_responses['validation'] == False, column_name] = np.nan
    
    all_responses.head()




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
          <th>id</th>
          <th>th_input</th>
          <th>th_agent_response</th>
          <th>th_extracted_value</th>
          <th>validation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>id</td>
          <td>traufhöhe</td>
          <td>None</td>
          <td>NaN</td>
          <td>True</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1956227.pdf</td>
          <td>/ fh 9,5 m bei gebäuden mit zwei vollgeschossen: th 6,5 m / fh 8,5 m bestimmung der traufhöhe: die traufhöhe wird durch den äußeren schnittpunkt des aufgehenden mauerwerks mit der dachhaut gebildet. bestimmung der firsthöhe: die firsthöhe wird durch den ;;; grz 0,3 grundflächenzahl ii zahl der vollgeschosse als höchstmaß 2 wo höchstzulässige zahl der wohnungen in wohngebäuden th 00,0 m traufhöhe als höchstmaß fh 00,0 m firsthöhe als höchstmaß 00,00 m unterer bezugspunkt zur bemessung der trauf und firsthöhen bauweise, baulinien, ;;; 4,3 m / fh 9,5 m bei gebäuden mit zwei vollgeschossen: th 6,5 m / fh 8,5 m bestimmung der traufhöhe: die traufhöhe wird durch den äußeren schnittpunkt des aufgehenden mauerwerks mit der dachhaut gebildet. bestimmung der firsthöhe: die firsthöhe wird</td>
          <td>th: 6,5 m</td>
          <td>6.5</td>
          <td>True</td>
        </tr>
        <tr>
          <th>2</th>
          <td>1956230.pdf</td>
          <td>anderes material zulässig. 2 dächer zulässig sind satteldächer mit einer neigung von 30° 40°. bei aneinandergebauten gebäuden sind dachneigung und traufhöhe einander anzupassen. dachaufbauten (gauben) dürfen 1/2 der gesamtdachlänge nicht überschreiten die traufe der gaube darf nicht höher als 1,20 m</td>
          <td>None</td>
          <td>NaN</td>
          <td>True</td>
        </tr>
        <tr>
          <th>3</th>
          <td>2112722.pdf</td>
          <td>zulhsige grundflächenzahl (grz) (gern.§ 16 (2) nr.1 baunvo) offene bauweise (gern.§ 9 (1) nr. 2 baugb und§ 22 baunvo) ma,c. traufllöhe (gern.§ 9 (1) nr. 1 baugb u. § 16 (2) nr. 4 baunvo) m;1x. firsthöhe (gern.§ 9 (1) nr. 1</td>
          <td>None</td>
          <td>NaN</td>
          <td>True</td>
        </tr>
        <tr>
          <th>4</th>
          <td>2112808.pdf</td>
          <td>der außenflächen der außenwand mit der dachhaut. untergeordnete bauteile (vorbauten, erker, zwerchgiebel) dürfen auf maximal 1/3 der baukörperlänge die maximale traufhöhe überschreiten. die maximal zulässige firsthöhe wird am fertiggestellten gebäude am schnittpunkt der außenflächen der dachhaut gemessen. maximal zulässige traufhöhe in ;;; maximale traufhöhe überschreiten. die maximal zulässige firsthöhe wird am fertiggestellten gebäude am schnittpunkt der außenflächen der dachhaut gemessen. maximal zulässige traufhöhe in metern th 5,00m auf flächen gem. § 9 (1) ziffer 25a baugb sind heimische sträucherund heister der qualität str.</td>
          <td>th: 5,00 m</td>
          <td>5.0</td>
          <td>True</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    all_responses.to_json('../data/nrw/bplan/knowledge_agent_output.json')
