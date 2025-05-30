import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle

# output path
model_filename = "forecast_model.pkl"

df = pd.read_csv('C:/Users/tobyh/mars_weather_system/backend/forecasting_model/temp_data.csv', index_col='sol', parse_dates=True)

# found with inspection
max_sol = 1221

# impute missing sols
full_range = pd.DataFrame({'sol': range(1, max_sol)})
df = pd.merge(full_range, df, on='sol', how='left')
#df = pd.merge(temp_df, pressure_df, on='sol', how='left')

# impute missing data. linear interpolation a good model as weather changes gradually
df.interpolate(method='linear', inplace=True)

# convert to celsius, the unit used by API
df['min_temp'] =  df['min_temp'] - 273.15
df['max_temp'] =  df['max_temp'] - 273.15

features = ['min_temp', 'max_temp']
X = []
y = []

#  we want to base predictions off the previous 7 days of weather
for i in range(7, len(df)):
    past_7_days = df[features].iloc[i-7:i].values.flatten()
    target_day = df[features].iloc[i].values
    X.append(past_7_days)
    y.append(target_day)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=True)


# fit model
model = RandomForestRegressor(n_estimators=50)
model.fit(X_train, y_train)


# evaluate
predictions = model.predict(X_test)

min_mse = mean_squared_error(y_test[0], predictions[0])
max_mse = mean_squared_error(y_test[1], predictions[1])
#mae = mean_absolute_error(df['true'], df['pred'])

# store model
with open(model_filename, 'wb') as file:
    pickle.dump(model, file)


