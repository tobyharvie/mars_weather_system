import pandas as pd

output_path = 'full_data.csv'

temp_df = pd.read_csv('forecasting_model/temp_data.csv', index_col='sol')
pressure_df = pd.read_csv('forecasting_model/pressure_data.csv', index_col='sol')

# found with inspection
max_sol = 1221

# impute missing sols
full_range = pd.DataFrame({'sol': range(1, max_sol)})
temp_df = pd.merge(full_range, temp_df, on='sol', how='left')
pressure_df = pd.merge(full_range, pressure_df, on='sol', how='left')

full_df = pd.merge(temp_df, pressure_df, on='sol', how='left')

# impute missing data. linear interpolation a good model as weather changes gradually
full_df.interpolate(method='linear', inplace=True)

# convert to celsius, the unit used by API
full_df['min_temp'] =  full_df['min_temp'] - 273.15
full_df['max_temp'] =  full_df['max_temp'] - 273.15
#full_df['mean_temp'] =  full_df['mean_temp'] - 273.15

full_df.to_csv(output_path, index=False)
