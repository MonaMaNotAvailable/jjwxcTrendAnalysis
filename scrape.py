# TODO: !!!fix 01072024 new data column (total points incorrect due to unmatched rows)
# TODO: allow variable for csv name (date), taking input date or extract from system time
# TODO: automate this script for weekly scraping
# TODO: handle rank changing for new novel that gets into the top 200 chart (row swap/insertion/drop)
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

# Load the table from a CSV file
df = pd.read_csv("晋江总分榜.csv")

# Get the number of columns
numColumns = df.shape[1]
# print(f'The number of columns in the DataFrame is: {numColumns}')

# Insert the new data, extract the 作品积分 only
df[numColumns] = table[6]
# print(df.iat[0, numColumns])
# Change 作品积分 to the date scraping the data
df.iat[0, numColumns] = "01072024"

df.to_csv('晋江总分榜.csv', index=False, encoding='utf_8_sig') # gb18030



# *****Statistics***** #

# Should I switch back to separate weekly csv due to how sensitive this ranking is? but a lot of repeated data exist
# print(table[2])
# print(df.iloc[:, 2])

# Write out the stats
with open('WeeklyStats/01072024.txt', 'w') as file:
    # Check if the rankings are the same
    comparison = table[2] == df.iloc[:, 2]

    # Count the number of different rankings
    false_count = (~comparison).sum()

    print(f'Number of changed rankings are: {false_count}', file=file)

    # # Iterate over the comparison results
    # for i in range(len(comparison)):
    #     if not comparison.iloc[i]:
    #         # Print the index and the differing values when a False is encountered
    #         print(f'Rank: {i}, last week: {table.iloc[i, 2]}, this week: {df.iloc[i, 2]}')

    # Elements in table[2] but not in df.iloc[:, 2]
    unique_to_df1 = table[~table[2].isin(df.iloc[:, 2])][2]

    # Elements in df.iloc[:, 2] but not in table[2]
    unique_to_df2 = df.loc[~df.iloc[:, 2].isin(table[2]), df.columns[2]]

    # Print the results
    print("Drop out of the ranking (in last week but not in this week):", file=file)
    for item in unique_to_df1:
        print(item, file=file)
    print("New to the ranking (in this week but not in last week):", file=file)
    for item in unique_to_df2:
        print(item, file=file)