library(shiny)
library(leaflet)
library(sf)
library(tidyverse)
library(plotly)
library(jsonlite)

# Reading and formatting the land parcel dataset 

df <- read_sf("data/land_parcels_2012_2022.geojson")

df <- df %>% mutate(datum = ymd(datum))

df <- df %>% st_transform(crs = 4326)

# read keywords and their ids

keywords_df <- read_csv("data/final_keywords.csv")
keyword_cols_and_names <- read_csv("data/keyword_variables.csv",locale = locale(encoding = "latin1"))


df <- df %>%
 inner_join(keywords_df) 

# Choices for drop-downs
baunvo_vars <- keyword_cols_and_names %>% filter(type == 'baunvo') %>% pull(colname)
baunvo_names <- keyword_cols_and_names %>% filter(type == 'baunvo') %>% pull(variable_name)

keyword_vars_baunvo <- setNames(baunvo_vars, baunvo_names)

agent_vars <- keyword_cols_and_names %>% filter(type == 'agent') %>% pull(colname)
agent_names <- keyword_cols_and_names %>% filter(type == 'agent') %>% pull(variable_name)
  
keyword_vars_agent <- setNames(agent_vars, agent_names)

hochwasser_vars <- keyword_cols_and_names %>% filter(type == 'hochwasser') %>% pull(colname)
hochwasser_names <- keyword_cols_and_names %>% filter(type == 'hochwasser') %>% pull(variable_name)

keyword_vars_hochwasser <- setNames(hochwasser_vars, hochwasser_names)

# Setting boundaries for the map
bounds <- st_bbox(df, crs = 4326)

bplans_plot <- leaflet(df %>%
                         filter(datum >= min(df$datum) & datum <= max(df$datum)))%>% 
  addProviderTiles(providers$Esri.WorldGrayCanvas) %>%
  fitBounds(~min(bounds$xmin), ~min(bounds$ymin), ~max(bounds$xmax), ~max(bounds$ymax)) %>%
  addPolygons(
    popup = ~paste("<b>Year:</b> ", year(datum),
                   "<br><b>Name: </b>", name,
                   "<br><b>Regional Plan: </b>", regional_plan_name,
                   "<br><b>Original url: </b> <a href='", scanurl, "'>",scanurl,"</a>"),
    fillColor = "#1f3d99",
    weight = 0,
    smoothFactor = 0.2,
    fillOpacity = 0.8
  )


# Regional plans prepro
 
 # Extracted info
 
json_file <- "data/rplan_keyword_search_result.json"
rplan_content <- fromJSON(json_file)
 
rplan_content <- as_data_frame(rplan_content) %>%
 unnest(everything())
 
# Map 
 
regions_geo <- read_sf("data/regional_plans_NRW.geojson")

regions_plot01 <- leaflet(regions_geo)%>% 
  addProviderTiles(providers$Esri.WorldGrayCanvas) %>%
  fitBounds(~min(bounds$xmin), ~min(bounds$ymin), ~max(bounds$xmax), ~max(bounds$ymax)) %>%
  addPolygons(
    popup = ~paste(
      "<b>Name:</b> ", Name),
    fillColor = "#1f3d99",
    weight = 1,
    color = 'white'
  )


# Remove null rows
 
rplan_content <- rplan_content %>% filter(!is.na(Name))
 
rplan_match <- regions_geo %>% left_join(rplan_content)

chapters_vars <- unique(rplan_match$chapter)
 
section_type_vars <- c('start', 'explanation', 'principle', 'target')
