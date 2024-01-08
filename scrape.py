# TODO: allow variable for column name (date)
# TODO: automate this script for weekly scraping
# TODO: handle rank changing for new novel that gets into the top 200 chart (row swap/insertion/drop)
# TODO: replace 进度 from 连载 to 完结 & update 字数 if changed
# TODO: (optional) preserve the link to each novel

import requests
import pandas as pd

# URL of the webpage
url = 'https://www.jjwxc.net/topten.php?orderstr=7&t=1'

# Fetch the HTML content
response = requests.get(url)

# Set the correct encoding (replace 'utf-8' with the encoding used by your webpage)
response.encoding = 'gb18030'

# Now use the text with correct encoding
html_content = response.text

# Parse the table
tables = pd.read_html(html_content)

# Identify the table
table = tables[1]

# Load the table from a CSV file
df = pd.read_csv("晋江总分榜.csv")

# Get the number of columns
numColumns = df.shape[1]
print(f'The number of columns in the DataFrame is: {numColumns}')

# Insert the new data, extract the 作品积分 only
df[numColumns] = table[6]
# print(df.iat[0, numColumns])
# Change 作品积分 to the date scraping the data
df.iat[0, numColumns] = "01072024"

df.to_csv('晋江总分榜.csv', index=False, encoding='utf_8_sig') # gb18030
    
# # # Insert the column 7发表时间 before the column 4进度 (put unchanged to the left while variable to the right)
# # column_to_move = df.iloc[:, 7]
# # column_name = df.columns[7]
# # df.drop(df.columns[7], axis=1, inplace=True)
# # df.insert(4, column_name, column_to_move)
# # df.to_csv('晋江总分榜.csv', index=False, encoding='utf_8_sig') # gb18030
# # print(df)
