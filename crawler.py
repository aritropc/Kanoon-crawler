# API Token : f06579b317399553a4c4132215cfab1d1858b9ac

import requests # fetch content from websites
from requests.structures import CaseInsensitiveDict
import cfscrape # scrape clouflare websites

from bs4 import BeautifulSoup as bs # for parsing html
import pycurl as pc
from pathlib import Path # for creating directories
import timeit

scraper = cfscrape.create_scraper()
url_home = "https://indiankanoon.org"
url_browse = url_home+"/browse/"

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

def makedir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def download(url, path, title) :
    print("url:", url)
    Path(path).mkdir(parents=True, exist_ok=True)
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    payload = "type=pdf"
    r = scraper.post(url, data=payload, headers=headers)

    filename = Path(path+'/'+title+'.pdf')
    filename.write_bytes(r.content)

def results(court, id, year, month, s):
    for res in s.find_all('div', attrs={'class':'result_title'}) :
        title = res.a.string
        file_num = res.a['href'].split('/')[2]
        print(f"{title} : {file_num}")
        download(url_home+'/doc/'+file_num+'/', court+'/'+year+'/'+month+'/', title)

    # print(result_url, result_id)

def months(court, id, year, s) :
    months, months_url = [], []
    for month in s.find_all('a', href=True) :
        months.append(month.string)
        months_url.append(month['href'])

    for i in range(3, len(months)):
        # url = url_home+id+'/'+year+'/'+months[i]
        url = url_home+months_url[i]
        # print("flag1 \nurl:", url)
        s = crawler(url)
        # print("months: ", months_url[i])
        results(court, id, year, months[i], s)



def court_years(court, id):
    s = crawler(url_home+id)
    years = []
    
    for year in s.find_all('a', href=True) :
        years.append(year.string)
    # for i in range(0,3):
    #     years.pop(0)
    for i in range(3, len(years)):
        url = url_home+id+'/'+years[i]
        s = crawler(url)
        # print("year :", years[i])
        months(court, id, years[i], s)

def courts(s) :
    courts_name, courts_id = [], []
    for court in s.findAll('a', href=True) :
        courts_name.append(court.string)
        courts_id.append(court['href'])
        
    # for i in range(0,3):
    #     courts_name.pop(0)
    #     courts_id.pop(0)

    for i in range(3, len(courts_name)):
        # print(courts_name[i], ":", courts_id[i])
        court_years(courts_name[i], courts_id[i])

def browse() :  
    print("---- Indian Kanoon web crawler ----")

    soup = crawler(url_browse)
    courts(soup)
        

    """for i in range(len(courts_name)):
        print(f"[{i+1}] {courts_name[i]}")

    dir = Path.cwd()

    # court_user = int(input("\nEnter the number of the court you want to crawl : "))
    # court_url = url_home + courts_url[court_user-1]
    # print(f"\nYou have selected {courts_name[court_user-1]}.")

    
    dir = Path.cwd()
    Path(dir+'/'+courts_name[court_user-1]).mkdir(parents=True, exist_ok=True)

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
    Path(dir+'/'+courts_name[court_user-1]+'/'+years[year_user]).mkdir(parents=True, exist_ok=True)"""


def test():
    url = "https://indiankanoon.org/search/?formInput=doctypes%3A%20delhidc%20fromdate%3A%201-8-2020%20todate%3A%2031-8-2020&pagenum=39"
    s = crawler(url)

    titles = []
    file_num = []
    for title in s.find_all('div', attrs={'class':'result_title'}) :
        titles.append(title.a.string)
        file_num.append(title.a['href'].split('/')[2])
    
    # print(titles)
    # print(file_num)


    doc_url = url_home+'/doc/'+file_num[0]+'/'
    # file download


def main() :
    browse()

if __name__ == '__main__':
    # browse()
    # test()
    main()
    
