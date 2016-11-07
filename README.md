## Westrock Coffee Analysis
1. [Motivation](#1-motivation)
2. [The Dataset](#2-the-dataset)
3. [The Model](#3-the-model)
      * [3.1 Setup](#31-setup)
      * [3.2 Splitting the Data](#32-splitting-the-data)
      * [3.3 Running the Model](#33-running-the-model)
      * [3.4 Model Summary](#34-model-summary)
4. [The Staff](#4-the-staff)
      * [4.1 Grouping the Farmers](#41-grouping-the-farmers)
      * [4.2 Staff Summary](#42-staff-summary)
5. [Conclusion](#5-conclusion)

## 1 Motivation

# Agribusiness Training Program

The coffee industry's future wull remain unsecured until transparency, shared value, and the opportunity for presperity amoung smallholder farmers become an industry norm. 

Equipping farners to build a financial foundation based on their coffee businesses creates space for them to reclaim power over their future and in doing so they will ensure our future coffee supply. Coffee farmers who are empowered with specific skills to increase and leverage their collective coffee incomes, are the most qualified individuals to solve the problems that perpetuate poverty in their households and communities.

-- Westrock Coffee

## 2 The Dataset

The dataset was provided to me from Westrock Coffee. The dataset consists of 10,518 farmers with the following features:
- Stations
- Staff
- Group ID
- Household ID
- Farmer Name
- Attendance
- Adoption
- 2015
- 2016
- Course Attended

A brief description of the columns are in [course_description.md](https://github.com/meutband/Capstone/blob/master/column_description.md).

The dataset contain many rows with empty values for columns. I felt that none of the columns were more important to not be empty than 2015 and 2016. These missing entries were recorded as 0 and will unfavorably influence results if used as is. If available, missing values for one year were filled in with the other year. If both years had missing values, the row was dropped from analysis.

## 3 The Model


###3.1 Setup

For analysis, I decided to make a new column that calculate the average yield totals for each farmer. 

The Stations, Staff, and Group ID are categorical variables, therefore for analysis, I created dummy variables for the columns. The Course Attended column is a list of courses. For analysis, I split the list and created dummy variables for each course as well as if a course was taken 2 or more times. 

<p align="left">
<img src="https://github.com/meutband/Capstone/blob/master/images/staff_counts.png"
align="middle"/>
<h4 align="left"> Figure 1. The number of farmers under each staff member.</h4>
</p>

<p align="right">
<img src="https://github.com/meutband/Capstone/blob/master/images/course_counts.png"
align="middle"/>
<h4 align="right"> Figure 1. The number of farmers under each staff member.</h4>
</p>



###3.2 Splitting the Data


###3.3 Running the Model


###3.4 Model Summary


## 4 The Staff


###4.1 Grouping the Farmers


###4.2 Staff Summary



## 5 Conclusion
