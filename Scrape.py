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

# Assuming the table you need is the first one
# print(tables[1])
table = tables[1]

# Save the table to a CSV file
table.to_csv('晋江总分榜12312023.csv', index=False, encoding='utf_8_sig') # gb18030



# TODO: preserve the link to each novel