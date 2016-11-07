import pandas as pd
import numpy as np
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
import seaborn as sns

farmers = pd.read_excel('data/original_farmers.xlsx')
trees = pd.read_excel('data/original_trees.xlsx')

#Combine trees and farmers
trees2 = trees.drop('ID', axis=1)
farmers = pd.concat([farmers, trees2], axis=1, join='inner')

#Fill in 2016 missing values with 2015 vis-a-versa / Trees and Trees_Producing
def copy_zeros(df, col1, col2):
    for i in xrange(len(df[col1])):
        if df[col1][i] > 0.0:
            continue
        else:
            df[col1][i] = df[col2][i]

copy_zeros(farmers, 2015, 2016)
copy_zeros(farmers, 2016, 2015)
copy_zeros(farmers, 'Trees', 'Trees_Producing')
copy_zeros(farmers, 'Trees_Producing', 'Trees')

#Fill all nan values as 0
farmers.fillna(0, inplace=True)

#Add new column of average yield
farmers['Avg. Yield'] = (farmers[2015] + farmers[2016]) / 2.

#Delete rows that are still 0, reset index
farmers = farmers[(farmers[2015] != 0.)]
farmers = farmers.reset_index(drop=True)

#Scatter Matrix for farmers
scatter_matrix(farmers, figsize=(8,8), alpha=.05, color='blue')
plt.savefig('images/scat_matr.png')

#Scatter Matrix for farmers sqrt 2015, 2016
farmers2 = farmers.copy()
farmers2[2015] = farmers2[2015].apply(lambda x: np.sqrt(x))
farmers2[2016] = farmers2[2016].apply(lambda x: np.sqrt(x))
scatter_matrix(farmers2, figsize=(8,8), alpha=.05, color='blue')
plt.savefig('images/scat_matr_sqrt.png')

#Changing the string of course attended to list in new column courses taken
temp  = [s.split(" \n ")[1:] if s != 0 else [] for s in farmers['Course Attended']]
farmers['Courses Taken'] = temp

counts = []
for i in xrange(len(farmers['Courses Taken'])):
    counts.append(len(farmers['Courses Taken'][i]))

#Make histrogram of the farmers and their courses count
df = pd.DataFrame(counts, index=list(farmers['Farmer Name']))
df.plot(kind='hist', figsize=(10,10), bins=25)
plt.savefig('images/course_counts.png')

#Creates set of courses that have been taken
courses = set()
for i in xrange(len(farmers['Courses Taken'])):
    for j in farmers['Courses Taken'][i]:
        courses.add(j)

# #Create heatmap of courses vs courses
df2 = pd.DataFrame(0, index=courses, columns=courses)

#Makes dataframe of index courses and columns courses
Dataframe values are the total occurances of index and column in farmers df
for i in list(df2.columns.values):
    for j in list(df2.index.values):
        for k in farmers['Courses Taken']:
            if i in k and j in k:
                df2[i][j] += 1
            else:
                continue
sns.heatmap(df2)
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.savefig('images/heatmap.png')

#Makes dataframe for courses (took out household id for use)
courses_df = pd.DataFrame()

#Makes columns of courses_df dataframe of count of courses
def add_courses(num):
    if num==1:
        for course in courses:
            check = []
            for row in farmers['Courses Taken']:
                check.append(1 if course in row else 0)
            courses_df[course] = check
        return courses_df
    else:
        for course in courses:
            check = []
            for row in farmers['Courses Taken']:
                check.append(1 if row.count(course) >= num else 0)
            courses_df["{}, {} or more times".format(course,num)] = check
        return courses_df

courses_df = add_courses(1)
courses_df = add_courses(2)

#Make list of columns that are objects (only for data)
groups = ['Station', 'Staff', 'Group ID']

#Function that changes the given column for the index of the list
def dummy(col, data_):
    df_col = pd.get_dummies(data_[col])
    return pd.concat([data_, df_col], axis=1)

#Calling the function for every columns of objects (only for data)
for col in groups:
    farmers = dummy(col, farmers)
    farmers = farmers.drop(col, axis=1)

farmers_short = farmers[[2015, 2016, 'Avg. Yield', 'Adoption']]
courses_df = pd.concat([courses_df, farmers_short], axis=1, join='inner')

#courses_df to xlsx file (with household id's)
writer = pd.ExcelWriter('data/courses_data.xlsx')
courses_df.to_excel(writer, 'Sheet1')
writer.save()

#Check to make sure that the courses taken list is the same as courses_df with
#the same index
print farmers['Courses Taken'][1000]
print courses_df[1000:1001]


#Drop courses taken from farmers (will add courses_df below)
farmers = farmers.drop(['Courses Taken', 'Course Attended', 2015, 2016], axis=1)

#Add farmers and course_df sdataframes to farmers dataframe (without hosuehol id's)
new_farmers = pd.concat([farmers, courses_df], axis=1, join='inner')

#Bar Graph of courses vs. farmers
counts = []
for course in courses:
    counts.append(new_farmers[course].sum())

df = pd.DataFrame(counts, index=courses)
df = df.sort_values(by=0,ascending=False)
df.plot(kind='bar')
plt.savefig('images/courses_farmers.png')

# Make excel file with all data in it
writer2 = pd.ExcelWriter('data/all_data.xlsx')
new_farmers.to_excel(writer2, 'Sheet1')
writer2.save()
