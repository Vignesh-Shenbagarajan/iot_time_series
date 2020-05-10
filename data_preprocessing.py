#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 18:40:09 2020

@author: vigneshshenbagarajan
"""

#Time series Forecasting of temp data

#Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime 
from datetime import date ,time,datetime

df = pd.read_csv('IOT-temp.csv')

df.columns

#drop columns that does not contribute to the time series model
df_ts = df.drop(['id','room_id/id'],axis=1)

#data cleaning 

#check for nulls
df_ts.isnull().any()
df_ts.isnull().sum()

#check for duplicates
df_ts=df_ts.drop_duplicates()


df_ts[df_ts['out/in']=='Out']['temp'].max()
df_ts[df_ts['out/in']=='In']['temp'].max()

df_ts['date'] = pd.to_datetime(df_ts['noted_date']).dt.date
df_ts["year"] = pd.to_datetime(df_ts['noted_date']).dt.year
df_ts["month"] = pd.to_datetime(df_ts['noted_date']).dt.month
df_ts["weekday"]= pd.to_datetime(df_ts['noted_date']).dt.dayofweek
er 
df_ts.weekday.value_counts()

#df_ts.drop('weekday_tag',axis=1,inplace=True)

# creating weekend lists
df_ts['weekday_tag']=df_ts['weekday'].apply(lambda x: 'weekend' if x==5 or x==6 else 'weekday')

#df_ts.to_csv('data_cleaned.csv')