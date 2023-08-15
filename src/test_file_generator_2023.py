import pandas as pd
import numpy as np

dft = pd.DataFrame(
        {'Hours': pd.date_range('2023-01-01', '2024-01-01', freq='1H')}
     )

dft['Hours'] = dft['Hours'].astype('datetime64[ms]')

dft['Time'] = dft["Hours"].dt.time

dft['Hour'] = pd.to_datetime(dft['Time'], format='%H:%M:%S').dt.hour

dft['Day-of-Week'] = dft['Hours'].dt.day_of_week

dft['Year'] = dft['Hours'].dt.strftime('%Y')

dft['Month'] = dft['Hours'].dt.strftime('%m')

dft['Day'] = dft['Hours'].dt.strftime('%d')

dft_copy = dft.copy()

dft_copy = dft_copy.drop(columns=['Hours','Time'])

dft_copy['Year'] = dft_copy['Year'].astype('int32')
dft_copy['Month'] = dft_copy['Month'].astype('int32')
dft_copy['Day'] = dft_copy['Day'].astype('int32')

dft_copy.to_csv("../test_files/test_2023.csv", sep=',', encoding='utf-8', index=False)