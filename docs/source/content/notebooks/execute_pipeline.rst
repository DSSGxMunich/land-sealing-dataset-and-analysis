Execute Pipeline Notebook
============================

.. code:: ipython3

    import os
    
    from data_pipeline.nrw_pdf_downloader.geojson_parser import parse_geojson
    from data_pipeline.nrw_pdf_downloader.nrw_pdf_scraper import run_pdf_downloader
    from data_pipeline.match_RPlan_BPlan.matching_plans import merge_RP_BP
    from data_pipeline.match_RPlan_BPlan.matching_plans import export_merged_BP_RP

.. code:: ipython3

    INPUT_BP_FILE_PATH = os.path.join("..", "data","nrw","NRW_BP.geojson")
    OUTPUT_PDF_FOLDER_PATH = os.path.join( "..", "data", "nrw", "pdfs")
    OUTPUT_CSV_PATH = os.path.join( "..", "data", "nrw", "sample_pdf.csv")
    OUTPUT_LAND_PARCELS_PATH = os.path.join("..", "data","nrw","land_parcels.geojson")
    INPUT_REGIONS_FILE_PATH = os.path.join( "..", "data","nrw","regions_map.geojson")

.. code:: ipython3

    df = parse_geojson(INPUT_BP_FILE_PATH, sample_n = 5, output_path = OUTPUT_CSV_PATH)


.. parsed-literal::

    100%|██████████| 5/5 [00:00<00:00,  8.54it/s]


.. code:: ipython3

    # Run downloader
    run_pdf_downloader(df,
                       output_folder=OUTPUT_PDF_FOLDER_PATH,
                       sample_n=3)


.. parsed-literal::

      0%|          | 0/3 [00:00<?, ?it/s]100%|██████████| 3/3 [00:01<00:00,  1.82it/s]


.. code:: ipython3

    land_parcels = merge_RP_BP(INPUT_BP_FILE_PATH, INPUT_REGIONS_FILE_PATH)

.. code:: ipython3

    land_parcels.head()




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
          <th>objectid</th>
          <th>geometry</th>
          <th>planid</th>
          <th>levelplan</th>
          <th>name</th>
          <th>kommune</th>
          <th>gkz</th>
          <th>nr</th>
          <th>besch</th>
          <th>aend</th>
          <th>...</th>
          <th>aendnr</th>
          <th>begruendurl</th>
          <th>umweltberurl</th>
          <th>erklaerungurl</th>
          <th>shape_Length</th>
          <th>shape_Area</th>
          <th>regional_plan_id</th>
          <th>regional_plan_name</th>
          <th>ART</th>
          <th>LND</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>84060</td>
          <td>POLYGON ((7.28543 50.82280, 7.28728 50.82179, ...</td>
          <td>DE_05382060_Siegburg_BP93/1</td>
          <td>infra-local</td>
          <td>Im Klausgarten, Braschosser Straße, Am Kreuztor</td>
          <td>Siegburg</td>
          <td>05382060</td>
          <td>93/1</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>868.647801</td>
          <td>3.196032e+04</td>
          <td>5022</td>
          <td>Region Bonn/Rhein-Sieg</td>
          <td>Teilabschnitt</td>
          <td>5</td>
        </tr>
        <tr>
          <th>126</th>
          <td>559438</td>
          <td>POLYGON ((7.39385 50.90281, 7.39416 50.90240, ...</td>
          <td>DE_05382036_02_32</td>
          <td>infra-local</td>
          <td>32. Änderung des Bebauungsplanes Nr. 2 „Much-K...</td>
          <td>Much</td>
          <td>05382036</td>
          <td>0</td>
          <td>None</td>
          <td>32.  Änderung</td>
          <td>...</td>
          <td>32</td>
          <td>https://www.much.de/zukunft/bauleitplanungen</td>
          <td>https://www.much.de/zukunft/bauleitplanungen</td>
          <td>None</td>
          <td>473.229327</td>
          <td>4.467916e+03</td>
          <td>5022</td>
          <td>Region Bonn/Rhein-Sieg</td>
          <td>Teilabschnitt</td>
          <td>5</td>
        </tr>
        <tr>
          <th>2722</th>
          <td>2257588</td>
          <td>POLYGON ((7.12896 50.77292, 7.12899 50.77292, ...</td>
          <td>DE_05314000_00</td>
          <td>local</td>
          <td>Flächennutzungsplan der Bundesstadt Bonn</td>
          <td>Bonn</td>
          <td>05314000</td>
          <td>00</td>
          <td></td>
          <td></td>
          <td>...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>69372.039264</td>
          <td>1.410146e+08</td>
          <td>5022</td>
          <td>Region Bonn/Rhein-Sieg</td>
          <td>Teilabschnitt</td>
          <td>5</td>
        </tr>
        <tr>
          <th>3436</th>
          <td>2367967</td>
          <td>MULTIPOLYGON (((7.23255 50.91855, 7.23242 50.9...</td>
          <td>DE_05378028_9aenderungI_Ur</td>
          <td>local</td>
          <td>9. Änderung §34_Urschrift</td>
          <td>Rösrath</td>
          <td>05378028</td>
          <td>9aenderungI_Ur</td>
          <td>Breide und Durbusch</td>
          <td>Urschrift</td>
          <td>...</td>
          <td>None</td>
          <td>http://www.roesrath.de/34-9.-aenderung-breide-...</td>
          <td></td>
          <td></td>
          <td>739.659941</td>
          <td>7.348491e+03</td>
          <td>5022</td>
          <td>Region Bonn/Rhein-Sieg</td>
          <td>Teilabschnitt</td>
          <td>5</td>
        </tr>
        <tr>
          <th>3444</th>
          <td>2367975</td>
          <td>MULTIPOLYGON (((7.19091 50.88535, 7.19112 50.8...</td>
          <td>DE_05378028_1aenderungundUrschriftI_Ur</td>
          <td>local</td>
          <td>1. Änderung und Urschrift §34_Urschrift</td>
          <td>Rösrath</td>
          <td>05378028</td>
          <td>1aenderungundUrschriftI_Ur</td>
          <td></td>
          <td>Urschrift</td>
          <td>...</td>
          <td>None</td>
          <td>http://www.roesrath.de/34-urfassung-und-1.-aen...</td>
          <td></td>
          <td></td>
          <td>56630.267941</td>
          <td>6.082747e+06</td>
          <td>5022</td>
          <td>Region Bonn/Rhein-Sieg</td>
          <td>Teilabschnitt</td>
          <td>5</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 30 columns</p>
    </div>



File can be exported with the function export_merged_BP_RP() (runs the
same as merge_RP_BP, but have to add output_path parameter) in the
module, or by using *to_file* from the geopandas module. We will do a
run of the export function.

.. code:: ipython3

    export_merged_BP_RP(OUTPUT_LAND_PARCELS_PATH, INPUT_BP_FILE_PATH, INPUT_REGIONS_FILE_PATH)
