library(sf)
library(tidyverse)
library(leaflet)

floodings_geo <- read_sf("../../../data/regional_plans/floodings/festgesetzte_Ueberschwemmungsgebiete.shp")

floodings_geo <- floodings_geo %>% st_transform(crs = 4326)
st_write(floodings_geo, 'R/data/flooding_areas.geojson')
