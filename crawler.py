from requests.structures import CaseInsensitiveDict # request CaseInsensitiveDicts
import cfscrape # scrape clouflare websites

from bs4 import BeautifulSoup as bs # for parsing html
from pathlib import Path # for creating directories

import asyncio # for asynchronous process

scraper = cfscrape.create_scraper() # create cfscrape object
url_home = "https://indiankanoon.org" # home url
url_browse = url_home+"/browse/"

def crawler(url) : # scrape content from web pages
    content_home = scraper.get(url).content
    return bs(content_home, features="html.parser")

def makedir(path): # make directories if not presesnt
    Path(path).mkdir(parents=True, exist_ok=True)

async def download(url, path, title) : # downloads pdfs from url
    print("url:", url)
    path = 'Documents/'+path
    Path(path).mkdir(parents=True, exist_ok=True)

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    payload = "type=pdf"
    r = scraper.post(url, data=payload, headers=headers)

    title = title.replace('/', '-')
    filename = Path(path+'/'+title+'.pdf')
    filename.write_bytes(r.content)


async def results(court, id, year, month, s): # fetches doc links from search results
    counter = 0
    for res in s.find_all('div', attrs={'class':'result_title'}) :
        if counter < 5 :
            title = res.a.string
            file_num = res.a['href'].split('/')[2]
            print(f"{title} : {file_num}")
            await download(url_home+'/doc/'+file_num+'/', court+'/'+year+'/'+month+'/', title)
            counter += 1


async def months(court, id, year, s) : # fetches links for each month
    months, months_url = [], []
    for month in s.find_all('a', href=True) :
        months.append(month.string)
        months_url.append(month['href'])

    for i in range(3, len(months)):
        url = url_home+months_url[i]
        s = crawler(url)
        await results(court, id, year, months[i], s)


async def court_years(court, id): # fetches links for each year
    s = crawler(url_home+id)
    years = []
    
    for year in s.find_all('a', href=True) :
        years.append(year.string)

    for i in range(3, len(years)):
        url = url_home+id+'/'+years[i]
        s = crawler(url)
        await months(court, id, years[i], s)

async def courts(s) : # fetches links for each court
    courts_name, courts_id = [], []
    for court in s.findAll('a', href=True) :
        courts_name.append(court.string)
        courts_id.append(court['href'])

    for i in range(3, len(courts_name)):
        await court_years(courts_name[i], courts_id[i])

async def main() :  
    print("---- Indian Kanoon web crawler ----")

    soup = crawler(url_browse) # scrape browse page for courts
    await courts(soup)

if __name__ == '__main__':
    asyncio.run(main()) # invoke function to run async

    
