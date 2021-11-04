import os # for os.path.isfile()
import requests # fetch content from websites
import cfscrape # scrape clouflare websites
from bs4 import BeautifulSoup as bs # for parsing html


url_home = "https://indiankanoon.org/browse/"
r = requests.get(url_home)

scraper = cfscrape.create_scraper()
content_home = scraper.get(url_home).content
s = bs(content_home, features="html.parser")

courts = []

for court in s.findAll('a') :
    courts.append(court.string)

for i in range(0,3):
    courts.pop(0)
print(courts)
