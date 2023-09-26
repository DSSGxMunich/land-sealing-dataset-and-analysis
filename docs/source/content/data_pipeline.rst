Data Pipeline
-----------------

This is the documentation for the data_pipeline to download, extract, and transform the building plans and regional
plans. It contains the definitions for all methods necessary to run the pipeline.

Download NRW building plan PDFs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The methods used here are demonstrated in the `land_parcels_demo.ipynb` notebook.

.. autofunction:: src.data_pipeline.nrw_pdf_downloader.geojson_parser.parse_geojson

.. autofunction:: src.data_pipeline.nrw_pdf_downloader.nrw_pdf_scraper.run_pdf_downloader

.. autofunction:: src.data_pipeline.match_RPlan_BPlan.matching_plans.merge_rp_bp

.. autofunction:: src.data_pipeline.match_RPlan_BPlan.matching_plans.export_merged_bp_rp


Extract Text from PDFs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.data_pipeline.pdf_scraper.tika_pdf_scraper.pdf_parser_from_folder

.. autofunction:: src.data_pipeline.pdf_scraper.tika_pdf_scraper.pdf_parser_from_path


Parsing the regional plans
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The RPlan Converter is used to extract the content from the regional plan PDFs.

.. autoclass:: src.data_pipeline.rplan_content_extraction.rplan_content_extractor.RPlanContentExtractor
    :members:
    :undoc-members:
    :show-inheritance:

It utilizes the following methods:

.. autofunction:: src.data_pipeline.rplan_content_extraction.rplan_content_extractor.parse_rplan_directory

.. autofunction:: src.data_pipeline.rplan_content_extraction.rplan_utils.parse_result_df

