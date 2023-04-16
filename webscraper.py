"""
This script searches for albums by a given artist on hmv.com and saves their artist, title, price, and format to a CSV file.

Usage:
Enter the artist name when prompted.
The script will then search for all albums by the given artist on hmv.com.
The script will write a CSV file with the artist, title, price, and format of each album that matches the search criteria.
Example:
please enter an artist to search: queen
Success! There are 5 records available for sale on hmv.com by Queen.
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Path to chromedriver
ser = Service(r'/Users/lucy/Desktop/projects/chromedriver_mac64/chromedriver')
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)

# Get artist name from user
userInput = input('please enter an artist to search: ')
artistFormatted = userInput.replace(' ', '-')

# Construct search URL for hmv.com
link = 'https://hmv.com/search?searchtext=' + artistFormatted

# Search for albums by the artist on hmv.com
s.get(link)
results = []
content = s.page_source
soup = BeautifulSoup(content, features="html.parser")

# Extract artist, title, price, and format for each album
for album in soup.find_all('div', {'class': 'prod__content__inner'}):
    try:
        artist = album.find('span', {'class': 'prod__artist'}).text
        name = album.find('a', {'class': 'js-prod-link'}).text
        price = album.find('meta', {'itemprop': 'price'}).get('content')
        format = album.find('p', {'class': 'prod__type'}).text.strip()
        results.append([artist, name, price, format])
    except:
        break

# Write results to CSV file
if len(results) == 0:
    print('No results found - did you spell the artist name correctly?')
else:
    with open('hmv.csv', 'w') as f:
        f.write('artist, title, price, format\n')
        for a in results:
            if a[0].lower() == userInput.lower() and 'Vinyl' in a[3]:
                f.write(','.join(a) + '\n')

    # Read results from CSV file into a DataFrame
    df = pd.read_csv('hmv.csv')

    # Print success message or error message if no results were found
    if len(df) > 1:
        print('Success! There are {} records available for sale on hmv.com by {}.'.format(
            (len(df)), userInput.capitalize()))
    else:
        print('No results found - did you spell the artist name correctly?')
