library(shiny)

ui <- navbarPage(strong("Land Sealing Analysis of NRW"), id = "map_nav",
                 tabPanel('Home',
                 tags$style(HTML("
                      /* Center-align text */
                      h1, h2, p {
                        text-align: center;
                      }
                      
                      /* Add some margin to paragraphs for spacing */
                      p {
                        margin-bottom: 20px;
                      }
                      
                      /* Style links with a different color */
                      a {
                        color: #007BFF; /* You can choose your preferred link color */
                      }
                      
                      /* Style the ordered list (ol) */
                      ol {
                        list-style-type: decimal;
                        margin-left: 20px; /* Add left margin to make it look indented */
                      }
                      
                      /* Style list items (li) */
                      li {
                        margin-bottom: 10px; /* Add spacing between list items */
                      }
                    ")),
                    HTML('<h1 id="welcome-">Welcome!</h1>
                    <p>This is the Shiny App for the Land Sealing Analysis of North Rhine-Westphalia.</p>
                    <p>This was developed during the <a href="https://sites.google.com/view/dssgx-munich-2023/startseite">Data Science for Social Good project in Munich</a>, in the summer of 2023.</p>
                    <p>The goal of this App is to provide users information about building plans and regional plans in NRW. These documents were digitalized and certain relevant keywords were extracted using NLP techniques. </p>
                    <h2 id="building-plans">Building plans</h2>
                    <ol>
                    <li>PDFs were scraped from the NRW geo dataportal and additional resources</li>
                    <li>For the BauNVO and Hochwasser relevant info certain keywords were searched in the building plans. </li>
                    <li>For other information, such as max. area permitted to build, min area and so a LLM model was used to extract information. </li>
                    </ol>
                    <h2 id="regional-plans">Regional plans</h2>
                    <ol>
                    <li>Certain regional plans were selected manually. </li>
                    <li>The PDFs were segmented into chapters and sections as rows of dataframe.</li>
                    <li>A keyword search for relevant words was made. </li>
                    </ol>
                    <p>The full code for this project and the development of the info can be found in the <a href="https://github.com/DSSGxMunich/dssgx_land_sealing_dataset_analysis">GitHub repository</a>.</p>
                    <p>Enjoy! </p>
                    ')
                 ),
                 
                 #Tab for the BP interactive map
                 tabPanel('Building Plans',
                          
                          #Adding CSS file with style for font, format of the box that selects the inputs. 
                          
                          tags$head(includeCSS("styles.css")),
                          
                          div(class="outer",
                              
                              leafletOutput("bplan_map"),
                              
                              absolutePanel(
                                id = "controls", class = "panel panel-default", fixed = TRUE,
                                draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                                width = 400, height = "auto",
                                
                                br(),
                                
                                #Select dates to show
                                dateRangeInput("date_range", "Select date:", 
                                               start = min(df$datum), end = max(df$datum)),
                                
                                # Radio buttons to select the input type
                                radioButtons("inputType", "Keyword category", 
                                             choices = c("BauNVO", "Maß der baulichen Nutzung", "Hochwasser"), 
                                             selected = "BauNVO"),
                                
                                #Select variables to show in heatmap
                                selectInput("color", "Choose keyword:", 
                                             choices = c("", keyword_vars_baunvo)),

                                
                                #To control overlapping, we can remove the polygons that don't contain the word
                                checkboxInput('remove_NA_polygons', 
                                              'Only show parcels that contain the keyword', 
                                              value = FALSE),
                                
                                #Show barcount of that word per years
                                plotOutput("keyword_per_years",
                                             width = "100%",
                                             height = "200px"),
                                
                                p(
                                  HTML("<strong><span style='color: #1f3d99;'>Blue</span></strong> shows all the BP."),
                                  br(),
                                  HTML("<strong><span style='color: #FFCE30;'>Yellow</span></strong> shows all the BP that contain that keyword."),
                                  br(),
                                  HTML("<strong><span style='color: #808080;'>Gray</span></strong> shows the BP that don't.")
                                )
                                
                              ),
                              tags$div(id="cite",
                                       'Data compiled for ', tags$em('Data Science for Social Good'), ' in Munich (2023).'
                              )
                          )),
                 
                  tabPanel('Regional Plans',
                           
                           leafletOutput("regionalplan_map"),
                           
                           tags$head(includeCSS("styles.css")),
                           
                           absolutePanel(
                             id = "controls", class = "panel panel-default", fixed = TRUE,
                             draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                             width = 330, height = "auto",
                             
                             h2('Keyword Explorer'),
                  
                             #Input selection for chapter to look for
                             textInput("chapter_selection", "Explore topics by chapter:", value = "No topic defined"),
                             
                             #Radio selection for type of section to search
                             selectInput("section", "Choose section:", section_type_vars),
                             
                             #Output warning text if necessary (otherwise will be blank based on empty string)
                             uiOutput("textbox_ui"),
                             br(),
                             actionButton("action","Search")
                             
                           ),
                           tags$div(id="cite",
                                    'Data compiled for ', tags$em('Data Science for Social Good'), ' in Munich (2023).'
                           ),
                           )
                 
)
