import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# Path to chromedriver
artist = input('please enter an artist to search: ')
artist = artist.replace(' ', '-')


ser = Service(r'/Users/lucy/Desktop/projects/chromedriver_mac64/chromedriver')
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)


link = 'https://hmv.com/search?searchtext=' + artist

# hmv.com price
s.get(link)

results = []
content = s.page_source
soup = BeautifulSoup(content, features="html.parser")
for element in soup.find_all(attrs={'class': 'prod__content__inner'}):
    results.append(element.text.strip().replace('\n', ' '))

for i in results:
    if 'Vinyl' in i:
        print(i.strip())
