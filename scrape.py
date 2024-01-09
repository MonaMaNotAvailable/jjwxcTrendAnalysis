# TODO: backward compatibility: new version of 晋江总分榜 is missing the first row (used to be the column names) line28
# TODO: allow variable for csv name (date), taking input date or extract from system time
# TODO: automate this script for weekly scraping
# TODO: (optional) preserve the link to each novel

import requests
import pandas as pd

# URL of the webpage
url = 'https://www.jjwxc.net/topten.php?orderstr=7&t=1'

# Fetch the HTML content
response = requests.get(url)

# Set the correct encoding (replace 'utf-8' with the encoding used by your webpage)
response.encoding = 'gb18030'

# Use the text with correct encoding
html_content = response.text

# Parse the table
tables = pd.read_html(html_content)

# Identify the table
table = tables[1]

# Keep 3 columns only
table = table[[1, 2, 6]]

# Load the table from a CSV file
df = pd.read_csv("晋江总分榜.csv", dtype=str)

# print(table)
# print(df)

# Prepare for merging
table.rename(columns={1: '1', 2: '2'}, inplace=True)

# Merge based on 作者 & 作品
merged = table.merge(df[['1','2','6']], on=['1','2'], how='outer')
# Change 作品积分 to the date scraping the data
merged.iat[0, 2] = "01092024"

# Assign the first row to be the column names
merged.columns = merged.iloc[0]

# Drop the first row
merged = merged.drop(merged.index[0])

# Reset the index and add it as a new column
merged = merged.reset_index(drop=False)

# Rename the new column
merged.rename(columns={'index': '序号'}, inplace=True)
# print(merged)

# Count the number of NAN
total_nan = merged.isna().sum().sum()
print(f'Total number of NaN values in the newly merged df is: {total_nan}')

# Replace all NaN values with 'missing'
merged = merged.fillna('missing')

merged.to_csv('晋江总分榜.csv', index=False, encoding='utf_8_sig') # gb18030





# **********Statistics********** #

# Write out the stats to separate txt file
with open('WeeklyStats/01092024.txt', 'w') as file:
    old = df.loc[:, '2']
    new = table['2']
    # Check if the rankings are the same
    comparison = old == new

    # Count the number of different rankings
    false_count = (~comparison).sum()

    print(f'Number of changed rankings are: {false_count}', file=file)

    # Elements in new but not in old
    unique_to_df1 = table[~new.isin(old)]['2']

    # # Elements in old but not in new
    unique_to_df2 = df[~old.isin(new)]['2']

    # Print the results
    print("\nDrop out of the ranking (in last week but not in this week):", file=file)
    for item in unique_to_df1:
        print(item, file=file)
    print("New to the ranking (in this week but not in last week):", file=file)
    for item in unique_to_df2:
        print(item, file=file)

    # # Iterate over the comparison results
    # for i in range(len(comparison)):
    #     if not comparison.iloc[i]:
    #         # Print the index and the differing values when a False is encountered
    #         print(f'Rank: {i}, last week: {old.iloc[i]}, this week: {new.iloc[i]}')

    # Reset the index to get the rankings
    df_old = old.reset_index().rename(columns={'index': 'old_rank', '2': 'name'})
    df_new = new.reset_index().rename(columns={'index': 'new_rank', '2': 'name'})

    # Merge the DataFrames on the name
    rankMerged = df_old.merge(df_new, on='name')

    # Calculate the change in rankings (old rank - new rank), positive change indicates an upward movement
    rankMerged['rank_change'] = rankMerged['old_rank'] - rankMerged['new_rank']

    sorted = rankMerged.sort_values(by='rank_change', ascending=False)

    # print(sorted)
    print("\nSignificant rank changes:", file=file)

    for i in range(len(sorted)):
        if abs(sorted.iloc[i,3]) > 2:
            if sorted.iloc[i,3] > 0:
                print(f'{sorted.iloc[i,1]} rank: +{sorted.iloc[i,3]}, this week: {sorted.iloc[i,2]}, last week: {sorted.iloc[i,0]}', file=file)
            else:
                print(f'{sorted.iloc[i,1]} rank: {sorted.iloc[i,3]}, this week: {sorted.iloc[i,2]}, last week: {sorted.iloc[i,0]}', file=file)
                