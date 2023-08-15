import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Creating dataframe 
dataframe = pd.read_csv("./data/traffic.csv")

# drop null values
df = dataframe.dropna()

df['DateTime'] = df['DateTime'].astype('datetime64[ms]')

df['Time'] = df["DateTime"].dt.time

df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour

df['Day-of-Week'] = df['DateTime'].dt.day_of_week

df['Year'] = df['DateTime'].dt.strftime('%Y')

df = df.drop(columns='ID')

df['Month'] = df['DateTime'].dt.strftime('%m')

df['Day'] = df['DateTime'].dt.strftime('%d')

df["Month-Day"] = df['Month-Day'].str.replace("-","").astype(int)

df_copy = df.copy()

df_copy = df_copy.drop(columns=['DateTime','Time'])

df_copy['Year'] = df_copy['Year'].astype('int32')
df_copy['Month'] = df_copy['Month'].astype('int32')
df_copy['Day'] = df_copy['Day'].astype('int32')

df_copy.to_csv("data/preprocesed_data.csv", sep=',', encoding='utf-8', index=False)

