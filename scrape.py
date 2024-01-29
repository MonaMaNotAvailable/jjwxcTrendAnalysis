# TODO: validate get in & drop out of the rankings
# TODO: allow variable for column name (date), taking input date or extract from system time
# TODO: automate this script for weekly scraping
# TODO: (optional) preserve the link to each novel

import requests
import pandas as pd



### Part1: Scrape this week's data
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



### Part2: Adjust this week's data in prepare for merging
# Assign the first row to be the column names 
table.columns = table.iloc[0]
# Drop the first row
table = table.drop(table.index[0])
# Reset the index and add it as a new column
table = table.reset_index(drop=True)



### Part3: Adjust previous data in prepare for merging
# Load the table from a CSV file
df = pd.read_csv("晋江总分榜.csv", dtype=str)
# Get rid of the 序号 column before merging
df = df.drop('序号', axis=1)
# print(table)
# print(df)



### Part4: Perform merging
# Merge based on 作者 & 作品
merged = table.merge(df, on=['作者','作品'], how='outer')
# Change 作品积分 to the date scraping the data
merged = merged.rename(columns={'作品积分': '01282024'})



### Part5: Handle NaNs
# # Count the number of NAN
total_nan = merged.isna().sum().sum()
print(f'Total number of NaN values in the newly merged df is: {total_nan}')
# Replace all NaN values with string 'missing'
merged = merged.fillna('missing')



### Part6: Add rankings again & save to file
# Reset the index and add it as a new column
merged = merged.reset_index(drop=False)
# Rename the new column
merged.rename(columns={'index': '序号'}, inplace=True)
# print(merged)

merged.to_csv('晋江总分榜.csv', index=False, encoding='utf_8_sig') # gb18030




### Part7: summarize stats
# **********Statistics********** #

# Write out the stats to separate txt file
with open('WeeklyStats/01282024.txt', 'w') as file:
    #crop the loaded info to 200 rows
    old = df.loc[:, '作品'].iloc[:200]
    new = table['作品']
    # print(old)
    # print(new)
    # Check if the rankings are the same
    comparison = old == new
    # print(comparison)

    # Count the number of different rankings
    false_count = (~comparison).sum()

    print(f'Number of changed rankings are: {false_count}', file=file)

    # Elements in new but not in old
    unique_to_new = []
    # Elements in old but not in new
    unique_to_old = []

    # print(merged.iloc[:, 3:5])
    for index, row in merged.iterrows():
        if row[3] == "missing" and row[4] != "missing":
            unique_to_old.append(row[2])
        elif row[3] != "missing" and row[4] == "missing":
            unique_to_new.append(row[2])

    # Print the results
    print("\nDrop out of the ranking (in last week but not in this week):", file=file)
    for item in unique_to_old:
        print(item, file=file)
    # Handle empty set
    if not unique_to_old:
        print("--None--\n", file=file)
    print("New to the ranking (in this week but not in last week):", file=file)
    for item in unique_to_new:
        print(item, file=file)
    # Handle empty set
    if not unique_to_new:
        print("--None--\n", file=file)

    # # Iterate over the comparison results
    # for i in range(len(comparison)):
    #     if not comparison.iloc[i]:
    #         # Print the index and the differing values when a False is encountered
    #         print(f'Rank: {i}, last week: {old.iloc[i]}, this week: {new.iloc[i]}')

    # Reset the index to get the rankings
    df_old = old.reset_index().rename(columns={'index': 'old_rank'})
    df_new = new.reset_index().rename(columns={'index': 'new_rank'})

    # Merge the DataFrames on the 作品 column
    rankMerged = df_old.merge(df_new, on='作品')

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
                