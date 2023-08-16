# import modules
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Creating dataframe 
dataframe = pd.read_csv("../data/traffic.csv")

# drop null values
df = dataframe.dropna()

# change the type to datetime
df['DateTime'] = df['DateTime'].astype('datetime64[ms]')

# extract the time
df['Time'] = df["DateTime"].dt.time

# extract the hour
df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour

# extract Day-of-Week
df['Day-of-Week'] = df['DateTime'].dt.day_of_week

# extract year
df['Year'] = df['DateTime'].dt.strftime('%Y')

# extract month
df['Month'] = df['DateTime'].dt.strftime('%m')

# extract day
df['Day'] = df['DateTime'].dt.strftime('%d')

# drop unnecessary columns and make a copy of the dataframe
df = df.drop(columns='ID')
df_copy = df.copy()
df_copy = df_copy.drop(columns=['DateTime','Time'])

# chnage the type to numeric
df_copy['Year'] = df_copy['Year'].astype('int32')
df_copy['Month'] = df_copy['Month'].astype('int32')
df_copy['Day'] = df_copy['Day'].astype('int32')

# save preprocessed data to a csv
df_copy.to_csv("../data/preprocesed_data.csv", sep=',', encoding='utf-8', index=False)

