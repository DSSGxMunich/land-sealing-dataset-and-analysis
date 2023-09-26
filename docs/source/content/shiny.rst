Shiny app
==============
This is the web application that can be used to explore the dataset. It is hosted on shinyapps.io and can be accessed via the following link:

 `Shiny App <https://dssgxmunich2023.shinyapps.io/land_sealing_analysis/>`_


.. image:: ../assets/shiny_app.png
    :alt: test alt text
    :target: https://dssgxmunich2023.shinyapps.io/land_sealing_analysis/


Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Building Plans allow users to filter and explore construction-related data within the date range of 2012 to 2022. This feature empowers users to track the evolution of specific keywords over time and across geographical locations, particularly those related to "hochwasser" (high water) or "BauNVO" (Building Land Use Ordinance).

Keyword Exploration
""""""""""""""""""""""""""""""""""""""""""""
Users can gain insights into how keywords related to construction and flood management have appeared over time and in different regions. This data provides valuable information for various purposes, from research to urban planning.

Structural Level of Use
""""""""""""""""""""""""""""""""""""""""""""

By selecting any of the keywords in the "Maß der baulichen Nutzung" (Degree of Building Use) category, users can access information on the structural levels associated with each building plan. These values have been extracted using a Large Language Model, and additional details on the methodology and documentation are available in the project's GitHub repository.

Regional Plans
""""""""""""""""""""""""""""""""""""""""""""

The Regional Plans section focuses on specific regional plans within the NRW (North Rhine-Westphalia) region. These plans have been manually selected and processed to provide users with comprehensive insights.

PDF Segmentation
""""""""""""""""""""""""""""""""""""""""""""

The PDFs of regional plans have been segmented into chapters and sections, effectively transforming them into structured rows of data. This approach allows users to explore the presence of specific keywords, such as "Vorranggebiete" (priority areas), "Vorbehaltsgebiete" (reserved areas), or areas affected by flooding, within each chapter and section of the plan.

Keyword Search
""""""""""""""""""""""""""""""""""""""""""""

For enhanced usability, users can utilize the "Explore topics by chapter" feature. Simply enter a topic of interest that may be found within the regional plans. For example, searching for chapters containing the word "wasser" (water) and the section labeled "explanation" will help filter and display relevant information.
