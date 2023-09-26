library(tidyverse)
library(janitor)
library(jsonlite)


format_keyword_files <- function(input_path = '../../../data/nrw/bplan/features/keywords/fuzzy_search/', 
                                 file_pattern = '*.csv') #can be changed to '*.json'
  {
  defined_path <- input_path
  
  file_list <- list.files(path = input_path, pattern = file_pattern)  
  
  if (grepl('json', file_pattern)) {
    
    file_contents <- lapply(file_list, function(file_name) {
      fromJSON(file.path(defined_path, file_name))  
    })
    
  } else if (grepl('csv', file_pattern)) {
    file_contents <- lapply(file_list, function(file_name) {
      read_csv(file.path(defined_path, file_name))  
    })
    
  }
  
  result <- Reduce(function(x, y) merge(x, y, by = 'id', all = TRUE), file_contents)
  
  return(result)
}
  

keywords_df <- read_csv("../../../data/nrw/bplan/features/keywords/exact_search/baunvo_keywords.csv")

#remove the termination _digit.pdf 
keywords_df$objectid <- as.numeric(str_replace(keywords_df$filename, "(_\\d+)?\\.pdf", ""))

#remove .pdf
keywords_df$document_id <- str_replace(keywords_df$filename, ".pdf", "")

### Hochwasser

hochw_keywords_df <- read_csv("../../../data/nrw/bplan/features/keywords/exact_search/hochwasser_keywords.csv")
 
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

df_agent <- format_keyword_files(input_path = '../../../data/nrw/bplan/features/keywords/knowledge_extraction_agent/',
                                        file_pattern = '*.json')
  
df_agent <- df_agent %>% select(id, contains("_extracted_value")) #Select only extracted values

#Changing the name of 'id' col to filename
df_agent <- df_agent %>% rename(filename = id)

#Joining to the general keywords df
keywords_df <- keywords_df %>% 
  left_join(df_agent)

#Getting the link for each document:

#Reading json file
json_file <- "../../../data/nrw/bplan/raw/text/document_texts.json"
documents <- fromJSON(json_file)

#Keep only col of filename and url
documents <- documents %>% select(filename, land_parcel_scanurl)

#Join to our keywords data
keywords_df <- documents %>% inner_join(keywords_df)

#Format names (replacing - and whitespace with _, renaming vars that start with numbers)
keywords_df <- keywords_df %>% clean_names()

#Reorder vars
keywords_df <- keywords_df %>% select(objectid, document_id, filename, land_parcel_scanurl, everything())

keywords_df <- keywords_df %>% 
  select(objectid, land_parcel_scanurl:th_extracted_value) %>% 
  group_by(objectid) %>% 
  mutate_at(vars(land_parcel_scanurl:th_extracted_value), 
            ~paste(., collapse = ', ')) %>%
  distinct()

keywords_df <- keywords_df %>% 
  mutate_at(vars(land_parcel_scanurl:th_extracted_value), 
            ~str_replace_all(., "NA,?\\s*", ""))

keywords_df <- keywords_df %>% 
  mutate_at(vars(land_parcel_scanurl:th_extracted_value), 
            ~as.factor(case_when(
              . == "" | . == " " ~ NA,
              TRUE ~ .
            )))

# Create df to generate the choices to select in app in nice format
keyword_cols_id <- as_tibble(colnames(keywords_df)) %>%
  rename(colname = value)

keyword_cols_id <- keyword_cols_id %>% filter(!colname %in% c("objectid", "document_id", "filename", "land_parcel_scanurl"))

#Export
write_csv(keywords_df, "R/data/final_keywords.csv") #Save to Shiny data folder. It has to be there and not in the general data folder so that it can be deployed.
write_csv(keyword_cols_id, "R/data/keyword_variables.csv")
