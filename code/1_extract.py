import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here

import os

# Ensure cache directory exists
os.makedirs("cache", exist_ok=True)

# Extract US state name to abbreviation lookup table
us_state_abbrev = pd.read_csv('https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv')
us_state_abbrev.to_csv('cache/states.csv', index=False)

# Extract salary survey data
original_data = pd.read_csv('https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv')
original_data['year'] = original_data['Timestamp'].apply(pl.extract_year_mdy)
original_data.to_csv('cache/survey.csv', index=False)

# Extract cost of living data for each year
# Note: Placeholder URL 'https://example.com/col_data' should be replaced with actual URLs for each year's cost of living data
for year in original_data['year'].unique():
    col_data = original_data[original_data['year'] == year]
    col_data['year'] = year
    col_data.to_csv(f'cache/col_{year}.csv', index=False)
