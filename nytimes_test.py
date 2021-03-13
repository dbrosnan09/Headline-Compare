#!/usr/bin/env python                                                                                                                                                                


import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()



url = 'https://nytimes.com'
nytimes_content = session.get(url)
nytimes_soup = BeautifulSoup(nytimes_content.content,"html.parser")
nytimes_headlines = BeautifulSoup(nytimes_content.content,"html.parser").find_all("a"
)

items=nytimes_soup.select('section[data-block-tracking-id="Briefings"] h2')

briefings = []
for i in items:
  a = str(i)
  b = a.find(">")
  c=a.find("</h2")
  nope = a[b:c]
  nope= nope[1:]
  briefings.append(nope)

if len(briefings) < 3:
  briefings = ["kldjflsjdfs", "khdskfjhaskdjf", "lhsdkfhasdkjfh"]


for i in nytimes_headlines:
    if '<h3' or '<h2' in str(i):
        print(i.get_text())
        print(i.get('href'))


nyt_list = []
for i in nytimes_headlines:
    if '<h2' in str(i):
        if 'class="svelte-' not in str(i):
            interlist = []
            interlist.append(i.find('h2').get_text())
            interlist.append(i.get('href'))
            nyt_list.append(interlist)
    elif '<h3' in str(i):
        if 'class="svelte-' not in str(i):
            interlist = []
            interlist.append(i.find('h3').get_text())
            interlist.append(i.get('href'))
            nyt_list.append(interlist)

for z in briefings:
    print(z)

print("kjshdfkskjhfkasjhdfkljhaslkfjdhlaksjhflkjhdsalkjfhlakjshflkjh")
print(briefings[0])

final_nyt_list = []
for y in nyt_list:
    not_brief = True
    for z in briefings:
        if z in y[0]:
            not_brief = False
    if y[0] == 'Opinion':
        not_brief = False
    if not_brief:
        final_nyt_list.append(y)

for i in final_nyt_list:
    print(i)
        
for x in final_nyt_list: 
    if 'https://www.nytimes.com' not in x[1]:
        x[1] = 'https://www.nytimes.com'+x[1]

for y in final_nyt_list:
    print(y)

nytimeslist = []
counter = 1
for y in final_nyt_list:
    interlist = [1]
    interlist.append(counter)
    counter += 1
    interlist.append(y[0])
    interlist.append(y[1])
    nytimeslist.append(interlist)


       

