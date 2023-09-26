library(shiny)
library(leaflet)
library(sf)
library(tidyverse)
library(plotly)

# Define the server function
server <- function(input, output, session) {
  
  ### BPLAN SERVER
  
  # Filter data based on date range input
  filtered_data <- reactive({
    
    # Get the inputs that will work as filter
    filter_date_range <- input$date_range
    filter_keyword <- input$color
    filter_parcels <- input$remove_NA_polygons
    
    if (filter_keyword == ""){
      
      filtered_df <- df %>%
        filter(datum >= filter_date_range[1] & datum <= filter_date_range[2])
    
    } else {
      # Filter by date and join with the document keywords. Keep only column of the selected keyword. 
      filtered_df <- df %>%
        filter(datum >= filter_date_range[1] & datum <= filter_date_range[2])#%>%
        #inner_join(keywords_df %>% select(objectid, document_id, land_parcel_scanurl, !!filter_keyword)) 
      
      # Rename the column so it's easier to use, make dichotomic variable has keyword/doesnt have it
      filtered_df <- filtered_df %>%
        rename(keywords_match = !!filter_keyword) %>%
        mutate(has_keyword = ifelse(is.na(keywords_match), "no_word", "has_word"))
      
      filtered_df <- filtered_df%>%
        group_by_at(vars(objectid:kommune)) %>% 
        filter(!("has_word" %in% has_keyword) | has_keyword == "has_word")
      
      filtered_df <- filtered_df %>% unique()
      
      #If checkbox is selected, only show parcels that contain the keyword to control overlapping
      
      if (filter_parcels == TRUE) {
        filtered_df <- filtered_df %>%
          filter(has_keyword == "has_word")
      }
  
    }
    

    return(filtered_df)
    
  })
  
  observeEvent(input$inputType, {
    if (input$inputType == "BauNVO") {
      updateSelectizeInput(session,
                           inputId = "color",
                           choices = c("No keyword" = '', keyword_vars_baunvo))
    } else if (input$inputType == "Maß der baulichen Nutzung") {
      updateSelectizeInput(session,
                           inputId = "color",
                           choices = c("No keyword" = '', keyword_vars_agent))
    } else if (input$inputType == "Hochwasser") {
      updateSelectizeInput(session,
                           inputId = "color",
                           choices = c("No keyword" = '', keyword_vars_hochwasser))
    }
  })
  
  #Render plot with appearance of keyword
  output$keyword_per_years <- renderPlot({
    
    if (input$color == ''){
      p <- filtered_data() %>% 
        as_data_frame() %>%
        group_by(year = year(datum)) %>% 
        summarise(n = n()) %>%
        ggplot(aes(x = as.factor(year), y = n))+
        geom_col()+
        labs(x = "Year",
             y = "",
             title = "BP over time")+
        theme_minimal()
      
    } else {
      
      p <- filtered_data() %>% 
        as_data_frame() %>%
        group_by(year = year(datum), has_keyword) %>%
        summarise(n = n()) %>%
        filter(has_keyword == "has_word") %>%
        ggplot(aes(x = as.factor(year), y = n))+
        geom_col()+
        labs(x = "Year",
             y = "",
             title = "Appearance in documents over time")+
        theme_minimal() 
      
    }
    
    p 
    
  })
  
  # Render the Leaflet map
  output$bplan_map <- renderLeaflet({
    bplans_plot
  })
  
  # Updating map dynamically with leafletProxy
  observe({
    
    if(input$color != ''){
      
      colorData <- filtered_data()$has_keyword
      pal <- colorFactor(palette = c('#FFCE30', '#808080'), colorData)
      
      leafletProxy("bplan_map", data = filtered_data()) %>%
        clearShapes() %>%
        addPolygons(
          popup = ~paste("<b>Year:</b> ", year(datum),
                         "<br><b>Name: </b>", name,
                         "<br><b>Regional Plan: </b>", regional_plan_name,
                         "<br><b>Url: </b> <a href='", land_parcel_scanurl, "'>",land_parcel_scanurl,"</a>",
                         "<br><b>Keywords: </b>", str_sub(keywords_match, start = 1, end = 600)),
          fillColor = pal(colorData),
          weight = 0,
          smoothFactor = 0.2,
          fillOpacity = 0.8
        )
    }
    
  })
  
  
  ## REGIONAL PLAN SERVER
   
   filtered_regions <- reactive({
     
     filter_chapter <-input$chapter_selection
     filter_section <- input$section
     
     result <- rplan_match %>% 
       filter(str_detect(chapter, filter_chapter)) %>%
       filter(section_type == !!filter_section)%>% 
       select(-c(section, ART, LND)) %>% 
       group_by_at(vars(Name, chapter, section_type)) %>%
       summarise_at(vars(vorranggebiete:affected_by_flooding),
                    ~paste(., collapse = ", ")) %>%
       mutate_at(vars(vorranggebiete:affected_by_flooding), 
                 ~case_when(
                   str_detect(., 'TRUE') ~ 'mentions word',
                   TRUE ~ 'does not mention word'
                 ))
     
   return(result)
     
   })
   
   # Render the Leaflet map
   output$regionalplan_map <- renderLeaflet({
     regions_plot01
   })
   
   
   # Updating map dynamically with leafletProxy
    observeEvent(input$action, {
      
      leafletProxy("regionalplan_map") %>%
          clearShapes()  %>%
          addPolygons(
            data = filtered_regions(),
            popup = ~paste(
              "<b>Name:</b> ", Name,
              "<br><b>Chapter name: </b>", chapter,
              "<br><b>Vorranggebiete: </b>", vorranggebiete,
              "<br><b>Vorbehaltsgebiete: </b>", vorbehaltsgebiete,
              "<br><b>Affected by flooding: </b>", affected_by_flooding),
            weight = 0.5,
            color = "white",
            smoothFactor = 0.2,
            fillColor = "#fecc5c",
            fillOpacity = 0.5,
            group = "Regional plans"
          ) 
      })
    
    # Wrap the rendering of textbox_ui in a reactive expression
    textbox_ui <- eventReactive(input$action, {
       if (nrow(filtered_regions()) < 1) {
         return(
           HTML("<strong><span style='color: #c61a09;'>No regional plans found!</span></strong> Please try another topic or section.")
         )
       } else {
         return(NULL)
       }
     })
    
    # Update the UI with the textbox
    output$textbox_ui <- renderUI({
       textbox_ui()
     })
    
    
    
}
