import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data = pd.read_excel('data/all_data_nodummy.xlsx')

#Remove farmers name, household id, and station
data = data.drop(['Farmer Name', 'Household ID', 'Station'], axis=1)

#Courses taken 1 time
courses1 = ['Staff', 'Weed Control', 'Shade Management', 'Climate Change', 'Nutrition & Mulching',
'Adapting to Climate Change', 'Farm Protection (Ecosystem and Biodiversity Conservation)',
'Composting', 'Rainforest Alliance Certification', 'Integrated Pest Management',
'Harvesting Best Practices', 'Erosion Control', 'Community Coffee Collection',
'Farm Business Principles', 'Pruning & Rejuvenation', 'Post Harvesting', 'Mulching',
'Transparency Standards & Group Goal Setting','Transparent Supply Chain & Pricing']

#Courses taken 2 or more times
courses2 = ['Staff', 'Weed Control, 2 or more times',
'Shade Management, 2 or more times', 'Climate Change, 2 or more times',
'Nutrition & Mulching, 2 or more times', 'Adapting to Climate Change, 2 or more times',
'Farm Protection (Ecosystem and Biodiversity Conservation), 2 or more times',
'Composting, 2 or more times', 'Rainforest Alliance Certification, 2 or more times',
'Integrated Pest Management, 2 or more times', 'Harvesting Best Practices, 2 or more times',
'Erosion Control, 2 or more times', 'Community Coffee Collection, 2 or more times',
'Farm Business Principles, 2 or more times', 'Pruning & Rejuvenation, 2 or more times',
'Post Harvesting, 2 or more times', 'Mulching, 2 or more times',
'Transparency Standards & Group Goal Setting, 2 or more times',
'Transparent Supply Chain & Pricing, 2 or more times']


#Group all the farmers by staff, staff and field officers.
#Calculate the mean, median, and counts (sum will count the courses columns) for field officers
mean_staff = data.groupby('Staff').mean()
median_staff = data.groupby('Staff').median()
count_staff = data.groupby('Staff').sum()

mean_group = data.groupby(['Staff', 'Group ID']).mean()
median_group = data.groupby(['Staff', 'Group ID']).median()
count_group = data.groupby(['Staff', 'Group ID']).sum()

#Counts the number of farmers who takes a course once, or two or more times
#Calculates the counts (sum) and mean of each field officers
#Combines mean into one table and counts (sum) into a second table
mean_course1 = data[courses1].groupby('Staff').mean()
count_course1 = data[courses1].groupby('Staff').sum()
mean_course2 = data[courses2].groupby('Staff').mean()
count_course2 = data[courses2].groupby('Staff').sum()

mean_courses = pd.concat([mean_course1.mean(axis=1), mean_course2.mean(axis=1)], axis=1)
count_courses = pd.concat([count_course1.sum(axis=1), count_course2.sum(axis=1)], axis=1)

#Save the calculations in excel spreadsheet
writer = pd.ExcelWriter('data/staff_data.xlsx')
mean_staff.to_excel(writer, 'Sheet1')
median_staff.to_excel(writer, 'Sheet2')
count_staff.to_excel(writer, 'Sheet3')
mean_group.to_excel(writer, 'Sheet4')
median_group.to_excel(writer, 'Sheet5')
count_group.to_excel(writer, 'Sheet6')
mean_courses.to_excel(writer, 'Sheet7')
count_courses.to_excel(writer, 'Sheet8')
writer.save()


#Courses that dont have at lest 10 data values (half)
drops = [('Rank', 'Weed Control'),('Rank', 'Climate Change'), ('Rank', 'Nutrition & Mulching'),
('Rank', 'Erosion Control, 2 or more times'), ('Rank', 'Community Coffee Collection, 2 or more times'),
('Rank', 'Farm Business Principles, 2 or more times'), ('Rank', 'Pruning & Rejuvenation, 2 or more times'),
('Rank', 'Post Harvesting, 2 or more times'), ('Rank', 'Mulching, 2 or more times'),
('Rank', 'Transparency Standards & Group Goal Setting, 2 or more times'),
('Rank', 'Transparent Supply Chain & Pricing, 2 or more times'),
('Rank', 'Climate Change, 2 or more times'), ('Rank', 'Nutrition & Mulching, 2 or more times'),
('Rank', 'Adapting to Climate Change, 2 or more times'), ('Rank', 'Farm Protection (Ecosystem and Biodiversity Conservation), 2 or more times'),
('Rank', 'Composting, 2 or more times'), ('Rank', 'Rainforest Alliance Certification, 2 or more times'),
('Rank', 'Weed Control, 2 or more times'), ('Rank', 'Shade Management, 2 or more times'),
('Rank', 'Transparency Standards & Group Goal Setting'), ('Rank', 'Rainforest Alliance Certification')]


#Calculate the field officer rankings for the mean staff group column by column
ranks = pd.DataFrame()
ranks['Staff'] = list(mean_staff.index.values)
ranks = ranks.set_index('Staff')

for col in mean_staff:
    blah = mean_staff[col].rank(ascending=False, method='average')
    ranks['Rank', str(col)] = blah

ranks = ranks.drop(drops, axis=1)
ranks['Average'] = ranks.mean(axis=1)

#Calculate the field officer rankings for the median staff group column by column
ranks2 = pd.DataFrame()
ranks2['Staff'] = list(median_staff.index.values)
ranks2 = ranks2.set_index('Staff')

for col in median_staff:
    blah = median_staff[col].rank(ascending=False, method='average')
    ranks2['Rank', str(col)] = blah

ranks2 = ranks2.drop(drops, axis=1)
ranks2['Median'] = ranks2.median(axis=1)


#Save the rankings in an excel spreadsheet
writer = pd.ExcelWriter('data/ranks.xlsx')
ranks.to_excel(writer, 'Sheet1')
ranks2.to_excel(writer, 'Sheet2')
writer.save()


#Make a scatterplot for each rankings, sort by average ranking
ranks = ranks.sort_values(by='Average', ascending=False)
avg = ranks.pop('Average')
ranks.reset_index(inplace=True)

columns = list(ranks.columns.values)
columns.remove('Staff')
index = list(ranks.index.values)

for col in columns:
    plt.plot(index, ranks[col], 'o') #for ranks2.png

avg.plot()
plt.xticks(rotation=45)
plt.ylabel('Ranks')
plt.savefig('images/mean_ranks.png')


#Make a scatterplot for each rankings, sort by median ranking
ranks2 = ranks2.sort_values(by='Median', ascending=False)
med = ranks2.pop('Median')
ranks2.reset_index(inplace=True)

columns = list(ranks2.columns.values)
columns.remove('Staff')
index = list(ranks2.index.values)

for col in columns:
    plt.plot(index, ranks2[col], 'o')

med.plot()
plt.xticks(rotation=45)
plt.ylabel('Ranks')
plt.savefig('images/median_ranks.png')


#Make seaborn bar graph that shows attendance vs. adoption for every staff
count1 = data[courses1].sum(axis=1)
count2 = data[courses2].sum(axis=1)

data['Count of Courses Attended'] = count1
data['Count of Courses Attended 2 or more times'] = count2

sns.set(style="whitegrid")
f, ax = plt.subplots(figsize=(10, 15))

sns.set_color_codes("pastel")
sns.barplot(x="Attendance", y="Staff", data=data, label='Attendance', color="b")

sns.set_color_codes("muted")
sns.barplot(x="Adoption", y="Staff", data=data, label="Adoption", color="b")

ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(xlim=(0, 1), ylabel="", xlabel="Percent")
sns.despine(left=True, bottom=True)
plt.savefig('images/att_vs_adop.png')


#Make scatterplots of Attendance times Adoption vs. Counts of courses once
sns.set_context("notebook", font_scale=1.1)
sns.set_style("ticks")

data['Percent Followed'] = data['Adoption'] * data['Attendance']
data2 = data
data2['Count of Courses Attended'] = data['Count of Courses Attended'] - 0.5 + np.random.uniform(size = data.shape[0])
data2['Count of Courses Attended 2 or more times'] = data['Count of Courses Attended 2 or more times'] - 0.5 + np.random.uniform(size = data.shape[0])

sns.lmplot('Percent Followed', 'Count of Courses Attended', data=data2,
fit_reg=False, hue='Staff', size=6, aspect=2)

plt.xlabel('Attendace x Adoption')
plt.ylabel('Count of Courses Attended')
plt.savefig('images/courses1.png')


#Make scatterplots of Attendance times Adoption vs. Counts of courses more than once
sns.set_context("notebook", font_scale=1.1)
sns.set_style("ticks")

sns.lmplot('Percent Followed', 'Count of Courses Attended 2 or more times', data=data2,
fit_reg=False, hue='Staff', size=6, aspect=2)

plt.xlabel('Attendace x Adoption')
plt.ylabel('Count of Courses Attended 2 or more times')
plt.savefig('images/courses2.png')



#Makes seaborn violinplot for adoption rate, avg yield (log), and attendace rate
#Drop 2 staff members who dont show up in the plots
#Sort each graph by median large to small
data['Average Yield'] = np.log(data['Avg. Yield'])

plt.figure(1)

plt.subplot(221)
sns.violinplot(y=data['Adoption'], x=data['Staff'], order=['Nathan Shyirambere',
'Hakizimana Augustin', 'Annociata Uwimana', 'Uwizeyimana Francoise', 'Karambizi Narcisse',
'Twagiruwijuru Emmanuel', 'Ubarijoro Innocent', 'Gasangwa Gustave', 'Habonimana Venuste',
'Mugabufitake J. de Dieu', 'Mugema Emmanuel', 'Mukunzi Fidele',
'Nyirahabimana Charlotte', 'Nyiranshuti Janviere', 'Twizeyimana Deo',
'Uwiringiyimana Joyce', 'Uwizeyimana Rachel'])
plt.xticks(rotation=90)

plt.subplot(222)
sns.violinplot(y=data['Average Yield'], x=data['Staff'], order=['Uwiringiyimana Joyce',
'Ubarijoro Innocent', 'Nyirahabimana Charlotte', 'Mukunzi Fidele', 'Uwizeyimana Rachel',
'Twizeyimana Deo', 'Twagiruwijuru Emmanuel', 'Uwizeyimana Francoise', 'Habonimana Venuste',
'Mugema Emmanuel', 'Karambizi Narcisse', 'Gasangwa Gustave', 'Nyiranshuti Janviere',
'Nathan Shyirambere', 'Mugabufitake J. de Dieu', 'Hakizimana Augustin', 'Annociata Uwimana'])
plt.xticks(rotation=90)

plt.subplot(223)
sns.violinplot(y=data['Attendance'], x=data['Staff'], order=['Uwizeyimana Rachel',
'Mugema Emmanuel', 'Habonimana Venuste', 'Gasangwa Gustave', 'Uwizeyimana Francoise',
'Nyiranshuti Janviere', 'Mukunzi Fidele', 'Nathan Shyirambere', 'Karambizi Narcisse',
'Hakizimana Augustin', 'Mugabufitake J. de Dieu', 'Annociata Uwimana',
'Nyirahabimana Charlotte', 'Twagiruwijuru Emmanuel', 'Ubarijoro Innocent',
'Uwiringiyimana Joyce', 'Twizeyimana Deo'])
plt.xticks(rotation=90)

plt.savefig('images/violins.png')
