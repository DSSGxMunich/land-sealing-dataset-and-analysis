hi! this is the module that runs the shiny app.

`00_filter_dataset.r` and `01_prepro_keywords_data.r` are the files that do the preprocessing on the many files we have so we get a unified dataset, easy and fast to read for the app. it takes as input dataframes that are in the upper 'data' folder, and stores them in a data folder inside 'R' which contains all the content for the shiny app.

after running `01_prepro_keywords_data.r`, you should open the csv file and add a column called variable_name replacing the names of the variables as they come to something understandable and readable for the app.

none of the elements in that folder should be removed since this structure is necessary for the deployment at [land sealing analysis app.](https://dssgxmunich2023.shinyapps.io/land_sealing_analysis/){.uri}
