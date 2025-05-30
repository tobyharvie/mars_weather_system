import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# info: pressure data was being process very slowly - one file every 10 minutes. Perhaps slowed down by online server
# this would take too long to run with 1200 files, so I have not included pressure data in the model yet.

# data is located here. To get csv files, first need to enter subfolder of form /sol_[start]_[end]
base_url = "https://atmos.nmsu.edu/PDS/data/PDS4/InSight/ps_bundle/data_calibrated/"

all_data = []
output_path = 'pressure_data.csv'

# scrape parent directory
parent_response = requests.get(base_url)
parent_soup = BeautifulSoup(parent_response.text, 'html.parser')

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
            if href and href.endswith('.csv') and 'calibevent' not in href:

                file_url = folder_url + href
                print(f"Processing: {file_url}")

                # get sol from file name. File names of form [desc]_[desc]_[sol]_[version]
                sol = int(href.split('_')[2])

                try:
                    # read csv file from url
                    # low memory set false to suppress dtype warning on irrelevant column
                    df = pd.read_csv(file_url, low_memory=False)
                except Exception as e:
                    print(f"Failed to load {file_url}: {e}")
                    continue

                if 'PRESSURE' in df.columns:

                    # append data
                    data = {'sol' : sol, 
                                    'pressure_mean' : df['PRESSURE'].mean(),
                                    'pressure_min' : df['PRESSURE'].min(),
                                    'pressure_max' : df['PRESSURE'].max()}
                    
                    
                    # backup writing
                    with open("pressure.jsonl", "a") as f:
                        json.dump(data, f)
                        f.write("\n")
                    
                    all_data.append(data)


# Concatenate all collected data and write to csv
combined_df = pd.DataFrame(all_data)
combined_df.to_csv(output_path, index=False)
print(combined_df)