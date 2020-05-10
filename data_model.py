#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 14:29:18 2020

@author: vigneshshenbagarajan
"""

##Data Model - TimeSeries Forecasting

import pandas as pd
import matplotlib.pyplot as plt

import warnings
import itertools
warnings.filterwarnings("ignore")
plt.style.use("fivethirtyeight")
import statsmodels.api as sm
import matplotlib

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'K'


#Time Series Analysis

df = pd.read_csv('dataEDA.csv')

#drop unwanted columns
df_ts =df.drop(['out_in','unique_id','date','year','weekday','weekday_tag','min','max'],axis = 1)

#data Preprocessing
df_ts = df_ts.groupby(['month']).temp.mean().reset_index()

df_ts =  df_ts.assign(date =['2018-01-01','2018-02-01','2018-03-01','2018-04-01','2018-05-01','2018-06-01','2018-07-01','2018-08-01','2018-09-01','2018-10-01','2018-11-01','2018-12-01'])

df_ts = df_ts.set_index('date')

y = df_ts.temp
y.head()

#Avg temp monthwise
y.plot(figsize = (20,6))
plt.show()

#Time series mopdeling

p = d = q = range(0,2)
pdq = list(itertools.product(p,d,q))
seasonal_pdq = [(x[0],x[1],x[2],12) for x in list(itertools.product(p,d,q))]
print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

print("Selecting best AIC For Model")
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order = param,
                                            seasonal_order = param_seasonal,
                                            enforce_stationarity = False,
                                            enforce_invertibility = False)
            result = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param,param_seasonal,result.aic))
        except :
            continue

mod = sm.tsa.statespace.SARIMAX(y,
                               order =(1,1,1),
                               param_seasonal = (0,0,0,12),
                               enforce_stationarity = False,
                               enforce_invertibility = False)
result = mod.fit()
print(result.summary().tables[1])

pred = result.get_prediction(start = pd.to_datetime('2018-07-01'),dynamic = False)
pred_ci = pred.conf_int()

ax = y['2018-01-01':'2018-07-01'].plot(label = 'observed')
pred.plot(ax = ax,label ='Forecast',alpha= 0.7,figsize = (100,8))

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)


ax.set_xlabel('date')
ax.set_ylabel('temp')
plt.legend

plt.show()

pred = result.get_prediction(start = pd.to_datetime('2018-07-01'),dynamic = False)
pred_ci = pred.conf_int()

ax = y['2018-01-01':].plot(label = 'observed')

pred.plot(ax = ax,label ='Forecast',alpha= 0.6,figsize = (14,14))

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('date')
ax.set_ylabel('temp')
plt.legend

plt.show()

#Predicted and Actual Temp Table
y_Forecasted = pred.predicted_mean
y_truth = y['2018-08-01':]
actual_pred_table = y_truth.to_frame().join(y_Forecasted.to_frame())
actual_pred_table = actual_pred_table.rename(columns = {"temp":"Actual_value"})
actual_pred_table = actual_pred_table.rename(columns = {0:"Predicted_value"})
actual_pred_table['error'] = actual_pred_table.apply(lambda x : x.Predicted_value - x.Actual_value,axis = 1)
actual_pred_table['error_square'] = actual_pred_table.apply(lambda x : x.error**2,axis = 1 )
actual_pred_table

#Error
actual_pred_table.error.mean()
import math
round(math.sqrt(actual_pred_table.error_square.mean()),0)

pred_uc = result.get_forecast(steps=12)
pred_ci = pred_uc.conf_int()
print("prediction of average temperature for next 12 month is")
pred_ci