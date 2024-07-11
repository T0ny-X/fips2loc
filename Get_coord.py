#%% md
# # Part B
# This part is trying to utilize wikipedia to convert the fips into a coordinates for weather data
# 
# ### Step 1: Utilize wiki aggregate page to create a dataframe.
# https://en.wikipedia.org/wiki/List_of_United_States_FIPS_codes_by_county#bodyContent
#%%
from bs4 import BeautifulSoup
import pandas as pd

with open('loc.html', 'r') as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')

data = []
# Find all table rows
for row in soup.find_all('tr'):
    cols = row.find_all('td')
    # Check if the row has columns (i.e., it's not a header)
    if cols:
        number = cols[0].text.strip()
        link = cols[1].find('a')
        title = link.get('title')
        url = link.get('href')
        data.append([number, title, url])

# Convert the data to a DataFrame
df = pd.DataFrame(data, columns=['Number', 'Title', 'URL'])

#%% md
# ### Step 2: Request and save
# Almost all pages have a coordinates, thus we can simply get those first.
#%%
import requests
import concurrent.futures

# Function to get coordinates from a Wikipedia URL
def get_coordinates(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    geo_tag = soup.find('span', {'class': 'geo'})
    if geo_tag:
        return geo_tag.text
    else:
        return None

# Assuming 'df' is your DataFrame
with concurrent.futures.ThreadPoolExecutor() as executor:
    df['Coordinates'] = list(executor.map(get_coordinates, df['URL']))

#%% md
# ### Step 4: Save and manual lookup
# At the time of writing, only one is missing, so manually use Google Map allows us to get the coord and modify it in the file. 
#%%
df.to_csv('fips2coords.csv')
#%%
