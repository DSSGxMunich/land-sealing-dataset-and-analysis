library(tidyverse)
library(janitor)
library(jsonlite)

keywords_df <- read_csv("../../../data/keyword_search/exact_search/exact_search_final.csv")

#remove the termination _digit.pdf 
keywords_df$objectid <- as.numeric(str_replace(keywords_df$filename, "(_\\d+)?\\.pdf", ""))

#remove .pdf
keywords_df$document_id <- str_replace(keywords_df$filename, ".pdf", "")

keywords_df <- keywords_df %>% select(-c(contains("hq")))

hochw_keywords_df <- read_csv("../../../data/keyword_search/hochwasser_keywords.zip")

hochw_keywords_df <- hochw_keywords_df %>% select(filename, category, actual_keyword) %>% 
  pivot_wider(id_cols = filename,
              names_from = category,
              values_from = actual_keyword) 

hochw_keywords_df <- hochw_keywords_df %>% mutate_at(vars(hq100:flächensparen), ~as.character(.))

hochw_keywords_df <- hochw_keywords_df %>% mutate_at(vars(hq100:flächensparen), ~ifelse(. == 'NULL', NA, .))

hochw_keywords_df$document_id <- str_replace(hochw_keywords_df$filename, ".pdf", "")

hochw_keywords_df <- hochw_keywords_df %>% select(-filename)

keywords_df <- keywords_df %>% 
  left_join(hochw_keywords_df, by = "document_id") 

#Read results from agent extraction

folder_path_agent <- "../../../data/keyword_search/knowledge_extraction_agent/" 

file_list_agent <- list.files(path = folder_path_agent, pattern = "*.json")  

file_contents_agent <- lapply(file_list_agent, function(file_name) {
  fromJSON(file.path(folder_path_agent, file_name))  
})

#All the csvs from fuzzy search were read into a list, now i merge them all together with Reduce and merge
result_df_agent <- Reduce(function(x, y) merge(x, y, by = 'id', all = TRUE), file_contents_agent)

result_df_agent <- result_df_agent %>% select(id, contains("_extracted_value"))

#Changing the name of 'id' col to filename
result_df_agent <- result_df_agent %>% rename(filename = id)

#Joining to the general keywords df
keywords_df <- keywords_df %>% 
  left_join(result_df_agent)

#Getting the link for each document:

#Reading json file
json_file <- "../../../data/document_texts/nrw_document_texts.json"
documents <- fromJSON(json_file)

#Keep only col of filename and url
documents <- documents %>% select(filename, land_parcel_scanurl)

#Join to our keywords data
keywords_df <- documents %>% inner_join(keywords_df)

#Format names (replacing - and whitespace with _, renaming vars that start with numbers)
keywords_df <- keywords_df %>% clean_names()

#Reorder vars
keywords_df <- keywords_df %>% select(objectid, document_id, filename, land_parcel_scanurl, everything())

# Create df to generate the choices to select in app in nice format
keyword_cols_id <- as_tibble(colnames(keywords_df)) %>%
  rename(colname = value)

keyword_cols_id <- keyword_cols_id %>% filter(!colname %in% c("objectid", "document_id", "filename", "land_parcel_scanurl"))

#Export
write_csv(keywords_df, "R/data/final_keywords.csv") #Save to Shiny data folder. It has to be there and not in the general data folder so that it can be deployed.
write_csv(keyword_cols_id, "R/data/keyword_variables_2.csv")
