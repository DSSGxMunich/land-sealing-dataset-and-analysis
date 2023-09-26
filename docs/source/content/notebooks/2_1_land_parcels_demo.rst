.. figure:: assets/dssg_banner.png
   :alt: dssg_banner


.. code:: ipython3

    import os
    
    from data_pipeline.nrw_pdf_downloader.geojson_parser import parse_geojson
    from data_pipeline.nrw_pdf_downloader.nrw_pdf_scraper import run_pdf_downloader
    from data_pipeline.match_RPlan_BPlan.matching_plans import merge_rp_bp
    from data_pipeline.match_RPlan_BPlan.matching_plans import export_merged_bp_rp

Get started: PDF downloader for land parcels of Bebauungspläne
==============================================================

The first step necessary to run the BP downloader is to have a database
that contains links to different building plans in PDF format. The input
for this was the information provided in the `NRW
geoportal <https://www.geoportal.nrw/?activetab=map>`__. Clicking on the
download button there, you should be able to select all the areas of
NRW, select to download information from Bebauungsplane and get the
information in GeoPackage format (gpkg extension).

This extension can be loaded into any GIS interface, and exported into a
geojson format. This is the format that the functions finally take as
input.

-  ``parse_geojson:`` parses geojson file with download links to
   different building plans. It iterates over all rows and checks if the
   url matches the pattern of a osp-plan.de link without a list format,
   meaning than the scan url is not directly to a pdf, but the pdf is
   contained somewhere in the html of the page. If the url matches the
   pattern, the html of the page is downloaded and parsed with beautiful
   soup. All links that start with https://www.o-sp.de/download/ are
   extracted and written to a dataframe.

   -  to parse only a sample of the rows, set a sample size defined by
      sample_n.

   :math:`~`

-  ``run_pdf_downloader:`` goes through a GDF with PDF download links
   and downloads all the files. Links that return error are saved in a
   csv called error_links in the defined output folder.

   -  to parse only a sample of the rows, set a sample size defined by
      sample_n. 

Necessary file path specifications:
-----------------------------------

.. code:: ipython3

    INPUT_BP_FILE_PATH = os.path.join("..", "data","nrw", "bplan", "raw", "links", "NRW_BP.geojson")
    OUTPUT_PDF_FOLDER_PATH = os.path.join("..", "data", "nrw", "bplan", "raw", "pdfs")
    OUTPUT_CSV_PATH = os.path.join("..", "data", "nrw", "bplan", "raw", "links", "NRW_BP_parsed_links.csv")
    OUTPUT_LAND_PARCELS_PATH = os.path.join("..", "data", "nrw", "bplan", "raw", "links", "land_parcels.geojson")
    INPUT_REGIONS_FILE_PATH = os.path.join( "..", "data","nrw", "rplan", "raw", "geo", "regions_map.geojson")

Now, let’s start the process:
-----------------------------

.. code:: ipython3

    df = parse_geojson(file_path=INPUT_BP_FILE_PATH,
                       sample_n = 5,
                       output_path = OUTPUT_CSV_PATH)


.. parsed-literal::

    100%|██████████| 5/5 [00:00<00:00,  8.54it/s]


Run the downloader and save the pdfs in output folder:
------------------------------------------------------

.. code:: ipython3

    run_pdf_downloader(input_df=df,
                       output_folder=OUTPUT_PDF_FOLDER_PATH,
                       sample_n=3)


.. parsed-literal::

      0%|          | 0/3 [00:00<?, ?it/s]100%|██████████| 3/3 [00:01<00:00,  1.82it/s]


Enrich bplan info to create ``land_parcels.csv``
------------------------------------------------

To generate the file ``land_parcels.csv`` we need the columns from the
original NRW_BP but we also need to add the columns that refer to the
regional plans that match each parcel. For that, we will use the
function merge_rp_bp stored in the module
match_rplan_bplan.matching_plans. It takes as input the same
``INPUT_BP_FILE_PATH`` we were working with, but also the file that
contains geodata of the regions (provided by GreenDIA).

.. code:: ipython3

    land_parcels = merge_rp_bp(path_bp_geo=INPUT_BP_FILE_PATH,
                               path_rp_geo=INPUT_REGIONS_FILE_PATH)

The result is a dataframe that contains all the original columns from
the BP dataset and the columns from the regions. The *relevant* columns
in this dataset are:

-  **objectid:** unique numeric ID of the building plan.
-  **geometry:** contains the spatial information of the polygons.
-  **kommune:** name of the municipality.
-  **name:** name of the building plan.
-  **datum:** date of the building plan.
-  **regional_plan_id:** unique numeric ID of the regional plan.
-  **regional_plan_name:** nominal name of the regional plan.

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

    export_merged_bp_rp(output_path=OUTPUT_LAND_PARCELS_PATH,
                        path_bp_geo=INPUT_BP_FILE_PATH,
                        path_rp_geo=INPUT_REGIONS_FILE_PATH)
                    
