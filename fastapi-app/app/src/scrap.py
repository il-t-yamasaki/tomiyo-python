from bs4 import BeautifulSoup
import urllib.request
import re

def scraper(URL, keyword):
    res = urllib.request.urlopen(URL)
    soup = BeautifulSoup(res, 'html5lib')
    body_href = soup.find_all("a", text=re.compile(keyword))
    return body_href