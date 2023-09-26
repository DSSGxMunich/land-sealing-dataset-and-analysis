library(jsonlite)
library(sf)
library(tidyverse)

regions_geo <- read_sf("../../../data/nrw/rplan/raw/geo/regions_map.geojson")

regions_geo <- regions_geo %>% filter(LND == 5) 

st_write(regions_geo, 'R/data/regional_plans_NRW.geojson')
