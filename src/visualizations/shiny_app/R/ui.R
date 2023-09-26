library(shiny)

ui <- navbarPage(strong("Land Sealing Analysis of NRW"), id = "map_nav",
                 tabPanel('Home',
                 tags$style(HTML("
                      /* Center-align text */
                      h1, h2, h3, h4, p {
                        text-align: left;
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
                    <h2 id="building-plans-and-regional-plans-documentation">Building Plans and Regional Plans Documentation</h2>
                    <h3 id="building-plans">Building Plans</h3>
                    <p>Building Plans allow users to filter and explore construction-related data within the date range of 2012 to 2022. This feature empowers users to track the evolution of specific keywords over time and across geographical locations, particularly those related to &quot;hochwasser&quot; (high water) or &quot;BauNVO&quot; (Building Land Use Ordinance).</p>
                    <h4 id="keyword-exploration">Keyword Exploration</h4>
                    <p>Users can gain insights into how keywords related to construction and flood management have appeared over time and in different regions. This data provides valuable information for various purposes, from research to urban planning.</p>
                    <h4 id="structural-level-of-use">Structural Level of Use</h4>
                    <p>By selecting any of the keywords in the &quot;Maß der baulichen Nutzung&quot; (Degree of Building Use) category, users can access information on the structural levels associated with each building plan. These values have been extracted using a Large Language Model, and additional details on the methodology and documentation are available in the project&#39;s GitHub repository.</p>
                    <h3 id="regional-plans">Regional Plans</h3>
                    <p>The Regional Plans section focuses on specific regional plans within the NRW (North Rhine-Westphalia) region. These plans have been manually selected and processed to provide users with comprehensive insights.</p>
                    <h4 id="pdf-segmentation">PDF Segmentation</h4>
                    <p>The PDFs of regional plans have been segmented into chapters and sections, effectively transforming them into structured rows of data. This approach allows users to explore the presence of specific keywords, such as &quot;Vorranggebiete&quot; (priority areas), &quot;Vorbehaltsgebiete&quot; (reserved areas), or areas affected by flooding, within each chapter and section of the plan.</p>
                    <h4 id="keyword-search">Keyword Search</h4>
                    <p>For enhanced usability, users can utilize the &quot;Explore topics by chapter&quot; feature. Simply enter a topic of interest that may be found within the regional plans. For example, searching for chapters containing the word &quot;wasser&quot; (water) and the section labeled &quot;explanation&quot; will help filter and display relevant information.</p>
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
