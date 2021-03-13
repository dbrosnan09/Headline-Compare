###code for backing up html to be used when can schedule tasks on python anywhere, paste onto bottom of scraper.py

from bs4 import BeautifulSoup
import requests
from datetime import date
import os.path
url = 'https://nytimes.com'
nytimes_content = requests.get(url)
nytimes_soup = BeautifulSoup(nytimes_content.content,"html.parser")

url = 'https://bbc.com/news'
bbc_content = requests.get(url)
bbc_soup = BeautifulSoup(bbc_content.content,"html.parser")

url = 'https://foxnews.com'
fn_content = requests.get(url)
fn_soup = BeautifulSoup(fn_content.content,"html.parser")

a = date.today()
file_title = str(a) + "nyt.txt"
f = open("/Users/davidbrosnan/django_scraping_template/htmlbackup/" + file_title, "w+")
b = str(nytimes_soup)

f.write(b)
f.close()

a = date.today()
file_title = str(a) + "bbc.txt"
f = open("/Users/davidbrosnan/django_scraping_template/htmlbackup/" + file_title, "w+")
b = str(bbc_soup)

f.write(b)
f.close()

a = date.today()
file_title = str(a) + "fn.txt"
f = open("/Users/davidbrosnan/django_scraping_template/htmlbackup/" + file_title, "w+")
b = str(fn_soup)

f.write(b)
f.close()