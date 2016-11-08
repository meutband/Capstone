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

## Agribusiness Training Program

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

The dataset was combined with a tree dataset that has the number of trees and the number of trees producing yield. 

<p align="center">
<img src="https://github.com/meutband/Capstone/blob/master/images/scat_matr_sqrt.png" width="500" height="500"/>
<h6 align="middle"> Figure 1. Scatter Matrix of the dataset.</h6>
</p>

## 3 The Model

###3.1 Setup

For analysis, I decided to make a new column that calculate the average yield totals for each farmer. 

The Stations, Staff, and Group ID are categorical variables, therefore for analysis, I created dummy variables for the columns. The Course Attended column is a list of courses. For analysis, I split the list and created dummy variables for each course as well as if a course was taken 2 or more times. 

<p align="center">
<img src="https://github.com/meutband/Capstone/blob/master/images/staff_count.png" width="300" height="300"/>
<img src="https://github.com/meutband/Capstone/blob/master/images/course_counts.png" width="300" height="300"/>
<table style="width:100%">
     <tr>
     <td> Figure 2. The number of farmers under each staff member.</td>
     <td> Figure 3. The number of farmers that took x number of courses.</td>
     </tr>
</table>
</p>

<p align="center">
<img src="https://github.com/meutband/Capstone/blob/master/images/heatmap.png" width="400" height="300"/>
<img src="https://github.com/meutband/Capstone/blob/master/images/courses_farmers.png" width="300" height="300"/>
<table style="width:100%">
     <tr>
     <td> Figure 4. The number of times that courses were taken together.</td>
     <td> Figure 5. The number of farmers that take each course.</td>
     </tr>
</table>
</p>

###3.2 Splitting the Data

For splitting the data into a training set and testing set, I choose to use kfold cross validation with the number of folds as 10. 

<p align="center">
<img src="https://github.com/meutband/Capstone/blob/master/images/kfold_image.jpg" width="600" height="300"/>
<h6 align="center"> Figure 6. A breakdown of kfold cross validation.</h6>
</p>

All of the setup and splitting can be found here [clean-up.py] (https://github.com/meutband/Capstone/blob/master/src/clean_up.py).

###3.3 Running the Model

For the model, I choose to use Linear Regression to predict the average yield between 2015 and 2016. Farmer Name, Household ID, 2015 and 2016 were features that I choose to remove from the model in order to get a more accurate prediction from the other features. I added interaction features between the adoption rate and each course taken and each course taken 2 or more times. This allows for no effect on the model if there is no adoption rate. 

As I ran the Linear Model, I removed the least important features (highest pvalue) from the model using Backwards Stepwise Selection technique. I choose to remove features that had a pvalue greater than 0.05. 

<p align="center">
<img src="https://github.com/meutband/Capstone/blob/master/images/back_select.png" width="400" height="400"/>
<h6 align="center"> Figure 7. Backwards Stepwise Selection steps.</h6>
</p>

If an interaction was in the final model, and the course was taken out of the model, then I put the original course column feature back into the model so the effect of the course can occur alongside the interaction. If adoption was removed, then it was also put back into the model. 

###3.4 Model Summary

Below is the results from the model. The code for the model can be found here [all_data_model.py] (https://github.com/meutband/Capstone/blob/master/src/all_data_model.py).

<p align="center">
<img src="https://github.com/meutband/Capstone/blob/master/images/All%20Data%20Adoption%20Summary.png" width="500" height="1000"/>
<h6 align="center"> Figure 8. Backwards Stepwise Selection steps.</h6>
</p>

## 4 The Staff

###4.1 Grouping the Farmers

For field officer analysis, I grouped all the farmers together by their field officer (Staff column). For the each field officer I calculated the mean farmer and the median farmer for all features, and the count of all course features. The features that I focused on in particular were the attendance rates, adoption rates, and the average yield totals. 

For all the mean and median calculations, I ranked the field officers by feature and then calculated the mean and median (with respect to the inital calculations). Below are the graphs for the rankings for each calculation.

<p align="center">
<img src="https://github.com/meutband/Capstone/blob/master/images/mean_ranks.png" width="400" height="300"/>
<img src="https://github.com/meutband/Capstone/blob/master/images/median_ranks.png" width="400" height="300"/>
<table width="100">
     <tr>
     <td> Figure 9. The rankings of the mean values.</td>
     <td> Figure 10. The rankings of the median values.</td>
     </tr>
</table>
</p>

###4.2 Staff Summary



## 5 Conclusion

I want to thank the instructors for all the help and support for the duration of the project as well as the program. I also want the thank Westrock Coffee for the opportunity to work on the project. 

If you have any questions about this project you can reach me on [Twitter] (https://twitter.com/markhevans1) or [LinkedIn] (https://www.linkedin.com/in/markhevans).
