.. figure:: assets/dssg_banner.png
   :alt: dssg_banner

.. code:: ipython3

    import os
    
    from data_pipeline.pdf_scraper.tika_pdf_scraper import pdf_parser_from_folder

Illustration of usage of pdf_scraper.py
=======================================

This pdf scraper assumes to-be-scraped documents to be present in a
subfolder in the same project (here: ``../data/nrw/bplan/raw/pdfs``).
Due to storage constraints, the pdfs have however not been uploaded to
this Github repository. Make sure to provide files before running the
code. While Apache tika (the API used for Optical Character Recognition)
technically allows scraping based on URLs too, here, the pdfs were
further processed too (e.g., image extraction) and download necessary
anyways. Therefore, the pdf scraper expects a folder containing the
files (in .pdf or .png format) as input.

To use the pdf scraper: - **Install Java** (we originally used version
20.0.2, `download
here <https://www.oracle.com/java/technologies/downloads/>`__) -
**Adjust the data input and data output in code block 1**: Specify a
functioning file path leading to a folder containing pdf/png documents -
**Adjust the optional sample_size parameter in code block 2**: Specify
the desired sample size or leave empty to consider all.

.. code:: ipython3

    # code block 1: specify data inputs and outputs
    INPUT_FOLDER_PATH = os.path.join("..", "data", "nrw", "bplan", "raw", "pdfs")
    OUTPUT_FILENAME_CSV = os.path.join("..", "data", "nrw", "bplan", "raw", "text", "bp_text.csv")
    OUTPUT_FILENAME_JSON = os.path.join("..", "data", "nrw", "bplan", "raw", "text", "bp_text.json")

Parse PDFs from folder
----------------------

.. code:: ipython3

    # code block 2: apply pdf_parser function to folder containing pdfs
    parsed_df = pdf_parser_from_folder(folder_path=INPUT_FOLDER_PATH,
                                       sample_size=3)


.. parsed-literal::

    2023-09-18 17:03:49.502 | INFO     | data_pipeline.pdf_scraper.tika_pdf_scraper:pdf_parser_from_folder:64 - Parsing file: 2368027_8.pdf
    2023-09-18 17:03:50,775 [MainThread  ] [WARNI]  Failed to see startup log message; retrying...
    2023-09-18 17:04:04.482 | INFO     | data_pipeline.pdf_scraper.tika_pdf_scraper:pdf_parser_from_folder:64 - Parsing file: 2368027_6.pdf
    2023-09-18 17:04:04.867 | INFO     | data_pipeline.pdf_scraper.tika_pdf_scraper:pdf_parser_from_folder:64 - Parsing file: 2220502_14.pdf
    2023-09-18 17:04:04.957 | INFO     | data_pipeline.pdf_scraper.tika_pdf_scraper:pdf_parser_from_folder:75 - Parsing done.


.. code:: ipython3

    # code block 3: check results
    parsed_df.head()




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
          <th>content</th>
          <th>metadata</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2368027_8.pdf</td>
          <td>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n...</td>
          <td>{'pdf:PDFVersion': '1.6', 'xmp:CreatorTool': '...</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2368027_6.pdf</td>
          <td>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n...</td>
          <td>{'pdf:PDFVersion': '1.6', 'xmp:CreatorTool': '...</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2220502_14.pdf</td>
          <td>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n...</td>
          <td>{'pdf:unmappedUnicodeCharsPerPage': ['0', '0']...</td>
        </tr>
      </tbody>
    </table>
    </div>



Write results to CSV and json
-----------------------------

.. code:: ipython3

    # code block 4:
    # write results to csv
    parsed_df.to_csv(OUTPUT_FILENAME_CSV, header=True, index=False)
    
    # write results to json
    result_json = parsed_df.to_json(orient='records')
    
    with open(OUTPUT_FILENAME_JSON, 'w') as outputfile:
        outputfile.write(result_json)
