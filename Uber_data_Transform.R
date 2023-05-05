# Load necessary packages
library(tidyverse)  # For data manipulation and visualization
library(lubridate)  # For working with dates and times
library(shiny)  # For building interactive web apps

# Read in the Uber data for different months
uber_data_apr <- read.csv("original data/uber-raw-data-apr14.csv") 
uber_data_aug <- read.csv("original data/uber-raw-data-aug14.csv")
uber_data_jul <- read.csv("original data/uber-raw-data-jul14.csv")
uber_data_jun <- read.csv("original data/uber-raw-data-jun14.csv")
uber_data_may <- read.csv("original data/uber-raw-data-may14.csv")
uber_data_sep <- read.csv("original data/uber-raw-data-sep14.csv")

# Combine the data for all months into a single data frame
uber_data <- rbind(uber_data_apr,uber_data_aug, uber_data_jul, 
                   uber_data_jun, uber_data_may, uber_data_sep 
)

# Convert the Date.Time column to a POSIXct format
uber_data$Date.Time <- as.POSIXct(uber_data$Date.Time, format = "%m/%d/%Y %H:%M:%S")

# Add a column for the day of the week
uber_data$day_of_week <- weekdays(as.Date(uber_data$Date.Time))

# Add a column for the week number of the year
uber_data$week <- week(as.Date(uber_data$Date.Time))

# Group the data by month and week and count the number of trips in each group
trips_by_month_week <- uber_data %>%
  group_by(month = month(Date.Time), week) %>%
  summarise(trips = n()) %>%
  arrange(month)

# Group the data by hour of the day and count the number of trips in each group
trips_by_hour <- uber_data %>%
  group_by(hour = hour(Date.Time)) %>%
  summarise(trips = n()) %>%
  arrange(hour)

# Group the data by hour of the day and month of the year, and count the number of trips in each group
trips_by_hour_month <- uber_data %>%
  group_by(hour = hour(Date.Time), month = month(Date.Time, label = TRUE)) %>%
  summarise(trips = n()) %>%
  arrange(hour, month)

# Group the data by day of the month and month of the year, and count the number of trips in each group
trips_by_full_month <- uber_data %>%
  group_by(day = day(Date.Time), month = month(Date.Time, label = TRUE)) %>%
  summarise(trips = n()) %>%
  arrange(day)

# Group the data by day of the week and month of the year, and count the number of trips in each group
trips_by_day_month <- uber_data %>%
  group_by(day_of_week, month = month(Date.Time, label = TRUE)) %>%
  summarise(trips = n()) %>%
  arrange(month)

# Group the data by Uber base code and month of the year, and count the number of trips in each group
trips_by_base_month <- uber_data %>%
  group_by(base = Base, month = month(Date.Time, label = TRUE)) %>%
  summarise(trips = n()) %>%
  arrange(month)
#Create a data frame of number of trips by day and hour of the day
trips_by_hour_day <- uber_data %>%
  group_by(day = day(Date.Time), hour = hour(Date.Time)) %>%
  summarise(trips = n()) %>%
  arrange(day, hour)
#Create a data frame of number of trips by base and day of the week
trips_by_base_day <- uber_data %>%
  group_by(base = Base, day_of_week) %>%
  summarise(trips = n()) %>%
  arrange(base, day_of_week)
#Create a data frame of number of trips by latitude and longitude
trips_by_lat_lon <- uber_data %>%
  group_by(lat = Lat, lon = Lon) %>%
  summarise(trips = n()) 
#Write data frames to csv files
write.csv(trips_by_hour, file = "trips_by_hour.csv")
write.csv(trips_by_hour_month, file = "trips_by_hour_month.csv")
write.csv(trips_by_full_month, file = "trips_by_full_month.csv")
write.csv(trips_by_day_month, file = "trips_by_day_month.csv") 
write.csv(trips_by_base_month, file = "trips_by_base_month.csv")
write.csv(trips_by_hour_day, file = "trips_by_hour_day.csv")
write.csv(trips_by_base_day, file = "trips_by_base_day.csv")
write.csv(trips_by_month_week, file = "trips_by_month_week.csv")
write.csv(trips_by_lat_lon, file = "trips_by_lat_lon.csv")

