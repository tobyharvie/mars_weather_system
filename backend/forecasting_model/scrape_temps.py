import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

base_url = "https://atmos.nmsu.edu/PDS/data/PDS4/InSight/twins_bundle/data_derived/"

# data is located here. To get csv files, first need to enter subfolder of form /sol_[start]_[end]
parent_response = requests.get(base_url)
parent_soup = BeautifulSoup(parent_response.text, 'html.parser')

all_data = []
output_path = "processed_mars_data.csv"

# scrape parent directory
for parent_link in parent_soup.find_all('a'):
    parent_href = parent_link.get('href')
    if parent_href and 'sol' in parent_href:

         # scrape subfolder       
        folder_url = base_url + parent_href
        print(f"Processing: {folder_url}")

        nested_response = requests.get(folder_url)
        nested_soup = BeautifulSoup(nested_response.text, 'html.parser')

        for link in nested_soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.csv') and 'modelevent' not in href:

                file_url = folder_url + href
                print(f"Processing: {file_url}")

                # get sol from file name. File names of form [desc]_[desc]_[sol]_[version]
                sol = int(href.split('_')[2])

                # open file
                try:
                    # low memory set false to suppress irrelevant dtype warning
                    df = pd.read_csv(file_url, low_memory=False)
                except Exception as e:
                    print(f"❌ Failed to load {file_url}: {e}")
                    continue

                if 'BMY_AIR_TEMP' in df.columns and 'BPY_AIR_TEMP' in df.columns:

                    # get average of two temperature columns
                    df = (df['BMY_AIR_TEMP'] + df['BPY_AIR_TEMP']) / 2 
                    # append data
                    all_data.append({'sol' : sol, 'min' : df.min(), 'max' : df.max()})

# Concatenate all collected data
combined_df = pd.DataFrame(all_data)
combined_df.to_csv('temp_data.csv', index=False)
print(combined_df)