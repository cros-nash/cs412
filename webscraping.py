# web scraping example:
# open/read a URL
# prcoess HTML to extract data we care about
# ... build a cSV file

import requests # HTTP requests
from bs4 import BeautifulSoup
import csv

# start with the URL:
url = 'https://stores.brooksrunning.com/region/US/MA'

# download this web page:

page = requests.get(url)

# page.text is content of webpage

# tokenize the page into HTML tree

soup = BeautifulSoup(page.content, "html.parser")

# find the div container with class "tiles wider"
store_container = soup.find('div', class_='tiles wider')

# break larger div into smaller chunks
rows = store_container.find_all('a')

# go through all stores (rows)
for row in rows:
    # extract name and address from span tages
    name = row.find('span', class_="name")
    address = row.find('span', class_="address")
    print(name.text.strip(), address.text.strip().replace('\n', ','))