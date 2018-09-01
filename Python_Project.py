# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 21:17:16 2017

@author: Rakshit
"""

import pandas as pd
import cufflinks as cf
cf.go_offline()
import plotly as py
from matplotlib.ticker import FuncFormatter
import wikipedia as wp
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression


formatter = FuncFormatter(lambda y, pos: "%d%%" % (y))


df_dist=pd.read_csv('2015_16_Districtwise.csv')
df_dist.describe()


df_dist.isnull().sum().sum() # To find out missing values if any, 569 missing values

df_dist.isnull().sum()


df_dist.drop(['STATCD','DISTCD','DISTRICTS','BLOCKS','CLUSTERS'],axis=1,inplace=True)
df_dist.describe()


#Delete columns with all zero entries 
df_dist=df_dist.loc[:, (df_dist != 0).any(axis=0)]


# Impute Null values with suitable values
df_dist['TOTPOPULAT'].fillna((df_dist['TOTPOPULAT'].mean()), inplace=True)
df_dist['P_URB_POP'].fillna((df_dist['P_URB_POP'].mean()), inplace=True)
df_dist['POPULATION_0_6'].fillna((df_dist['POPULATION_0_6'].mean()), inplace=True)
df_dist['GROWTHRATE'].fillna((df_dist['GROWTHRATE'].mean()), inplace=True)
df_dist['SEXRATIO'].fillna((df_dist['SEXRATIO'].mode()[0]), inplace=True)
df_dist['P_SC_POP'].fillna((df_dist['P_SC_POP'].mean()), inplace=True)
df_dist['P_ST_POP'].fillna((df_dist['P_ST_POP'].mean()), inplace=True)
df_dist['OVERALL_LI'].fillna((df_dist['OVERALL_LI'].mean()), inplace=True)
df_dist['FEMALE_LIT'].fillna((df_dist['FEMALE_LIT'].mean()), inplace=True)
df_dist['MALE_LIT'].fillna((df_dist['MALE_LIT'].mean()), inplace=True)
df_dist['TOT_6_10_15'].fillna((df_dist['TOT_6_10_15'].mean()), inplace=True)
df_dist['TOT_11_13_15'].fillna((df_dist['TOT_11_13_15'].mean()), inplace=True)
df_dist['AREA_SQKM'].fillna((df_dist['AREA_SQKM'].mean()), inplace=True)
mean_areasqm=df_dist['AREA_SQKM'].mean()
df_dist['AREA_SQKM']=df_dist.AREA_SQKM.mask(df_dist.AREA_SQKM==0,mean_areasqm)
df_dist.to_csv('cleandata.csv',index=False)


# Reading the cleaned CSV to do data analysis
df=pd.read_csv('cleandata.csv')

# Ploting the overall literacy rate by states
overall_lit=df[['STATNAME','OVERALL_LI']].groupby('STATNAME').mean()
py.offline.plot(overall_lit.iplot(kind='bar',barmode='stack',fontsize=5,shape=(2,5),title='Average Literacy Rate Overall across different States (in %age)',asFigure=True))


#Plotting the male and female literacy states by states
mf_lit=df[['STATNAME','MALE_LIT','FEMALE_LIT']].groupby('STATNAME').mean()
py.offline.plot(mf_lit.iplot(kind='bar',barmode='stack',fontsize=5,shape=(2,5),title='Average Literacy Rate by Gender across different States (in %age)',asFigure=True))


#Presence of Basic Infrastrucutral facilities among the highest literacy states and lowest litearcy states (states only and no union terrotries)
df1=df.loc[df['STATNAME'].isin(['KERALA','GOA','MIZORAM','BIHAR','JHARKHAND','RAJASTHAN'])]
df1['midaymealsprovided']=df1['MDMTOT']+df1['KITSTOT']+df1['KITTOT']
mf_lit=df1[['STATNAME','SWATTOT','DISTNAME','SELETOT','ROADTOT','SGTOILTOT','midaymealsprovided']].groupby('STATNAME').mean()
py.offline.plot(mf_lit.iplot(kind='bar',barmode='stack',fontsize=5,shape=(2,5),title='Presence of basic infrastructural facilities among highest and lowest literacy states',asFigure=True))


# Indian education law states that any person with age >= 7 having the ability to read & write is lliterate
# Subtracting population between Age 0 & 6 from total population to find out the eligible dataset as defined in Indian Law
df['pop_gt_7']=df['TOTPOPULAT']-df['POPULATION_0_6']


# Finding and plotting the most densely populated states based on population per sqkm
df['denspop']=df['pop_gt_7']/df['AREA_SQKM']
py.offline.plot(df[['STATNAME','denspop']].groupby('STATNAME').mean().iplot(kind='bar',asFigure=True,shape=(2,5),fontsize=5,title='Average Density Population by States'))


# Integrate area sq km variable to determine the state with most literate population per sq km
# Defining a new variable to find out the number of literate persons per square km
df['lt_per_sqkm']=(df['OVERALL_LI']/100)*(df['pop_gt_7']/df['AREA_SQKM'])
py.offline.plot(df[['STATNAME','lt_per_sqkm']].groupby('STATNAME').mean().iplot(kind='bar',asFigure=True,shape=(2,5),fontsize=5,title='Average Number of literate people per square km divided by states' ))

''' Elementary level'''
# Caluculating the population between age group 6 to 13, the population for elementary level
df['primstudentpop']=df['TOT_6_10_15']+df['TOT_11_13_15']  
py.offline.plot(df[['STATNAME','primstudentpop']].groupby('STATNAME').sum().iplot(kind='bar',title='Elementary level population among different states',shape=(2,5),fontsize=5,asFigure=True))


# Number of people with Primary/Elementary level literacy across different rates
df['primarystudentliteracyrates']=(df['OVERALL_LI']/100)*df['primstudentpop']
elementary_lit=df[['STATNAME','primarystudentliteracyrates']].groupby('STATNAME').mean()
py.offline.plot(elementary_lit.iplot(kind='bar',barmode='stack',fontsize=5,shape=(2,5),title='Average Number of literate people from elementary level population across different States',asFigure=True))


# Defining Gross Enrollment ratio for elementary education by differnet categories of schools and plotting it for different states
# With variables, ENRTOT,ENRTOTG, ENRTOTP, ENRTOTM, and TOT_6_10_15,TOT_11_13_15

df['grentot%']=(df['ENRTOT']/df['primstudentpop'])*100
df['grentotg%']=(df['ENRTOTG']/df['ENRTOT'])*100
df['grentotp%']=(df['ENRTOTP']/df['ENRTOT'])*100
df['grentotm%']=(df['ENRTOTM']/df['ENRTOT'])*100
py.offline.plot(df[['STATNAME','grentot%']].groupby('STATNAME').mean().iplot(kind='bar',asFigure=True,shape=(2,5),fontsize=5,title='Average Gross Enrollment Ratio across States (in %age)'))
py.offline.plot(df[['STATNAME','grentotg%','grentotp%','grentotm%']].groupby('STATNAME').mean().iplot(kind='bar',title='Avergage Gross Enrollment Ratio among different school categories (Government, Private and Madraasas/Unrecognized) for different states (in %age)',shape=(2,5),fontsize=5,asFigure=True))


''' Analyzing the dataset for SC & ST population at elementary level '''
# Finding out which states has the highest SC & ST population
df['scpop']=(df['P_SC_POP']/100)*df['TOTPOPULAT']
df['stpop']=(df['P_ST_POP']/100)*df['TOTPOPULAT']
py.offline.plot(df[['STATNAME','scpop','stpop']].groupby('STATNAME').mean().iplot(kind='bar',title='Avergage SC & ST population among different states',shape=(2,5),fontsize=5,asFigure=True))


# Enrollmennt levels for backward categories including SC and ST at Primary level
df['scenroll']=((df['SCPTOT']+df['SCUTOT'])/((df['P_SC_POP']/100)*df['TOTPOPULAT']))*100
df['stenroll']=((df['STPTOT']+df['STUTOT'])/((df['P_ST_POP']/100)*df['TOTPOPULAT']))*100
py.offline.plot(df[['STATNAME','scenroll','stenroll']].groupby('STATNAME').mean().iplot(kind='bar',asFigure=True,fontsize=5,shape=(2,5),title='Gross Enrollment level of students for SC & ST categories at primary level across different states'))


''' Feature Scaling & Selection for determining the parameters that most influence the overall literacy rate of the country'''
# Normalizing the data based on min-max normalization
dfno = (df - df.mean()) / (df.max() - df.min())
dfno.to_csv('normaliseddata.csv')

# Read the normalized data CSV file
dfn = pd.read_csv('normaliseddata.csv')

# Create dummy variables for categorical data
dfn = pd.get_dummies(dfn)

# create a base classifier used to evaluate a subset of attributes
model = LinearRegression()

# create the RFE model and select 3 attributes
rfe = RFE(model, 4)
y = dfn['OVERALL_LI']
df = dfn.drop('OVERALL_LI', axis=1)
X = dfn


# this would give my rfe arrays
def feature_selection(rfe):
    rfe = rfe.fit(X, y)
    
    # summarize the selection of the attributes
    print(rfe.support_)
    print(rfe.ranking_)
    # [False False False ..., False False False]
    # [1033  985  109 ...,  351  770  141]

    # the best features are put into al list
    best_feature = []
    list = rfe.support_.tolist()
    for i in range(len(list)):
        if (list[i] == True):
            best_feature.append(i)
        else:
            continue
    return best_feature


best_feature = feature_selection(rfe)
# index of the most important features

df_all = X.iloc[:, best_feature]

import statsmodels.api as sm

#Overall F-test :
from sklearn.linear_model import LinearRegression
X2 = sm.add_constant(df_all)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())


# Feature selection for state Kerala
df1=dfn_all.loc[dfn['STATNAME_KERELA'] == 1]
y1=y[df1.index.values]
X2 = sm.add_constant(df1)
est = sm.OLS(y1, X2)
est2 = est.fit()
print(est2.summary())

# Linear Regression for State Kerala based on number of features determined from feature selection along with features determined by intution
def regression_city(df,index_1,index_2):
    df1 = df[index_1:index_2]
    education = df1['OVERALL_LI']
    rest_1 = df1[['P_URB_POP','POPULATION_0_6','GROWTHRATE','AREA_SQKM']]
    rest_1 = pd.get_dummies(rest_1)

    X2 = sm.add_constant(rest_1)
    est = sm.OLS(education, X2)
    est2 = est.fit()
    print(est2.summary())

regression_city(df,621,634) #Kerala

''' Web scraping'''
# Scraping the Literacy rate data of 190 countries from wikipedia
#Get the html source
html = wp.page("List of countries by literacy rate").html().encode("UTF-8")
df = pd.read_html(html)[0]
df.to_csv('litearcy_rates.csv',index=False,header=0)
print (df)
dgl=pd.read_csv('literacy_rates.csv')
dgl=dgl.iloc[:,0:4]
dgl=dgl.iloc[1:]
dgl=dgl.values
s=pd.DataFrame(dgl)
s.to_csv('s.csv',index=False,header=False)
dlg=pd.read_csv('s.csv',encoding = "ISO-8859-1")
dlg.columns=['country','literacy_rate_all','male_literacy','female_literacy']
dlg1=dlg.loc[dlg.iloc[:, 1] != 'not reported by UNESCO 2015']
dlg1=dlg1.dropna(axis=0, how='any')
dlg1.to_csv('dlg1.csv',index=False)