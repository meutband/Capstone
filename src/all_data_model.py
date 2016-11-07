import pandas as pd
import statsmodels.api as sm
from sklearn.cross_validation import train_test_split, KFold
from sklearn.metrics import mean_squared_error
import numpy as np

#Import all_data delete courses taken column(list of courses)
data = pd.read_excel('data/all_data.xlsx')
data = data.drop(['Household ID', 'Farmer Name'], axis=1)
data['Intercept'] = 1


#List of all the courses
multi_courses = ['Weed Control, 2 or more times', 'Shade Management, 2 or more times',
'Climate Change, 2 or more times', 'Nutrition & Mulching, 2 or more times',
'Adapting to Climate Change, 2 or more times',
'Farm Protection (Ecosystem and Biodiversity Conservation), 2 or more times',
'Composting, 2 or more times', 'Rainforest Alliance Certification, 2 or more times',
'Integrated Pest Management, 2 or more times', 'Harvesting Best Practices, 2 or more times',
'Erosion Control, 2 or more times', 'Community Coffee Collection, 2 or more times',
'Farm Business Principles, 2 or more times', 'Pruning & Rejuvenation, 2 or more times',
'Post Harvesting, 2 or more times', 'Mulching, 2 or more times',
'Transparency Standards & Group Goal Setting, 2 or more times',
'Transparent Supply Chain & Pricing, 2 or more times']

#if there are less than 100 people who are in the courses 2 or more times,
#then the course is dropped
for course in multi_courses:
    if data[course].sum() < 100:
        data = data.drop(course, axis=1)


#List of all the courses in data
course_dummies = ['Weed Control', 'Shade Management', 'Climate Change', 'Nutrition & Mulching',
'Adapting to Climate Change', 'Farm Protection (Ecosystem and Biodiversity Conservation)',
'Composting', 'Rainforest Alliance Certification', 'Integrated Pest Management',
'Harvesting Best Practices', 'Erosion Control', 'Community Coffee Collection',
'Farm Business Principles', 'Pruning & Rejuvenation', 'Post Harvesting', 'Mulching',
'Transparency Standards & Group Goal Setting', 'Transparent Supply Chain & Pricing',
'Shade Management, 2 or more times', 'Integrated Pest Management, 2 or more times',
'Harvesting Best Practices, 2 or more times', 'Farm Business Principles, 2 or more times',
'Post Harvesting, 2 or more times']

#Makes interaction of course and adoption
for course in course_dummies:
    data[course + ' Adoption'] = data[course]*data['Adoption']

#List of all interactions
course_dummies2 = ['Weed Control Adoption', 'Shade Management Adoption', 'Climate Change Adoption', 'Nutrition & Mulching Adoption',
'Adapting to Climate Change Adoption', 'Farm Protection (Ecosystem and Biodiversity Conservation) Adoption',
'Composting Adoption', 'Rainforest Alliance Certification Adoption', 'Integrated Pest Management Adoption',
'Harvesting Best Practices Adoption', 'Erosion Control Adoption', 'Community Coffee Collection Adoption',
'Farm Business Principles Adoption', 'Pruning & Rejuvenation Adoption', 'Post Harvesting Adoption', 'Mulching Adoption',
'Transparency Standards & Group Goal Setting Adoption', 'Transparent Supply Chain & Pricing Adoption',
'Shade Management, 2 or more times Adoption', 'Integrated Pest Management, 2 or more times Adoption',
'Harvesting Best Practices, 2 or more times Adoption', 'Farm Business Principles, 2 or more times Adoption',
'Post Harvesting, 2 or more times Adoption']

#Statsmodels linear regression, backwards stepwise selection
def backwards(X, model, max_):
    index = str(model.pvalues.idxmax())
    X = X.drop(index, axis=1)
    return X


#Function that implements backwards selection
def backwards2(p, train, test):
    Xtrain = X.iloc[train]
    Xtest = X.iloc[test]
    ytrain = y.iloc[train]
    ytest = y.iloc[test]

    model = sm.OLS(ytrain, Xtrain).fit()
    max1 = model.pvalues.max()
    results = Xtrain

    if p != 1.:
        #Backwards selection
        while max1 > p:
            results = backwards(results, model, max1)
            model = sm.OLS(ytrain, results).fit()
            max1 = model.pvalues.max()

        #If a interaction is in the results but the components arent then the
        #components are put into results
        for interaction in course_dummies2:
            if interaction in results:
                interaction = interaction.split()
                interaction.remove('Adoption')
                interaction = ' '.join(interaction)
                if interaction not in results:
                    results[interaction] = X[interaction]

        if 'Adoption' not in results:
            results['Adoption'] = X['Adoption']

        #Drops columns from Xtest that arent in model
        Xtest_columns = list(Xtest.columns.values)
        for column in Xtest_columns:
            if column not in results:
                Xtest = Xtest.drop(column, axis=1)


    #Run predict and print calculations
    model4 = sm.OLS(ytrain, results).fit()
    pred = model4.predict(Xtest)
    return mean_squared_error(ytest, pred), model4.params


#Kfold cross validation function
def kfold(p):
    error = np.empty(10)
    index = 0
    df = pd.DataFrame()
    for train, test in kf:
        mse, coeff = backwards2(p, train, test)
        error[index] = mse
        df[index] = coeff
        index += 1
    average = np.mean(error)
    return average, df


#Make X,y from dataframe
X = data.drop([2015, 2016], axis=1)
y = X.pop('Avg. Yield')


#Concluded pvalue for results, rerun to get dataframe for just the pvalue.
#Use columns from model within original results to get final model

kf = KFold(len(X), n_folds=10)

avg1, df1 = kfold(0.05)
indexes = list(df1.index.values)
X_final = X[indexes]

final_model = sm.OLS(y, X_final).fit()
print final_model.summary()
