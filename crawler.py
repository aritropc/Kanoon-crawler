# API Token : f06579b317399553a4c4132215cfab1d1858b9ac

import os # for os.path.isfile()
import requests # fetch content from websites
import cfscrape # scrape clouflare websites
from bs4 import BeautifulSoup as bs # for parsing html


scraper = cfscrape.create_scraper()

# for i in range(0,3):
#     courts.pop(0)
# print(courts)

# url_sc = url_home+courts['Supreme Court of India']
# content_sc = scraper.get(url_sc).content
# s_sc = bs(content_sc, features="html.parser")

# startYear_sc = s_sc.findAll('a', href=True)[3].string
# print(startYear_sc)

def crawler(url) :
    content_home = scraper.get(url).content
    return bs(content_home, features="html.parser")
        

if __name__ == '__main__':

    print("---- Indian Kanoon web crawler ----")
    url_home = "https://indiankanoon.org"
    url_browse = url_home+"/browse/"

    courts_name = []
    courts_url = []

    s = crawler(url_browse)

    for court in s.findAll('a', href=True) :
        courts_name.append(court.string)
        courts_url.append(court['href'])
        # courts[court.string] = court['href']
    for i in range(0,3):
        courts_name.pop(0)
        courts_url.pop(0)
        

    for i in range(len(courts_name)):
        print(f"[{i+1}] {courts_name[i]}")

    court_user = int(input("\nEnter the number of the court you want to crawl : "))
    court_url = url_home + courts_url[court_user-1]
    print(f"\nYou have selected {courts_name[court_user-1]}.")

    s = crawler(court_url)
    years = []
    
    for year in s.find_all('a', href=True) :
        years.append(year.string)
    for i in range(0,3):
        years.pop(0)

    for i in range(len(years)):
        print(f"[{i+1}] {years[i]}")    
    year_user = int(input("\nEnter the number of the year you want to crawl : "))

    print(years[year_user-1])