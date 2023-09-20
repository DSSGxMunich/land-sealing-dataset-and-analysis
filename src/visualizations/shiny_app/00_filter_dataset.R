library(sf)
library(tidyverse)

#Here i will actually have to put in as input the documents and merge their geo column from land parcels

df <- read_sf("../../../data/NRW/land_parcels.geojson")

df <- df %>% mutate(datum = ymd(datum))

subset_df <- df %>% filter(year(datum) > 2012 & year(datum) < 2023) #Select dates to filter from

subset_df <- subset_df %>% select(objectid, datum, name, kommune, regional_plan_name, scanurl)

st_write(subset_df, "data/land_parcels_2012_2022.geojson", append=FALSE)  #Save to Shiny data folder. It has to be there and not in the general data folder so that it can be deployed.


