import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter

# Reading and initial preprocessing
THYAO = pd.read_csv('C:\\vscode\\hisse_files\\THYAO.IS.csv')
THYAO['Date'] = pd.to_datetime(THYAO['Date'])
THYAO = THYAO.sort_values(by='Date', ascending = False)
THYAO = THYAO.reset_index(drop=True)

BIST = pd.read_csv('C:\\vscode\\hisse_files\\XU100.IS.csv')

# Removing empty rows
Remove_Empty_THYAO = THYAO.dropna()
Remove_Empty_BIST = BIST.dropna()

# Create a copy of the dataframe to avoid SettingWithCopyWarning
Remove_Empty_THYAO = Remove_Empty_THYAO.copy()
Remove_Empty_BIST = Remove_Empty_BIST.copy()

# Date conversion and sorting
Remove_Empty_THYAO['Date'] = pd.to_datetime(Remove_Empty_THYAO['Date'])
Remove_Empty_BIST['Date'] = pd.to_datetime(Remove_Empty_BIST['Date'])
Remove_Empty_BIST = Remove_Empty_BIST.sort_values(by='Date', ascending = False)
Remove_Empty_BIST = Remove_Empty_BIST.reset_index(drop=True)

# Keeping original data
Old_Remove_Empty_THYAO = Remove_Empty_THYAO.copy()
Old_Remove_Empty_BIST = Remove_Empty_BIST.copy()

# Merging and return calculation
merged_data = pd.merge(Remove_Empty_THYAO, Remove_Empty_BIST, on='Date', how='inner', suffixes=('_THYAO', '_BIST'))
merged_data['THYAO_Return'] = merged_data['Adj Close_THYAO'].pct_change()
merged_data['BIST_Return'] = merged_data['Adj Close_BIST'].pct_change()
merged_data = merged_data.dropna()

# General beta calculation
cov_matrix = np.cov(merged_data['THYAO_Return'], merged_data['BIST_Return'])
if cov_matrix[1,1] != 0:
    beta = cov_matrix[0,1] / cov_matrix[1,1]
else:
    beta = np.nan

# Categorizing beta
beta_categories = Counter()

# Grouping by year and month
merged_data['Year'] = merged_data['Date'].dt.year
merged_data['Month'] = merged_data['Date'].dt.month
grouped = merged_data.groupby(['Year', 'Month'])

# Function to calculate monthly beta
def calculate_beta(group):
    cov_matrix = np.cov(group['THYAO_Return'], group['BIST_Return'])
    if cov_matrix[1,1] == 0:
        return np.nan
    beta = cov_matrix[0,1] / cov_matrix[1,1]
    return beta

# Monthly beta calculation
monthly_beta = grouped.apply(calculate_beta)
for (year, month), beta in monthly_beta.items():
    print(f"In {year} month {month}, beta is equal to {beta:.2f}")
    # Categorize the beta values
    if beta < 0:
        beta_categories['less than 0'] += 1
    elif 0 <= beta <= 1:
        beta_categories['between 0 and 1'] += 1
    else:
        beta_categories['greater than 1'] += 1

# Display counts of beta categories
print("\nCounts of beta categories:")
for category, count in beta_categories.items():
    print(f"{category}: {count}")




   
