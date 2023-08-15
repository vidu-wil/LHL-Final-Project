import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("../data/preprocesed_data.csv")
result_df1 = pd.df = pd.read_csv("../test_files/test_2023.csv")
result_df2 = pd.df = pd.read_csv("../test_files/test_2023.csv")
result_df3 = pd.df = pd.read_csv("../test_files/test_2023.csv")
result_df4 = pd.df = pd.read_csv("../test_files/test_2023.csv")

junction_num_grouped = df.groupby('Junction')
df_junc1 = junction_num_grouped.get_group(1).drop(columns='Junction')
df_junc2 = junction_num_grouped.get_group(2).drop(columns='Junction')
df_junc3 = junction_num_grouped.get_group(3).drop(columns='Junction')
df_junc4 = junction_num_grouped.get_group(4).drop(columns='Junction')

def random_forest_train(df_train, df_test):
    y = df_train["Vehicles"]
    X = df_train.drop(columns='Vehicles')
    scaler = StandardScaler() 
    df_scaled = pd.DataFrame(scaler.fit_transform(X))
    X_train = df_scaled
    y_train = y
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    scaler1 = StandardScaler() 
    X_test = pd.DataFrame(scaler1.fit_transform(df_test))
    pred = model.predict(X_test)
    df_test['Vehicles'] = np.around(pred, decimals=0)
    return df_test

rf_junc1 = random_forest_train(df_junc1, result_df1)
rf_junc2 = random_forest_train(df_junc2, result_df2)
rf_junc3 = random_forest_train(df_junc3, result_df3)
rf_junc4 = random_forest_train(df_junc4, result_df4)

rf_junc1.to_csv("../output/output_junc1.csv", sep=',', encoding='utf-8', index=False)
rf_junc2.to_csv("../output/output_junc2.csv", sep=',', encoding='utf-8', index=False)
rf_junc3.to_csv("../output/output_junc3.csv", sep=',', encoding='utf-8', index=False)
rf_junc4.to_csv("../output/output_junc4.csv", sep=',', encoding='utf-8', index=False)