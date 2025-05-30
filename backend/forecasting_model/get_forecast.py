import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle

model_filename = "../forecast_model.pkl"

def get_forecast(API_data):
    # data is full data recieved from the NASA API

    # select min and max temps
    relevant_data = [[API_data[sol_key]['AT']['mn'], API_data[sol_key]['AT']['mx']] for sol_key in API_data["sol_keys"]]
    weather_df = pd.DataFrame(relevant_data, columns=['min_temp', 'max_temp'])
    
    with open(model_filename, 'rb') as file:
        forecast_model = pickle.load(file)

    forecast = []

    # predict next three days of weather using sliding window
    for i in range(3):
        # get past 7 days of data. put in array as skikit predict expects 2d array
        past_7_days = [weather_df.iloc[-7: , :].values.flatten()]
        print('past 7 days: ')
        print(past_7_days)
        # forecast next day
        pred = np.array(forecast_model.predict(past_7_days)[0])
        # append to weather df for sliding window
        weather_df.loc[len(weather_df)] = pred
        # append to return result
        forecast.append({'min_temp' : pred[0], 'max_temp' : pred[1]})

    return forecast
    

    # convert data into format used by model
