#import modules
import pandas as pd
import numpy as np

# create a dataframe with the dates in 2023 including every hour
dft = pd.DataFrame(
        {'Hours': pd.date_range('2023-01-01', '2024-01-01', freq='1H')}
     )

# Change Date time to type datetime
dft['Hours'] = dft['Hours'].astype('datetime64[ms]')

# extract time from datetime
dft['Time'] = dft["Hours"].dt.time

# extract the hour
dft['Hour'] = pd.to_datetime(dft['Time'], format='%H:%M:%S').dt.hour

#extract Day-of-Week
dft['Day-of-Week'] = dft['Hours'].dt.day_of_week

# extract year
dft['Year'] = dft['Hours'].dt.strftime('%Y')

# extract month
dft['Month'] = dft['Hours'].dt.strftime('%m')

# extract day
dft['Day'] = dft['Hours'].dt.strftime('%d')

# make a copy of the dataframe and delete unnecessary columns
dft_copy = dft.copy()
dft_copy = dft_copy.drop(columns=['Hours','Time'])

# making all as type numeric
dft_copy['Year'] = dft_copy['Year'].astype('int32')
dft_copy['Month'] = dft_copy['Month'].astype('int32')
dft_copy['Day'] = dft_copy['Day'].astype('int32')

# saving as a test file
dft_copy.to_csv("../test_files/test_2023.csv", sep=',', encoding='utf-8', index=False)