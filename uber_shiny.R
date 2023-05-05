#Import necessary libraries
library(dplyr)
library(shiny)
library(lubridate)
library(leaflet)
library(tidyverse)
library(ggplot2)
library(shiny)

#Load data files
trips_by_day_month <- read.csv("csv files/trips_by_day_month.csv")
trips_by_full_month <- read.csv("csv files/trips_by_full_month.csv")
trips_by_hour <- read.csv("csv files/trips_by_hour.csv")
trips_by_hour_month <- read.csv("csv files/trips_by_hour_month.csv")
trips_by_base_month <- read.csv("csv files/trips_by_base_month.csv")
trips_by_base_day <- read.csv("csv files/trips_by_base_day.csv")
trips_by_hour_day <- read.csv("csv files/trips_by_hour_day.csv")
trips_by_month_week <- read.csv("csv files/trips_by_month_week.csv")
trips_by_lat_lon <- read.csv("csv files/trips_by_lat_lon.csv")

#Define text to be displayed in the UI
textnum1 <- "For each graph I produced, I utilized the geom_col function. I generated a table that displays the number of trips for each hour, covering the time frame of hour 0 to 23.  "
textnum2 <- "I generated a chart to display the number of trips per hour per month, with each month represented by a different color for ease of differentiation"
textnum3 <- "I generated a graph that displays the number of trips by hour. Although similar to the previous graph that showed trips by hour and month, this one doesn't include the months. Instead, it shows the total number of trips for each hour, aggregated across all months. "
textnum4 <- "Chart that illustrates the number of trips by day and month, Thursdays and Fridays are comparably the busiest days overall. "
textnum5 <- "6 graphs that depict the number of trips taken each day in comparison to each month. "
textnum6 <- "Table that presents the number of trips by days and months. This table can be filtered to display days, trips, or months in a specific order "
textnum7 <- "A visualization to compare the number of trips with their corresponding bases. The graph features five columns representing each month and shows the number of trips associated with each specific base. I opted to use a consistent format for displaying this type of graph as I find it to be the most straightforward way to compare all the data at once. "
textnum8 <- "One heatmap displays the number of trips per hour by day. The highest heat map values are for the later hours. However, the beginning and end of the heatmap appear to be reversed. "
textnum9 <- "This Heatmap displays the number of trips taken per day across different months. Compared to the heatmap showing trips per hour by day, this heatmap exhibits more scattered data points. "
textnum10 <- "The busiest months are the later ones, with higher trip numbers in the later weeks. "
textnum11 <- "This means that the number of trips taken from the first and last bases is lower compared to the number of trips taken from the bases in the middle. "
textnum12 <- "I created a leaflet that shows only 2000 of the lat and lons. The reason for this is because everytime I ran the whole code R would crash. All of the points are on the east side of the US"



#Define the UI layout
ui<-fluidPage( 
  
  tabsetPanel(
    
    tabPanel("table",
             fluidRow(
               column(2.5, textOutput("text_output1")),
               column(3.5,DT::dataTableOutput("table", width = "100%")))),
    
    tabPanel("1stplot1",
             fluidRow(
               column(7, textOutput("text_output2")),
               column(8,plotOutput('plot_01', width = '1000px')))),
    
    tabPanel("2ndplot",
             fluidRow(column(12, textOutput("text_output3")),
                      column(12,plotOutput('plot_02', width = '1000px')))),
    
    tabPanel("3rdplot",
             fluidRow(column(12, textOutput("text_output4")),
                      column(12,plotOutput('plot_03', width = '1000px')))),
    
    tabPanel("plots4-9",
             fluidRow(column(12, textOutput("text_output5")),
                      column(12,plotOutput('plot_04', width = '1000px')),
                      column(12,plotOutput('plot_05', width = '1000px')),
                      column(12,plotOutput('plot_06', width = '1000px')), 
                      column(12,plotOutput('plot_07', width = '1000px')), 
                      column(12,plotOutput('plot_08', width = '1000px')),
                      column(12,plotOutput('plot_09', width = '1000px')))), 
    
    
    tabPanel("Table2",
             fluidRow(
               column(12, textOutput("text_output6")),
               column(12,DT::dataTableOutput("table2", width = "100%")))),
    
    tabPanel("plot10",
             fluidRow(column(12, textOutput("text_output7")),
                      column(12,plotOutput('plot_10', width = '1000px')))), 
    
    tabPanel("1stHeatmap", 
             fluidRow(column(12, textOutput("text_output8")),
                      column(12,plotOutput('heatmap_1', width = '1000px')))),
    
    tabPanel("2ndHeatmap2",
             fluidRow(column(12, textOutput("text_output9")),
                      column(12,plotOutput('heatmap_2', width = '1000px')))),
    
    tabPanel("heatmap3", 
             fluidRow(column(12, textOutput("text_output10")),
                      column(12,plotOutput('heatmap_3', width = '1000px')))),
    
    tabPanel("heatmap4",
             fluidRow(column(12, textOutput("text_output11")),
                      column(12,plotOutput('heatmap_4', width = '1000px')))),
    
    tabPanel("MAP",
             fluidRow(column(12, textOutput("text_output12")),
                      column(12, leafletOutput("leaf")))),
    
    tabPanel("Predictive model", 
             fluidRow(
               #column(12, textOutput("text_output13")),
               column(12, plotOutput("model1"))))
    
    
    
  )
)

server<-function(input,output){
  
  output$text_output1 <- renderText({ textnum1 })
  
  output$table <- DT::renderDataTable(trips_by_hour[,c("Hours","Trips")],options = list(pageLength = 4))
  
  output$text_output2 <- renderText({ textnum2 })
  
  output$plot_01 <- renderPlot({
    ggplot(trips_by_hour_month, aes(x = hour, y = trips, fill = month)) +
      geom_col() +
      xlab("Hours") +
      ylab("Trips") +
      ggtitle("Trips by hour by month")
    
    
  })
  
  output$text_output3 <- renderText({ textnum3 })
  
  output$plot_02 <- renderPlot({
    ggplot(trips_by_hour, aes(x = hour, y = trips)) +
      geom_col(fill = "purple") +
      xlab("Hours") +
      ylab("Trips") +
      ggtitle("trips by hour")
    
  })
  
  output$text_output4 <- renderText({ textnum4 })
  
  output$plot_03 <- renderPlot({
    ggplot(trips_by_day_month, aes(x = day_of_week, y = trips, fill = month)) +
      geom_col() +
      xlab("week_days)") +
      ylab("Months") +
      ggtitle("trips by day by month")
  })
  
  output$text_output5 <- renderText({ textnum5 })
  
  output$plot_04 <- renderPlot({
    ggplot(filter(trips_by_full_month, month == "May"), aes(x = day , y = trips)) +
      geom_col(fill = "red") +
      xlab("Days") +
      ylab("Trips") +
      ggtitle("May Trips")
  })
  
  output$plot_05 <- renderPlot({
    ggplot(filter(trips_by_full_month, month == "April"), aes(x = day , y = trips)) +
      geom_col(fill = "orange") +
      xlab("Days") +
      ylab("Trips") +
      ggtitle("April Trips")
  })
  
  output$plot_06 <- renderPlot({
    ggplot(filter(trips_by_full_month, month == "Jun"), aes(x = day , y = trips)) +
      geom_col(fill = "yellow") +
      xlab("Days") +
      ylab("Trips") +
      ggtitle("June Trips")
  })
  
  output$plot_07 <- renderPlot({
    ggplot(filter(trips_by_full_month, month == "Jul"), aes(x = day , y = trips)) +
      geom_col(fill = "pink") +
      xlab("day") +
      ylab("trips") +
      ggtitle("July Trips")
  })
  
  output$plot_08 <- renderPlot({
    ggplot(filter(trips_by_full_month, month == "August"), aes(x = day , y = trips)) +
      geom_col(fill = "purple") +
      xlab("Days") +
      ylab("Trips") +
      ggtitle("Ausgust Trips")
  })
  
  output$plot_09 <- renderPlot({
    ggplot(filter(trips_by_full_month, month == "Sep"), aes(x = day , y = trips)) +
      geom_col(fill = "#f90492") +
      xlab("Days") +
      ylab("Trips") +
      ggtitle("September Trips")
  })
  
  output$text_output6 <- renderText({ textnum6 })
  
  output$table2 <- DT::renderDataTable(trips_by_full_month[,c("Days","Trips", "Month")],options = list(pageLength = 4)) 
  
  output$text_output7 <- renderText({ textnum7 })
  
  output$plot_10 <- renderPlot({
    ggplot(trips_by_base_month, aes(x = base , y = trips, fill = month)) +
      geom_col() +
      xlab("base") +
      ylab("trips") +
      ggtitle("Month Base")
    
  }) 
  
  output$text_output8 <- renderText({ textnum8 })
  
  output$heatmap_1 <-renderPlot({
    ggplot(trips_by_hour_day, aes(x = hour, y = day, fill = trips)) +
      geom_tile() + 
      xlab("hour") + 
      ylab("day")  
  })
  
  output$text_output9 <- renderText({ textnum9 })
  
  output$heatmap_2 <- renderPlot({
    ggplot(trips_by_full_month, aes(x = month, y = day, fill = trips)) + 
      geom_tile() + 
      xlab("Months") + 
      ylab("Days")
  }) 
  
  output$text_output10 <- renderText({ textnum10 })
  
  output$heatmap_3 <- renderPlot({
    ggplot(trips_by_month_week, aes(x = month, y = week, fill = trips)) +
      geom_tile() + 
      xlab("Months") +
      ylab("Weeks")
  })
  
  output$text_output11 <- renderText({ textnum11 })
  
  output$heatmap_4 <- renderPlot({
    ggplot(trips_by_base_day, aes(x = base, y = day_of_week, fill = trips)) +
      geom_tile() + 
      xlab("Base") +
      ylab("Days")
  })
  
  output$text_output12 <- renderText({ textnum12 })
  
  output$leaf <- renderLeaflet({
    leaflet(head(trips_by_lat_lon, 2000)) %>%
      addTiles() %>%
      addMarkers(~lon, ~lat, popup = "trips")
  })
  
  output$text_output13 <- renderText({ text13 })
  
  output$model1 <- renderPlot({
    model <- lm(trips ~ month, data = trips_by_full_month)
    predictions <- predict(model)
    observed <- trips_by_full_month$trips
    plot(predictions, observed, xlab = "Predictions", ylab = "Observations")
  })
} 

shinyApp(ui=ui, server=server)









