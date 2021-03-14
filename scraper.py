# -*- coding: UTF-8 -*-

import os
import sys
import django

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/scraper/')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from custom_scraper.models import Headline
from custom_scraper.models import word_sentiment
from custom_scraper.models import Headlinewrl
from custom_scraper.models import Headlinewc
from custom_scraper.models import total_word_count
from custom_scraper.models import cooc
from custom_scraper.models import Headline_emotion
from custom_scraper.models import emotion
from custom_scraper.models import hl_tokens_emotions
from custom_scraper.models import top_words_emotions_tally
from custom_scraper.models import top_words_emotions_percent
from custom_scraper.models import html_cache
class CustomScraper(object):
    def __init__(self):
        self.url = ""

    def scrape(self):
        print('scraping...')

if __name__ == '__main__':
    scraper = CustomScraper()
    scraper.scrape()


from bs4 import BeautifulSoup
import requests

from custom_scraper.models import variance_table
from custom_scraper.models import variance_table_word



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
    if y[0] == '':
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



#soup it up
url = 'https://foxnews.com'
fn_content = requests.get(url)
fn_soup = BeautifulSoup(fn_content.content,"html.parser")
fn_main = fn_soup.find_all("main")
main = str(fn_main)
main_soup = BeautifulSoup(main, "html.parser")
main_h2 = main_soup.find_all("h2")




#create numbered list of headlines
counter = 0
dailyrank = 1
fnlist = []
for v in main_h2:


  interlist = [3]
  interlist.append(dailyrank)
  dailyrank += 1
  interlist.append(v.text.lstrip().rstrip())
  fnlist.append(interlist)


#extract urls part 1 -> cut off leading
h2_html = []
counter1 = 0
for v in main_h2:

  if "http" in str(v):
    a = str(v).index(">")
    h2_html.append(str(v)[a + 10:])
  else:
    h2_html.append(str(v)[a+12:])
  counter1 += 1

#extract urls part 2: find index of where to cut off trailing
link_end = []

for i in h2_html:
  link_end.append(str(i).index('>'))


#actually cut off trailing
link_rip = []
link_end_index = 0

for i in h2_html:
  a = link_end[link_end_index]
  link_rip.append(i[:a-1])
  link_end_index +=1

#combine headline list with urls
link_rip_index = 0
for i in fnlist:
  b = link_rip[link_rip_index]
  i.append(b)
  link_rip_index += 1
#final in fnlist

from bs4 import BeautifulSoup
import requests


url = 'https://www.bbc.com/news'
bbc_content = requests.get(url)
bbc_soup = BeautifulSoup(bbc_content.content,"html.parser")
bbc_headlines = bbc_soup.findAll("h3")
counter = 0
dailyrank = 1
bbclist = []
vdoublecheck = []
for v in bbc_headlines:
  if "gs-u-vh" not in str(v):
    if "BBC World News TV" or "BBC World Service" not in str(v):
      if v not in vdoublecheck:
        interlist = [2]
        interlist.append(dailyrank)
        dailyrank += 1
        interlist.append(v.text.lstrip().rstrip())
        bbclist.append(interlist)
        if v not in vdoublecheck:
          vdoublecheck.append(v)



bbc_hrefs_soup = bbc_soup.findAll("a")

hrefs = []

vadoublecheck = []
for v in bbc_hrefs_soup:
  if v not in vadoublecheck:
    if "<h3" in str(v):

      if "http" in v["href"]:

        hrefs.append(v['href'])
      else:
        hrefs.append("https://bbc.com" + v['href'])
  vadoublecheck.append(v)

dailyrank2 = 1
hrefsfinal = []
dailyrank2 = 1
for i in hrefs:
  interlist3 = []
  interlist3.append(dailyrank2)
  dailyrank2 += 1
  interlist3.append(i)
  hrefsfinal.append(interlist3)

counter4 = 0
for i in hrefsfinal:
    for y in bbclist:
      if i[0] == y[1]:
        bbclist[counter4].append(i[1])
        counter4 += 1

for v in bbclist:
  if v[2] == "BBC World News TV":
    vindex = bbclist.index(v)
    bbclist.remove(v)
    for i in bbclist:
      if bbclist.index(i) >= vindex:
        i[1] -= 1

for v in bbclist:
  if v[2] == "BBC World Service Radio":
    vindex = bbclist.index(v)
    bbclist.remove(v)
    for i in bbclist:
      if bbclist.index(i) >= vindex:
        i[1] -= 1

#final in bbclist



from textblob import TextBlob


def sentiment_analysis(newspaperlist):
  sentiment_list = []
  for i in newspaperlist:
    text = str(i[2])

    obj = TextBlob(text)
    sentiment = obj.sentiment.polarity
    sentiment_list.append(sentiment)

  article_counter = 0

  for i in sentiment_list:
    newspaperlist[article_counter].append(i)
    article_counter += 1






sentiment_analysis(nytimeslist)
sentiment_analysis(fnlist)
sentiment_analysis(bbclist)







from django.utils import timezone


for i in nytimeslist:
  print(i)

for i in fnlist:
  print(i)

for i in bbclist:
  print(i)

for i in nytimeslist:
    nytimes = Headline(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4])
    nytimes.save()

for i in fnlist:
    foxnews = Headline(headline=str(i[2]), newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4])
    foxnews.save()

for i in bbclist:
    bbc = Headline(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4])
    bbc.save()

#save all data to alternate database with reading levels
import textstat
for i in nytimeslist:
    nytimes_rl = Headlinewrl(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4], reading_level=textstat.text_standard(i[2], float_output=True))
    nytimes_rl.save()

for i in fnlist:
    foxnews_rl = Headlinewrl(headline=str(i[2]), newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4], reading_level=textstat.text_standard(str(i[2]), float_output=True) )
    foxnews_rl.save()

for i in bbclist:
    bbc_rl = Headlinewrl(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4], reading_level=textstat.text_standard(i[2], float_output=True) )
    bbc_rl.save()


#save all data to alternate database with reading levels and headline word counts
import textstat
for i in nytimeslist:
    nytimes_wc = Headlinewc(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4], reading_level=textstat.text_standard(i[2], float_output=True), headline_wc=len(i[2].split()))
    nytimes_wc.save()

for i in fnlist:
    foxnews_wc = Headlinewc(headline=str(i[2]), newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4], reading_level=textstat.text_standard(str(i[2]), float_output=True), headline_wc=len(str(i[2]).split()) )
    foxnews_wc.save()

for i in bbclist:
    bbc_wc = Headlinewc(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4], reading_level=textstat.text_standard(i[2], float_output=True), headline_wc=len(i[2].split()) )
    bbc_wc.save()



#custom function to weed out stopwords, plurals and apostrophe s and get count of each word in a string
def get_sorted_word_count_by_string_emotion(all_headline_string):
    all_headline_test = all_headline_string
    # regex to isolate all "'s" = r" [^ ]*[^ ]['’]s"

    import re

    all_headlines_list = all_headline_test.split()




    #below removes all apostrophe s's from list made of all headlines string split
    for counter, i in enumerate(all_headlines_list):
        if re.findall(r"[^ ]*[^ ]['’]s", i):

            all_headlines_list[counter] = i[:len(i)-2]


    a = 0


    #remove all nonalphanumeric characters
    for counter,i in enumerate(all_headlines_list):
        if re.findall(r"\W",i):
            if not re.findall(r"-",i):

                new_i = re.sub(r"\W", '', i)
                all_headlines_list[counter] = new_i





    #ies number 1: takes 4 letter words ending with ies and removes s, to take care of cases similar to "dies", "vies", "ties"
    for counter, i in enumerate(all_headlines_list):
        if re.findall(r".*ies$",i):
            if len(i) == 4:

                new_i = i[:len(i)-1]
                all_headlines_list[counter] = new_i


    #ies number 2: end in "ies" but singular ends in "ie"
    for counter, i in enumerate(all_headlines_list):
        if re.findall(r".*ies$",i):
            if i in ["Zombies", "zombies", "Trekkies", "trekkies"]:

                new_i = i[:len(i)-1]
                all_headlines_list[counter] = new_i








    #erase stopwords
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    exceptions_ies = ['series', "Series", "monies", "Monies"]

    for counter, i in enumerate(all_headlines_list):
        if i.lower() in stopwords:
            all_headlines_list[counter] = ''




    #change "ies" plurals to end with "y"
    for counter, i in enumerate(all_headlines_list):
        if i.endswith("ies"):
            if i not in exceptions_ies:
                if len(i) > 4:

                    all_headlines_list[counter] = i[:len(i)-3] + "y"
            else:
                all_headlines_list[counter] = i + "donotdelete"



    #remove s from words ending with "ves"
    for counter, i in enumerate(all_headlines_list):
        if i.endswith("ves"):

            all_headlines_list[counter] = i[:len(i)-1]


    for counter, i in enumerate(all_headlines_list):
        if i.endswith("os"):

            if i.lower() in ['studios', 'photos']:
                all_headlines_list[counter] = i[:len(i)-1]



    #do not touch any words that end in "ess" make this an exception to s taking also "uss"




    for counter, i in enumerate(all_headlines_list):
        if i.endswith("as"):
            if i.lower() not in ['koalas', 'gorillas', 'areas', 'sherpas']:

                all_headlines_list[counter] = i + "donotdelete"



    #add a code to each word that we dont want to shave s off of.




    for counter,i in enumerate(all_headlines_list):
        if i.lower() in ['des', 'moines', 'holmes', 'bynes', 'angeles','philippines', 'nunes', 'thames']:
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if re.findall(r".shes$|.xes$|.sses$|.ches$|.uses$|.usses$", i):
            if i.lower() not in ['accuses', 'excuses']:
                all_headlines_list[counter] = i[:len(i)-2]
            else:
                all_headlines_list[counter] = i[:len(i)-1] + "donotdelete"


    #exceptions, words ending with s that want to flag to not eliminate
    for counter, i in enumerate(all_headlines_list):
        if i.lower() in ['sanders', 'news', 'collins', 'williams']:
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if i.endswith("is"):
            if i.lower() not in ['nazis']:
                all_headlines_list[counter] = i + "donotdelete"
            else:
                all_headlines_list[counter] = i[:len(i)-1]

    for counter, i in enumerate(all_headlines_list):
        if i.endswith("iss"):
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if i.endswith("ass"):
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if i.endswith("os"):
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if i.lower() in ['goes']:
            all_headlines_list[counter] = 'go'

    for counter, i in enumerate(all_headlines_list):
        if re.findall(r".us$|.ess$|.uss$|.ass$", i):
            all_headlines_list[counter] = i + "donotdelete"


    for counter, i in enumerate(all_headlines_list):
        if i.endswith("s"):
            all_headlines_list[counter] = i[:len(i)-1]


    all_headlines_list_lowered = []

    for i in all_headlines_list:
        all_headlines_list_lowered.append(i.lower())

    for counter, i in enumerate(all_headlines_list_lowered):
        if i.endswith("donotdelete"):
            all_headlines_list_lowered[counter] = i[:len(i)-11]

    word_count_dict = {}

    for i in all_headlines_list_lowered:
        if i not in word_count_dict:
            word_count_dict[i] = 1
        else:
            word_count_dict[i] += 1

    word_count_sorted = sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)

    return word_count_sorted


#save all data to database with emotions
for i in nytimeslist:
    headline_string = i[2]
    list_of_words = get_sorted_word_count_by_string_emotion(headline_string)
    emotion_dict = {'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'positive':0, 'negative':0, 'sadness':0, 'disgust':0, 'joy':0}
    for x,y in list_of_words:
        if emotion.objects.filter(word=x):
            emotions_for_word = emotion.objects.filter(word=x).values('fear', 'anger', 'anticip', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy')[0]
            emotion_dict['fear'] += emotions_for_word['fear']
            emotion_dict['anger'] += emotions_for_word['anger']
            emotion_dict['anticip'] += emotions_for_word['anticip']
            emotion_dict['trust'] += emotions_for_word['trust']
            emotion_dict['surprise'] += emotions_for_word['surprise']
            emotion_dict['positive'] += emotions_for_word['positive']
            emotion_dict['negative'] += emotions_for_word['negative']
            emotion_dict['sadness'] += emotions_for_word['sadness']
            emotion_dict['disgust'] += emotions_for_word['disgust']
            emotion_dict['joy'] += emotions_for_word['joy']
    nytimes_emotion = Headline_emotion(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4], reading_level=textstat.text_standard(i[2], float_output=True), headline_wc=len(i[2].split()), fear=emotion_dict['fear'], anger=emotion_dict['anger'], anticip=emotion_dict['anticip'], trust=emotion_dict['trust'], surprise=emotion_dict['surprise'], positive=emotion_dict['positive'], negative=emotion_dict['negative'], sadness=emotion_dict['sadness'], disgust=emotion_dict['disgust'], joy=emotion_dict['joy'], )
    nytimes_emotion.save()

for i in fnlist:
    headline_string = i[2]
    list_of_words = get_sorted_word_count_by_string_emotion(headline_string)
    emotion_dict = {'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'positive':0, 'negative':0, 'sadness':0, 'disgust':0, 'joy':0}
    for x,y in list_of_words:
        if emotion.objects.filter(word=x):
            emotions_for_word = emotion.objects.filter(word=x).values('fear', 'anger', 'anticip', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy')[0]
            emotion_dict['fear'] += emotions_for_word['fear']
            emotion_dict['anger'] += emotions_for_word['anger']
            emotion_dict['anticip'] += emotions_for_word['anticip']
            emotion_dict['trust'] += emotions_for_word['trust']
            emotion_dict['surprise'] += emotions_for_word['surprise']
            emotion_dict['positive'] += emotions_for_word['positive']
            emotion_dict['negative'] += emotions_for_word['negative']
            emotion_dict['sadness'] += emotions_for_word['sadness']
            emotion_dict['disgust'] += emotions_for_word['disgust']
            emotion_dict['joy'] += emotions_for_word['joy']

    foxnews_emotion = Headline_emotion(headline=str(i[2]), newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4], reading_level=textstat.text_standard(str(i[2]), float_output=True), headline_wc=len(str(i[2]).split()), fear=emotion_dict['fear'], anger=emotion_dict['anger'], anticip=emotion_dict['anticip'], trust=emotion_dict['trust'], surprise=emotion_dict['surprise'], positive=emotion_dict['positive'], negative=emotion_dict['negative'], sadness=emotion_dict['sadness'], disgust=emotion_dict['disgust'], joy=emotion_dict['joy'], )
    foxnews_emotion.save()

for i in bbclist:
    headline_string = i[2]
    list_of_words = get_sorted_word_count_by_string_emotion(headline_string)
    emotion_dict = {'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'positive':0, 'negative':0, 'sadness':0, 'disgust':0, 'joy':0}
    for x,y in list_of_words:
        if emotion.objects.filter(word=x):
            emotions_for_word = emotion.objects.filter(word=x).values('fear', 'anger', 'anticip', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy')[0]
            emotion_dict['fear'] += emotions_for_word['fear']
            emotion_dict['anger'] += emotions_for_word['anger']
            emotion_dict['anticip'] += emotions_for_word['anticip']
            emotion_dict['trust'] += emotions_for_word['trust']
            emotion_dict['surprise'] += emotions_for_word['surprise']
            emotion_dict['positive'] += emotions_for_word['positive']
            emotion_dict['negative'] += emotions_for_word['negative']
            emotion_dict['sadness'] += emotions_for_word['sadness']
            emotion_dict['disgust'] += emotions_for_word['disgust']
            emotion_dict['joy'] += emotions_for_word['joy']
    bbc_emotion = Headline_emotion(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1], sentiment=i[4], reading_level=textstat.text_standard(i[2], float_output=True), headline_wc=len(i[2].split()), fear=emotion_dict['fear'], anger=emotion_dict['anger'], anticip=emotion_dict['anticip'], trust=emotion_dict['trust'], surprise=emotion_dict['surprise'], positive=emotion_dict['positive'], negative=emotion_dict['negative'], sadness=emotion_dict['sadness'], disgust=emotion_dict['disgust'], joy=emotion_dict['joy'], )
    bbc_emotion.save()





from datetime import date, timedelta
from textblob import TextBlob
from django.shortcuts import render
from django.utils import timezone
from custom_scraper.models import Headline

today = date.today()
yesterday = date.today() - timedelta(days=1)

import nltk
from nltk.corpus import stopwords

today1 = today
nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
if not nytheadlines:
    nytheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1).filter(day_order__lte=25)

bbcheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=2).filter(day_order__lte=25)
if not bbcheadlines:
    bbcheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2).filter(day_order__lte=25)

fnheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=3).filter(day_order__lte=25)
if not fnheadlines:
    fnheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3).filter(day_order__lte=25)



def find_keywords(headlines):
    stopwords = nltk.corpus.stopwords.words('english')



    headlineslist = []
    for i in headlines:
        headlineslist.append(i.headline)
    headlineslist = " ".join(headlineslist)
    headlineslist = headlineslist.split()
    without_stopwords = []

    for i in headlineslist:
        if i.lower() not in stopwords:

            without_stopwords.append(i)

    without_stopwords_string = " ".join(without_stopwords)

    texta = TextBlob(without_stopwords_string)

    a = texta.word_counts

    nytimes_word_count_list = []
    for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
        interlist = []
        if key != "s" and key != "’" and key != "‘":
            interlist.append(value)
            interlist.append(key)
            nytimes_word_count_list.append(interlist)
    return nytimes_word_count_list



allkeywords = nytheadlines | bbcheadlines | fnheadlines
allkeywords = find_keywords(allkeywords)

nykeywords = find_keywords(nytheadlines)
bbckeywords = find_keywords(bbcheadlines)
fnkeywords = find_keywords(fnheadlines)


all_wf_keys = []
all_wf_values = []
keyword_counter = 0
for v in allkeywords:
    if keyword_counter < 5:
        all_wf_values.append(v[0])
        all_wf_keys.append(v[1])
    keyword_counter += 1

key1 = all_wf_keys[0]
freq1 = all_wf_values[0]
key2 = all_wf_keys[1]
freq2 = all_wf_values[1]
key3 = all_wf_keys[2]
freq3 = all_wf_values[2]

from requests_html import HTMLSession






from django.db.models import Avg


def find_positive(paper_num):
        all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

        all_headline_string = ""

        for i in all_headlines:
            all_headline_string += " " + i['headline']


        import nltk
        from nltk import FreqDist
        from nltk.corpus import stopwords
        stopword = stopwords.words('english')
        text = all_headline_string
        word_tokens = nltk.word_tokenize(text.lower())
        removing_stopwords = [word for word in word_tokens if word not in stopword]
        freq = FreqDist(removing_stopwords)
        most_common = freq.most_common(500)

        list_of_top_words = []

        for i in most_common:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            list_of_top_words.append(interlist)



        exceptions = [',',':',"'",'.','?', "'s", '‘', "n't", '’']

        top_words = []

        for i in list_of_top_words:
            if i[0] not in exceptions:
                interlist = []
                interlist.append(i[0])
                interlist.append(i[1])
                top_words.append(interlist)





        overall_words = []
        for i in top_words:
            overall_words.append(i)



        for i in overall_words:
            paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
            i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





        best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
        worst_words = sorted(overall_words, key = lambda x: x[2],)

        best_and_worst = []
        best_and_worst.append(best_words[:100])
        best_and_worst.append(worst_words[:100])

        return best_and_worst



nyt_words = find_positive(1)
nyt_best_words = nyt_words[0]
nyt_worst_words = nyt_words[1]

bbc_words = find_positive(2)
bbc_best_words = bbc_words[0]
bbc_worst_words = bbc_words[1]

fn_words = find_positive(3)
fn_best_words = fn_words[0]
fn_worst_words = fn_words[1]

print(nyt_best_words)

from custom_scraper.models import superlative_table



for i in nyt_best_words:
  save_to_db = superlative_table(graphid=1, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in bbc_best_words:
  save_to_db = superlative_table(graphid=1, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in fn_best_words:
  save_to_db = superlative_table(graphid=1, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in nyt_worst_words:
  save_to_db = superlative_table(graphid=2, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in bbc_worst_words:
  save_to_db = superlative_table(graphid=2, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in fn_worst_words:
  save_to_db = superlative_table(graphid=2, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()





def find_people(paper_num):
    all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

    all_headline_string = ""

    for i in all_headlines:
        all_headline_string += " " + i['headline']


    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(300)

    list_of_top_words = []

    for i in most_common:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)



    exceptions = ['tax', 'list','meet', 'vaccines','capitol', 'border', 'riot', 'scandal', 'nursing', 'decision', "'it", 'told', 'thousands', 'portland', 'legal', 'officers', 'chicago', 'getting', 'senator', 'biggest', 'office', 'convention', 'policy','republican', 'supporters', 'accused', 'riots', 'fires', 'talks', 'future', 'votes', 'christmas', 'early', 'become', 'keep', 'voting', 'thanksgiving', 'fraud', 'pennsylvania', 'general', 'polls', 'town', '10', 'moment', 'trade', 'tiktok', 'capital', 'final', 'lead',   'climate', 'pick',  'georgia', 'worse', 'democrat', 'run', 'warning', 'crime',  'fbi', 'due', 'game', 'explains', 'reacts', 'daughter', 'responds', 'jail', 'nypd',  'baby', 'boy', 'symptoms', 'afghan', 'eu', 'visual', 'isolation', 'italian', 'tracking', 'denies', 'israel', 'french', 'australian', 'abuse', 'theme', 'suspect', 'turkey', 'brazil', 'arrest', 'aged', 'london', 'harry', 'since', 'mental' , 'delhi', '-', 'speech', '&', 'impact', 'vp', "–",   'cnn', 'calling',      'distancing', 'saved', 'german', 'boss', 'australia', 'four', 'ca', 'huge', 'largest', 'england', 'photo', 'sea', 'passes', 'row', 'indian', 'ways',   'cdc', 'announces', 'issues', 'nfl', 'massive', 'comments', 'owner', 'dc', '-',       '...', 'begins', 'jailed', "'my", 'minister', 'queen', "'ve", 'reopens', 'largest'   'huge', 'shots', 'tips', 'rare', 'birthday', 'app', 'storm', 'returns',     'politics', 'c.d.c', 'finally', 'street', 'g.o.p', 'outbreaks', 'shots',         'hot', 'defense', 'control', 'facing', 'billion', 'schools', 'summer',    'w.h.o',          'coverage', 'providing', 'love', 'read', 'everyone', 'trillion', 'rich', 'region', 'rights', 'region', 'rights','threatens', '5', 'japan', 'moves', '(', ')', 'happened', 'already', 'became', 'nearly',      ',',':',"'",'.','?', "'s", '‘', "n't", '’', 'better', 'mike', 'hospitals', 'andrew', 'event', 'orders', 'tech', 'past','coronavirus', 'us', 'new', 'virus', 'says', 'george',  'china', 'police', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.', 'president', 'amid', 'york', 'death', 'america', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'state', 'man', 'news', '$', 'black', 'outbreak', 'people', 'city', 'back', 'one', 'joe', 'health', 'may', 'first', 'democrats', 'americans', 'white', 'media', '2020', 'take', 'life', 'time', 'updates', 'protests', 'report', 'get', 'calls', 'fight', 'help', '-', 'dr.', 'states', 'global', 'dies', 'response', 'day', 'say', 'case', 'american', 'week', 'bill', ';', 'deaths', 'workers', 'face', 'like', 'dems', 'top', 'see', 'campaign', 'claims', 'economy', 'race', 'court', 'super', 'judge', 'big', 'bbc', 'dead', 'test', 'protesters', 'show', 'india', 'iowa', 'make', 'want', 'reopen', 'still', 'live', 'found', 'go', 'would', 'quarantine', 'masks', 'south', 'work', 'election', 'need', 'democratic', 'vote', 'rep.', 'gov', 'sen.', 'california', 'rally', 'trial', 'plan', 'reopening', 'best', 'toll', 'law', 'vaccine', 'deal', 'travel', 'italy', 'spread', 'impeachment', 'woman', 'women', 'killed', 'end', 'mayor', 'warns', 'last', 'years', 'behind', 'care', 'debate', 'country', 'protest', 'russia', 'know', 'video', 'family', 'attack', 'war', 'quiz', 'senate', 'officials', 'going', 'fears', 'star', 'two', 'inside', 'pictures', 'next', 'former', 'service', 'covid', 'follow', 'voters', 'business', 'children', "'we", 'murder', 'stop', 'chief', 'national', 'testing', 'set', 'hospital', 'ahead', 'primary', 'tells', 'party', 'justice', 'shooting', 'europe', 'briefing', 'much', '2', 'economic', '3', 'tv', 'days', 'korea', 'iran', 'dem', 'win', 'mass', 'free', 'bowl', 'call', 'history', 'million', 'social', 'aid', 'lives', 'order', 'hits', 'five', 'many', 'michael', 'faces', 'rise', 'weekend', 'times', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'hong', 'kong', 'florida', 'supreme', 'chinese', 'doctor', 'charged', 'force', 'governor', 'takes', 'change', 'record', 'exclusive', 'stimulus', 'public', 'facebook', 'listen', 'twitter', 'hit', 'open', 'story', 'official', 'good', 'despite', 'leader', 'mother', 'tuesday', 'year', 'never', 'gives', 'gop', 'john', 'military', 'way', 'arrested', 'spreads', 'online', 'radio', 'got', 'reveals', 'save', 'stay', 'slams', 'africa', 'job', 'wants', 'texas', 'away', 'oil', 'ny', 'relief', 'markets', 'return', 'must', 'making', 'gets', 'long', 'start', 'rules', 'even', 'fall', 'fire', 'makes', 'look', 'latest', 'ban', 'risk', 'doctors', 'surge', 'use', 'food', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'russian', '11', 'federal', 'restrictions', 'cut', 'headlines', 'team', 'key', 'missing', 'kobe', 'probe', 'guide', 'mask', "'the", 'amazon', 'another', 'presidential', 'system', 'think', 'blasts', 'political', 'minneapolis', 'wuhan', 'reports', 'wins', 'lost', 'students', 'mark', 'move', 'kids', 'countries', 'changed', 'close', 'pm', 'shot', 'cities', 'safe', 'medical', 'study', 'seattle', 'made', 'ever', 'ship', 'threat', 'analysis', 'young', 'find', 'france',  'across', 'racism', 'die', 'patients', 'around', 'spain', 'goes', 'everything', 'wrong', 'real', 'washington', 'matter', 'government', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'died', 'deadly', 'left', 'experts', 'come', 'market', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'second', 'mr.', 'chris', 'administration', 'cops', 'wall', 'really', 'might', 'hampshire', 'jobs', 'de', 'germany', 'night', 'memorial', 'stocks', 'cathedral', 'businesses', 'nation', 'small', 'months', 'son', 'near', 'major', 'tom', 'trying', 'problem', 'coming', 'let', 'sign', 'turn', 'give', 'elizabeth', '4', 'seen', 'action', 'plans', 'west', 'father', 'secret', 'candidate', 'sick', 'prison', 'carolina', 'doj', 'message', 'reads', 'patrick', 'secretary', 'union', '!', 'canada', 'tweet', 'caucuses', 'meghan', 'crash', 'taking', 'things', 'stars', 'couple', 'needs', 'congress', 'school', 'power', 'staff', 'hope', 'violence', 'access', 'unrest',  'clash', '“', '”', 'far', 'girl', 'leaves', 'questions', 'six', 'today', 'pay', 'support', 'book', 'leaders', 'fighting', "'re", 'money', '1', 'officer', 'claim', 'release', 'without', 'church', 'concerns' ]

    top_words = []



    for i in list_of_top_words:
        if i[0] not in exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_words.append(interlist)





    overall_words = []
    for i in top_words:
        overall_words.append(i)



    for i in overall_words:
        paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
        i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))






    best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
    worst_words = sorted(overall_words, key = lambda x: x[2],)

    best_and_worst = []
    best_and_worst.append(best_words)
    best_and_worst.append(worst_words[:20])
    best_and_worst.append(exceptions)

    return best_and_worst

nyt_people = find_people(1)
nyt_best_people = nyt_people[0]

bbc_people = find_people(2)
bbc_best_people = bbc_people[0]

fn_people = find_people(3)
fn_best_people = fn_people[0]

people_exceptions = nyt_people[2]

print(nyt_best_people)

for i in nyt_best_people:
  save_to_db = superlative_table(graphid=3, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in bbc_best_people:
  save_to_db = superlative_table(graphid=3, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in fn_best_people:
  save_to_db = superlative_table(graphid=3, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()


def find_places(paper_num):
    all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

    all_headline_string = ""

    for i in all_headlines:
        all_headline_string += " " + i['headline']


    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(300)

    list_of_top_words = []

    for i in most_common:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)



    exceptions = [ 'tax', 'list', 'meet', 'rights', 'capitol', 'riot', 'scandal', 'nursing',   "'it", 'officers', 'decision', "", 'talks', 'coney', 'getting', 'senator', 'biggest', 'office', 'convention', 'policy', 'told', 'thousands', 'legal', 'harris', 'future', 'amy', 'barrett', 'hunter', 'supporters', 'accused', 'king', 'riots', 'fires','general', 'polls', '10', 'mcconnell', 'moment', 'trade', 'tiktok', 'kamala', 'final', 'lead', 'republican', 'votes', 'christmas', 'early', 'become', 'keep', 'voting', 'thanksgiving', 'fraud', 'climate', 'pick', 'crime', 'stone', 'democrat', 'run', 'worse' , 'warning',  'mental', 'theme', 'suspect', 'arrest', 'aged', 'harry', 'since',   'visual', 'isolation', 'tracking', 'denies', 'abuse',  'due', 'schumer', 'game', 'jail', 'gutfeld', 'nypd', 'fbi', 'mom',  'clinton', 'graham', 'texas', 'responds', 'wife', 'calling', 'explains', 'reacts', 'daughter',  "&", 'impact', 'vp', 'gingrich', 'cnn', 'mccarthy', 'mcenany',  'owner', "n't", "–", 'speech',    'pence', 'cdc', 'announces', 'issues', 'nfl', 'massive', 'comments', "'s", "'",'boss', 'boy', 'symptoms', 'boss', 'four', 'ca', 'baby', 'ways', 'distancing', 'saved',   "'ve", 'reopens', 'largest', 'photo', 'sea', 'passes', 'row', 'minister', 'queen', 'storm', 'returns', '...', 'begins', 'jailed', "'my" ,  'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app',    'donald','outbreaks', 'w.h.o', 'c.d.c', 'finally', 'street', 'g.o.p',        '.',':', 'schools', '?' , "’", ",", "summer", "‘",      'politics', 'hot', 'defense', 'control', 'facing', 'billion',      'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became',            'better', 'mike', 'hospitals', 'andrew', 'event', 'orders', 'tech', 'past','coronavirus', 'trump', 'us', 'new', 'virus', 'says', 'biden', 'police', 'covid-19', 'pandemic', 'lockdown', 'world', 'president', 'amid', 'death', 'sanders', 'could', 'crisis', 'cases', 'home', 'house', 'state', 'man', 'news', '$', 'black', 'outbreak', 'people', 'city', 'back', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'democrats', 'white', 'floyd', 'media', '2020', 'take', 'life', 'time', 'updates', 'protests', 'report', 'get', 'calls', 'fight', 'help', '-', 'dr.', 'states', 'dies', 'response', 'day', 'say', 'george', 'case',  'week', 'bill', ';', 'deaths', 'workers', 'face', 'like', 'dems', 'top', 'bloomberg', 'see', 'campaign', 'claims', 'economy', 'race', 'court', 'super', 'judge', 'big', 'bbc', 'dead', 'test', 'protesters', 'show', 'make', 'want', 'reopen', 'still', 'live', 'obama', 'found', 'go', 'flynn', 'would', 'quarantine', 'masks', 'south', 'work', 'election', 'need', 'democratic', 'vote', 'rep.', 'gov', 'sen.', 'rally', 'trial', 'plan', 'reopening', 'best', 'toll', 'law', 'vaccine', 'deal', 'travel', 'spread', 'impeachment', 'woman', 'women', 'killed', 'end', 'mayor', 'warns', 'last', 'years', 'behind', 'care', 'debate', 'country', 'protest', 'know', 'video', 'family', 'attack', 'war', 'quiz', 'senate', 'officials', 'going', 'fears', 'star', 'two', 'inside', 'pictures', 'next', 'former', 'service', 'pelosi', 'covid', 'follow', 'voters', 'business', 'children', "'we", 'murder', 'stop', 'chief', 'national', 'testing', 'set', 'warren', 'hospital', 'ahead', 'primary', 'tells', 'party', 'justice', 'shooting', 'briefing', 'much', '2', 'economic', '3', 'tv', 'days', 'dem', 'win', 'mass', 'free', 'bowl', 'call', 'history', 'million', 'social', 'aid', 'lives', 'order', 'hits', 'five', 'many', 'michael', 'tucker', 'hannity', 'faces', 'cuomo', 'rise', 'weekend', 'times', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'kong', 'supreme', 'doctor', 'charged', 'force', 'governor', 'takes', 'change', 'record', 'exclusive', 'buttigieg', 'stimulus', 'public', 'facebook', 'bolton', 'listen', 'twitter', 'hit', 'open', 'story', 'official', 'good', 'despite', 'leader', 'mother', 'tuesday', 'year', 'never', 'gives', 'gop', 'john', 'military', 'way', 'arrested', 'spreads', 'online', 'radio', 'got', 'reveals', 'save', 'stay', 'slams', 'job', 'wants', 'away', 'oil', 'barr', 'relief', 'markets', 'return', 'must', 'making', 'gets', 'long', 'start', 'rules', 'even', 'fall', 'fire', 'bryant', 'makes', 'look', 'latest', 'ban', 'risk', 'doctors', 'surge', 'use', 'food', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', '11', 'federal', 'restrictions', 'cut', 'headlines', 'team', 'key', 'missing', 'kobe', 'probe', 'guide', 'mask', "'the", 'amazon', 'another', 'presidential', 'system', 'think', 'blasts', 'political', 'minneapolis', 'reports', 'wins', 'lost', 'students', 'mark', 'move', 'kids', 'countries', 'changed', 'close', 'pm', 'shot', 'cities', 'safe', 'medical', 'study', 'made', 'ever', 'ship', 'threat', 'analysis', 'young', 'find', 'france', 'weinstein', 'across', 'racism', 'die', 'patients', 'around',  'goes', 'everything', 'wrong', 'aoc', 'real', 'matter', 'government', 'reform', 'said', 'attacks', 'kill', 'tests', 'bad',  'died', 'deadly', 'left', 'experts', 'come', 'market', 'possible', 'point', 'johnson', 'mean', 'worst', 'results', 'drug', 'north', 'sex', 'positive', 'daily', 'shows', 'cruise', 'great', 'college', 'second', 'mr.', 'chris', 'administration', 'cops', 'wall', 'really', 'might',  'jobs', 'de', 'night', 'memorial', 'stocks', 'cathedral', 'businesses', 'nation', 'small', 'months', 'son', 'near', 'major', 'tom', 'trying', 'problem', 'coming', 'let', 'newt', 'blasio', 'sign', 'turn', 'give', 'elizabeth', '4', 'seen', 'action', 'plans', 'father', 'secret', 'candidate', 'sick', 'prison', 'doj', 'message', 'reads', 'patrick', 'secretary', 'union', '!', 'tweet', 'caucuses', 'meghan', 'crash', 'taking', 'things', 'stars', 'couple', 'needs', 'congress', 'school', 'power', 'staff', 'hope', 'violence', 'access', 'fauci', 'unrest', 'pompeo', 'clash', '“', '”', 'far', 'girl', 'leaves', 'questions', 'six', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'fighting', "'re", 'money', '1', 'officer', 'claim', 'release', 'without', 'siegel', 'church', 'concerns']

    top_words = []



    for i in list_of_top_words:
        if i[0] not in exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_words.append(interlist)





    overall_words = []
    for i in top_words:
        overall_words.append(i)



    for i in overall_words:
        paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
        i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





    best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
    worst_words = sorted(overall_words, key = lambda x: x[2],)

    best_and_worst = []
    best_and_worst.append(best_words)
    best_and_worst.append(worst_words[:20])
    best_and_worst.append(exceptions)

    return best_and_worst

nyt_places = find_places(1)
bbc_places = find_places(2)
fn_places = find_places(3)

nyt_best_places = nyt_places[0]


bbc_best_places = bbc_places[0]


fn_best_places = fn_places[0]

place_exceptions = nyt_places[2]

for i in nyt_best_places:
  save_to_db = superlative_table(graphid=4, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in bbc_best_places:
  save_to_db = superlative_table(graphid=4, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in fn_best_places:
  save_to_db = superlative_table(graphid=4, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()



def find_politics(paper_num):
    all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

    all_headline_string = ""

    for i in all_headlines:
        all_headline_string += " " + i['headline']


    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(300)

    list_of_top_words = []

    for i in most_common:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)


    exceptions = ['list', 'taylor', 'meet', 'nursing', "'it",'biggest', 'office', 'convention', 'told', 'thousands', 'portland', 'chicago', 'decision', 'tiktok', 'kamala', 'final', 'lead', 'harris', 'future', 'amy', 'barrett', 'coney', 'hunter', 'accused', 'fires', 'getting', 'christmas', 'early', 'become', 'keep', 'thanksgiving', 'fraud', 'pennsylvania', 'pick', 'general', 'town', '10', 'mcconnell', 'moment', 'worse', 'warning',  'stone', 'georgia', 'worse', 'run', 'past',    'wife', 'jail', 'gutfeld', 'fbi', 'mom', 'due', 'schumer', 'game',  'street', 'outbreaks',   'reacts', 'daughter', 'graham', 'responds',  'cnn', 'doj', 'mccarthy', 'calling', 'explains',   'dc',  'gingrich', 'vp', 'impact', '&', 'speech', 'mcenany', 'law', "–",   'pence', 'clinton', 'cdc', 'announces', 'issues', 'nfl', 'massive', 'comments', 'owner', 'event',    'since','japan', 'harry', 'mental', 'delhi',  'aged', 'judge', 'london',  'australian', 'abuse', 'theme', 'suspect', 'media', 'turkey', 'brazil', 'arrest',  'italian', 'tracking', 'denies', 'israel', 'french',  'boy', 'symptoms', "'" , "'s", "afghan", 'eu', "n't", "visual", 'isolation',    'distancing', 'saved', 'german', 'boss', 'australia', 'four', 'ca', 'baby',   'england', 'photo', 'sea', 'passes', 'row', 'indian', 'orders', 'ways',  '...', 'begins', 'vote', 'jailed', "'my", 'minister', "'ve", 'reopens', 'largest',     'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app', 'storm', 'returns',     'finally', 'c.d.c',  'donald',  'tech', "‘", 'debate', 'w.h.o',   ".", ":", "schools", "?", "’", "," , 'summer',   'billion', 'trial',  'hot', 'defense', 'hospitals', 'control', 'facing',  'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became',  'better', 'mike','coronavirus', 'trump', 'us', 'new', 'virus', 'says', 'biden', 'china', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.',  'amid', 'york', 'death', 'america', 'sanders', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'state', 'man', 'news', '$', 'black', 'outbreak', 'people', 'city', 'back', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'americans', 'white', 'floyd', '2020', 'take', 'life', 'time', 'updates', 'report', 'get', 'calls', 'fight', 'help', '-', 'dr.', 'states', 'global', 'dies', 'response', 'day', 'say', 'george', 'case', 'american', 'week', 'bill', ';', 'deaths', 'face', 'like',  'top', 'bloomberg', 'see', 'claims', 'race', 'court', 'super', 'big', 'bbc', 'dead', 'test', 'show', 'india', 'iowa', 'make', 'want', 'reopen', 'still', 'live', 'obama', 'found', 'go', 'flynn', 'would', 'quarantine', 'masks', 'south', 'work', 'need', 'california', 'plan', 'reopening', 'best', 'toll', 'vaccine', 'deal', 'travel', 'italy', 'spread', 'woman', 'women', 'killed', 'end', 'warns', 'last', 'years', 'behind', 'care', 'country', 'protest', 'russia', 'know', 'video', 'family', 'attack', 'quiz',  'going', 'fears', 'star', 'two', 'inside', 'pictures', 'next', 'former', 'service', 'pelosi', 'covid', 'follow', 'business', 'children', "'we", 'murder', 'stop', 'chief', 'national', 'testing', 'set', 'warren', 'hospital', 'ahead', 'primary', 'tells', 'party', 'justice', 'shooting', 'europe', 'briefing', 'much', '2', '3', 'tv', 'days', 'korea', 'iran', 'win', 'mass', 'free', 'bowl', 'call', 'history', 'million', 'social', 'aid', 'lives', 'order', 'hits', 'five', 'many', 'michael', 'tucker', 'hannity', 'faces', 'cuomo', 'rise', 'weekend', 'times', 'watch', 'fox', 'fear', 'three', 'right', 'hong', 'kong', 'florida', 'supreme', 'chinese', 'doctor', 'charged', 'force', 'governor', 'takes', 'change', 'record', 'exclusive', 'buttigieg', 'stimulus', 'public', 'facebook', 'bolton', 'listen', 'twitter', 'hit', 'open', 'story', 'official', 'good', 'despite', 'leader', 'mother', 'tuesday', 'year', 'never', 'gives',  'john', 'military', 'way', 'arrested', 'spreads', 'online', 'radio', 'got', 'reveals', 'save', 'stay', 'slams', 'africa', 'job', 'wants', 'texas', 'away', 'oil', 'ny', 'barr', 'relief', 'markets', 'return', 'must', 'making', 'gets', 'long', 'start', 'rules', 'even', 'fall', 'fire', 'bryant', 'makes', 'look', 'latest', 'ban', 'risk', 'doctors', 'surge', 'use', 'food', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'russian', '11', 'federal', 'restrictions', 'cut', 'headlines', 'team', 'key', 'missing', 'kobe', 'probe', 'guide', 'mask', "'the", 'amazon', 'another', 'presidential', 'system', 'think', 'blasts', 'political', 'minneapolis', 'wuhan', 'reports', 'wins', 'lost', 'students', 'mark', 'move', 'kids', 'countries', 'changed', 'close', 'pm', 'shot', 'cities', 'safe', 'medical', 'study', 'seattle', 'made', 'ever', 'ship', 'threat', 'analysis', 'young', 'find', 'france', 'weinstein', 'across', 'racism', 'die', 'patients', 'around', 'spain', 'goes', 'everything', 'wrong', 'aoc', 'real', 'washington', 'matter', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'died', 'deadly', 'left', 'experts', 'come', 'market', 'possible', 'point', 'johnson', 'mean', 'worst', 'results', 'drug', 'north', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'second', 'mr.', 'chris', 'administration', 'cops', 'wall', 'really', 'might', 'hampshire', 'jobs', 'de', 'germany', 'night', 'memorial', 'stocks', 'cathedral', 'businesses', 'nation', 'small', 'months', 'son', 'near', 'major', 'tom', 'trying', 'problem', 'coming', 'let', 'newt', 'blasio', 'sign', 'turn', 'give', 'elizabeth', '4', 'seen', 'action', 'plans', 'west', 'father', 'secret', 'candidate', 'sick', 'prison', 'carolina', 'message', 'reads', 'patrick', 'secretary', 'union', '!', 'canada', 'tweet', 'caucuses', 'meghan', 'crash', 'taking', 'things', 'stars', 'couple', 'needs', 'school', 'power', 'staff', 'hope', 'violence', 'access', 'fauci', 'unrest', 'pompeo', 'clash', '“', '”', 'far', 'girl', 'leaves', 'questions', 'six', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'fighting', "'re", 'money', '1', 'officer', 'claim', 'release', 'without', 'siegel', 'church', 'concerns']


    top_words = []



    for i in list_of_top_words:
        if i[0] not in exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_words.append(interlist)





    overall_words = []
    for i in top_words:
        overall_words.append(i)



    for i in overall_words:
        paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
        i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





    best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
    worst_words = sorted(overall_words, key = lambda x: x[2],)

    best_and_worst = []
    best_and_worst.append(best_words)
    best_and_worst.append(worst_words[:20])
    best_and_worst.append(exceptions)

    return best_and_worst

nyt_politics = find_politics(1)
bbc_politics = find_politics(2)
fn_politics = find_politics(3)

nyt_politics_words = nyt_politics[0]
bbc_politics_words = bbc_politics[0]
fn_politics_words = fn_politics[0]
politics_exceptions = nyt_politics[2]

print(nyt_politics_words)

for i in nyt_politics_words:
  save_to_db = superlative_table(graphid=5, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in bbc_politics_words:
  save_to_db = superlative_table(graphid=5, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in fn_politics_words:
  save_to_db = superlative_table(graphid=5, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()



def find_economic(paper_num):
    all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

    all_headline_string = ""

    for i in all_headlines:
        all_headline_string += " " + i['headline']


    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(300)

    list_of_top_words = []

    for i in most_common:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)


    exceptions = [ 'voting', 'thanksgiving', 'pennsylvania', 'pick', 'town', '10', 'list', 'mcconnell', 'moment', 'taylor', 'meet', 'rights', 'riot', 'scandal', 'nursing', 'votes', 'christmas', 'early', 'become', "'re", 'keep', 'thousands', 'portland', 'legal', 'officers', 'chicago', 'officer', 'decision', "'it",'king', 'riots', 'fires', 'talks', 'getting', 'senator', 'biggest', 'office', 'convention', 'told', 'tiktok', 'capitol', 'kamala', 'final', 'lead', 'republican', 'harris', 'future', 'amy', 'barrett', 'coney', 'hunter', 'supporters', 'accused', 'warning', 'crime', 'georgia', 'stone', 'worse', 'democrat', 'run', 'jail', 'gutfeld', 'nypd', 'fbi', 'mom', 'due', 'schumer', 'game',  'calling', 'explains', 'reacts', 'daughter', 'graham', 'responds', 'wife',   'speech', '&', 'impact', 'vp', 'claim', 'gingrich', 'cnn', 'mccarthy',  'massive', 'comments', 'owner', 'siegel', 'dc', "–", 'mcenany',    'pence', 'concerns', 'clinton', 'cdc', 'announces', 'issues', 'nfl',  'since', 'mental', 'delhi',  'suspect', 'turkey', 'brazil', 'arrest', 'aged', 'london', 'japan', 'harry',  'tracking', 'denies', 'israel', 'french', 'australian', 'abuse', 'theme',  'italian', 'tracking', 'denies',   'boy', 'symptoms', "'",  "'s", 'afghan', 'eu', "n't", 'visual', 'isolation',   'ways', 'distancing', 'saved', 'german', 'boss', 'australia', 'four', 'ca', 'baby',   'reopens', 'largest', 'england', 'photo', 'sea', 'passes', 'row', 'indian',   '...', 'begins', 'jailed', "'my", 'minister', 'queen', "'ve", 'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app', 'storm', 'returns',   'g.o.p', 'street', 'outbreaks',   'schools', '?', 'job', "’",",", 'summer',"‘", 'w.h.o', 'donald', 'c.d.c', 'finally',     'politics', 'hot', 'defense', 'control', 'facing', '.', 'without', ':',   'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became',    'coronavirus', 'trump', 'us', 'new', 'virus', 'says', 'biden', 'china', 'police', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.', 'president', 'amid', 'death', 'york', 'america', 'sanders', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'man', 'state', 'black', 'news', 'outbreak', 'people', 'back', 'city', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'democrats', 'white', 'americans', 'floyd', '2020', 'media', 'take', 'life', 'updates', 'time', 'protests', 'report', 'get', 'calls', 'fight', 'help', 'day', 'dies', 'american', '-', 'dr.', 'say', 'global', 'states', 'response', 'case', 'george', 'week', ';', 'bill', 'like', 'face', 'deaths', 'campaign', 'dems', 'see', 'top', 'bloomberg', 'court', 'race', 'claims', 'dead', 'super', 'big', 'judge', 'bbc', 'test', 'protesters', 'show', 'make', 'india', 'iowa', 'want', 'reopen', 'still', 'live', 'masks', 'found', 'go', 'obama', 'would', 'south', 'flynn', 'election', 'quarantine', 'work', 'need', 'democratic', 'vote', 'rep.', 'california', 'gov', 'best', 'sen.', 'rally', 'reopening', 'trial', 'killed', 'plan', 'toll', 'mayor', 'woman', 'women', 'law', 'vaccine', 'deal', 'years', 'travel', 'end', 'care', 'italy', 'spread', 'impeachment', 'warns', 'last', 'behind', 'debate', 'country', 'protest', 'quiz', 'know', 'attack', 'russia', 'video', 'family', 'star', 'war', 'senate', 'service', 'two', 'officials', 'going', 'pictures', 'next', 'covid', 'follow', 'fears', 'former', 'inside', 'voters', 'pelosi', 'national', 'children', 'chief', 'ahead', "'we", 'murder', 'stop', 'justice', 'testing', 'set', 'warren', 'tells', 'hospital', 'primary', 'win', 'party', 'shooting', '2', '3', 'tv', 'europe', 'briefing', 'much', 'history', 'days', 'korea', 'weekend', 'iran', 'dem', 'many', 'mass', 'free', 'lives', 'order', 'bowl', 'hits', 'call', 'supreme', 'million', 'social', 'michael', 'aid', 'five', 'tucker', 'rise', 'times', 'hong', 'kong', 'florida', 'chinese', 'hannity', 'faces', 'cuomo', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'record', 'doctor', 'charged', 'force', 'governor', 'story', 'takes', 'change', 'exclusive', 'buttigieg', 'public', 'gives', 'facebook', 'gop', 'bolton', 'listen', 'military', 'official', 'away', 'twitter', 'hit', 'open', 'year', 'never', 'way', 'good', 'despite', 'leader', 'mother', 'tuesday', 'john', 'arrested', 'spreads', 'online', 'radio', 'texas', 'got', 'reveals', 'save', 'start', 'stay', 'return', 'slams', 'africa', 'wants', 'ny', '11', 'barr', 'relief', 'must', 'making', 'makes', 'gets', 'long', 'rules', 'even', 'food', 'headlines', 'fall', 'fire', 'bryant', 'look', 'latest', 'ban', 'mask', 'risk', 'russian', 'doctors', 'presidential', 'surge', 'system', 'use', 'security', 'battle', 'killing', 'push', 'emergency', 'another', 'cities', 'think', 'safe', 'blasts', 'federal', 'restrictions', 'cut', 'seattle', 'made', 'team', 'reports', 'key', 'missing', 'lost', 'kobe', '4', 'move', 'probe', 'guide', 'countries', "'the", 'amazon', 'shot', 'racism', 'political', 'minneapolis', 'wuhan', 'wins', 'students', 'threat', 'left', 'mark', 'kids', 'changed', 'close', 'pm', 'medical', 'study', 'around', 'spain', 'ever', 'ship', 'wrong', 'analysis', 'young', 'find', 'washington', 'france', 'government', 'weinstein', 'across', 'die', 'patients', 'goes', 'everything', 'deadly', 'aoc', 'real', 'west', 'experts', 'matter', 'johnson', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'nation', 'died', 'son', 'come', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'night', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'months', 'second', 'mr.', 'chris', 'administration', 'father', 'needs', 'cops', 'major', 'wall', 'problem', 'really', 'might', 'hampshire', 'newt', 'jobs', 'de', 'germany', 'turn', 'message', 'memorial', 'cathedral', 'reads', 'businesses', 'give', '!', 'small', 'plans', 'event', 'near', 'secret', 'tom', 'trying', 'staff', 'coming', 'let', 'carolina', 'blasio', 'sign', 'unrest', 'secretary', 'elizabeth', 'union', 'seen', 'action', 'candidate', 'sick', 'church', 'prison', 'doj', 'patrick', '“', '”', 'canada', 'past', 'girl', 'leaves', 'tweet', 'caucuses', 'questions', 'meghan', 'crash', 'six', 'taking', 'things', 'stars', 'couple', 'congress', 'school', 'orders', '1', 'power', 'hospitals', 'hope', 'violence', 'access', 'fauci', 'mike', 'pompeo', 'clash', 'far', 'better', 'andrew', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'tech', 'fighting']


    top_words = []



    for i in list_of_top_words:
        if i[0] not in exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_words.append(interlist)





    overall_words = []
    for i in top_words:
        overall_words.append(i)



    for i in overall_words:
        paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
        i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





    best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
    worst_words = sorted(overall_words, key = lambda x: x[2],)

    best_and_worst = []
    best_and_worst.append(best_words)
    best_and_worst.append(worst_words[:20])
    best_and_worst.append(exceptions)

    return best_and_worst

nyt_economic = find_economic(1)
bbc_economic = find_economic(2)
fn_economic = find_economic(3)

nyt_economic_words = nyt_economic[0]
bbc_economic_words = bbc_economic[0]
fn_economic_words = fn_economic[0]
economics_exceptions = nyt_economic[2]

for i in nyt_economic_words:
  save_to_db = superlative_table(graphid=6, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in bbc_economic_words:
  save_to_db = superlative_table(graphid=6, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in fn_economic_words:
  save_to_db = superlative_table(graphid=6, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()


def find_corona(paper_num):
    all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

    all_headline_string = ""

    for i in all_headlines:
        all_headline_string += " " + i['headline']


    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(300)

    list_of_top_words = []

    for i in most_common:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)


    exceptions = ['tax', 'list', 'taylor', 'meet', 'kamala', 'harris', 'senator', 'biggest', 'office', 'convention', 'told', 'thousands', 'portland', 'legal', 'officers', 'chicago', 'decision', "'it",'hunter', 'supporters', 'king', 'riots', 'fires', 'talks', 'getting',  'tiktok', 'capitol', 'final', 'lead', 'republican', 'future', 'amy', 'barrett', 'coney',  'polls', 'town', '10', 'mcconnell', 'moment', 'trade',  'votes', 'christmas', 'early', 'become', "'re", 'keep', 'voting', 'thanksgiving', 'fraud', 'pennsylvania', 'climate', 'pick', 'general', 'warning',  'crime', 'georgia', 'worse', 'run', 'democrat',   'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app', 'storm', 'returns', '', '...', 'begins', 'jailed', "", "'my", 'queen', "'ve", 'largest', 'england', 'photo', 'sea', 'passes', 'row', 'indian', 'ways', 'saved', 'german', 'boss', 'minister', 'australia', 'four', 'ca', 'baby', 'boy', "'", "'s", 'afghan', 'eu', "n't", 'visual', 'denies', 'music', 'israel', 'french', 'australian', 'abuse', 'theme', 'suspect', 'turkey', 'brazil', 'arrest', 'aged', 'london', 'japan', 'harry', 'since', 'mental', 'delhi', 'concerns', 'clinton', 'announces', 'issues', 'nfl', 'comments', 'owner', 'siegel', 'dc',  '–', 'mcenany', 'speech', '&', 'impact', 'vp', 'claim', 'gingrich', 'accused', 'cnn', 'mccarthy', 'calling', 'explains', 'reacts', 'daughter', 'graham', 'officer', 'responds', 'wife', 'jail', 'gutfeld', 'nypd', 'fbi', 'mom', 'due', 'schumer', 'game',    'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became', 'money', 'politics', 'hot', 'defense', 'control', 'without', 'facing', 'billion', '.', ':', '’', '?', ",", 'summer', "‘", 'schools', 'finally', 'street', 'g.o.p', 'stone',   'us', 'new', 'says', 'biden', 'china', 'police', 'world', 'u.s.', 'president', 'amid', 'death', 'york', 'america', 'sanders', 'could', 'crisis', 'uk', 'home', 'house', 'man', 'state', 'black', 'news', 'people', '$', 'back', 'city', 'one', 'joe',  'may', 'first', 'bernie', 'democrats', 'white', 'americans', 'floyd', '2020', 'media', 'take', 'life', 'updates', 'time', 'protests', 'report', 'get', 'calls', 'fight', 'help', 'day', 'dies', 'american', '-', 'dr.', 'say', 'global', 'states', 'response', 'case', 'george', 'week', ';', 'bill', 'like', 'face', 'deaths', 'workers', 'campaign', 'dems', 'see', 'top', 'bloomberg', 'court', 'race', 'claims', 'economy', 'dead', 'super', 'big', 'judge', 'bbc', 'test', 'protesters', 'show', 'make', 'india', 'iowa', 'want', 'still', 'live', 'found', 'go', 'obama', 'would', 'south', 'flynn', 'election', 'work', 'need', 'democratic', 'vote', 'rep.', 'california', 'gov', 'best', 'sen.', 'rally', 'trial', 'killed', 'plan', 'toll', 'mayor', 'woman', 'women', 'law',  'deal', 'years', 'travel', 'end', 'care', 'italy', 'impeachment', 'warns', 'last', 'behind', 'debate', 'country', 'protest', 'quiz', 'know', 'attack', 'russia', 'video', 'family', 'star', 'war', 'senate', 'service', 'two', 'officials', 'going', 'pictures', 'next', 'follow', 'fears', 'former', 'inside', 'voters', 'pelosi', 'national', 'children', 'chief', 'ahead', 'business', "'we", 'murder', 'stop', 'justice', 'set', 'warren', 'tells', 'primary', 'win', 'party', 'shooting', '2', '3', 'tv', 'europe', 'briefing', 'much', 'economic', 'history', 'days', 'korea', 'weekend', 'iran', 'dem', 'many', 'mass', 'free', 'lives', 'order', 'bowl', 'hits', 'call', 'supreme', 'million', 'social', 'michael', 'aid', 'five', 'tucker', 'rise', 'times', 'hong', 'kong', 'florida', 'chinese', 'hannity', 'faces', 'cuomo', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'record', 'doctor', 'charged', 'force', 'governor', 'story', 'takes', 'change', 'exclusive', 'buttigieg', 'stimulus', 'public', 'gives', 'facebook', 'gop', 'bolton', 'listen', 'military', 'official', 'away', 'twitter', 'hit', 'open', 'year', 'never', 'way', 'good', 'despite', 'leader', 'mother', 'tuesday', 'john', 'arrested', 'online', 'radio', 'texas', 'got', 'reveals', 'save', 'start', 'stay', 'return', 'slams', 'africa', 'job', 'wants', 'oil', 'ny', '11', 'barr', 'relief', 'markets', 'must', 'making', 'makes', 'gets', 'long', 'rules', 'even', 'food', 'headlines', 'fall', 'fire', 'bryant', 'look', 'latest', 'ban', 'risk', 'russian', 'doctors', 'presidential', 'surge', 'system', 'use', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'another', 'cities', 'think', 'safe', 'blasts', 'federal', 'restrictions', 'cut', 'seattle', 'made', 'team', 'reports', 'key', 'missing', 'lost', 'kobe', '4', 'move', 'probe', 'guide', 'countries', "'the", 'amazon', 'shot', 'racism', 'political', 'minneapolis', 'wins', 'students', 'threat', 'left', 'mark', 'kids', 'changed', 'close', 'pm', 'medical', 'study', 'around', 'spain', 'ever', 'ship', 'wrong', 'analysis', 'young', 'find', 'washington', 'france', 'government', 'weinstein', 'across', 'die', 'goes', 'everything', 'deadly', 'aoc', 'real', 'west', 'experts', 'matter', 'johnson', 'reform', 'said', 'nevada', 'attacks', 'kill',  'bad', 'nyc', 'nation', 'died', 'son', 'come', 'market', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'night', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'months', 'second', 'mr.', 'chris', 'administration', 'father', 'needs', 'cops', 'major', 'wall', 'problem', 'really', 'might', 'hampshire', 'newt', 'jobs', 'de', 'germany', 'turn', 'message', 'memorial', 'stocks', 'cathedral', 'reads', 'businesses', 'give', '!', 'small', 'plans', 'event', 'near', 'secret', 'tom', 'trying', 'staff', 'coming', 'let', 'carolina', 'blasio', 'sign', 'unrest', 'secretary', 'elizabeth', 'union', 'seen', 'action', 'candidate', 'sick', 'church', 'prison', 'doj', 'patrick', '“', '”', 'canada', 'past', 'girl', 'leaves', 'tweet', 'caucuses', 'questions', 'meghan', 'crash', 'six', 'taking', 'things', 'stars', 'couple', 'congress', 'school', 'orders', '1', 'power', 'hope', 'violence', 'access', 'mike', 'pompeo', 'clash', 'far', 'better', 'andrew', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'tech', 'fighting']


    top_words = []



    for i in list_of_top_words:
        if i[0] not in exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_words.append(interlist)





    overall_words = []
    for i in top_words:
        overall_words.append(i)



    for i in overall_words:
        paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
        i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





    best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
    worst_words = sorted(overall_words, key = lambda x: x[2],)

    best_and_worst = []
    best_and_worst.append(best_words)
    best_and_worst.append(worst_words[:20])
    best_and_worst.append(exceptions)

    return best_and_worst

nyt_corona = find_corona(1)
bbc_corona = find_corona(2)
fn_corona = find_corona(3)

nyt_corona_words = nyt_corona[0]
bbc_corona_words = bbc_corona[0]
fn_corona_words = fn_corona[0]
corona_exceptions = nyt_corona[2]

for i in nyt_corona_words:
  save_to_db = superlative_table(graphid=7, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in bbc_corona_words:
  save_to_db = superlative_table(graphid=7, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in fn_corona_words:
  save_to_db = superlative_table(graphid=7, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()




def find_rp(paper_num):
    all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

    all_headline_string = ""

    for i in all_headlines:
        all_headline_string += " " + i['headline']


    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(300)

    list_of_top_words = []

    for i in most_common:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)


    exceptions = ['tax', 'list', 'taylor', 'meet', 'capitol', 'border', 'nursing','chicago', 'decision', "'it", 'final', 'lead', 'amy', 'barrett', 'coney', 'hunter', 'talks', 'getting', 'senator', 'biggest', 'office', 'convention', 'told','town', '10', 'mcconnell', 'moment', 'trade', 'tiktok', 'votes', 'christmas', 'early', 'become', "'re", 'keep', 'voting', 'thanksgiving', 'fraud', 'pennsylvania', 'climate', 'pick', 'general', 'polls', 'democrat', 'run', 'warning',  'georgia', 'distancing', 'worse',   'announces', 'issues', 'nfl', 'comments', 'owner',  'siegel', 'dc', "–", 'mcenany', 'speech', '&', 'impact', 'vp', 'claim', 'gingrich', 'accused', 'cnn', 'mccarthy', 'calling', 'explains', 'reacts', 'daughter', 'graham', 'responds', 'wife', 'gutfeld', 'mom', 'due', 'schumer', 'game', 'pence', 'concerns', 'clinton', 'cdc',  'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app', 'storm', 'returns', '...', 'begins', 'jailed', "'my", 'queen', "'ve", 'largest', 'england', 'photo', 'sea', 'passes', 'row', 'indian', 'ways', 'saved', 'german', 'boss', 'minister', 'australia', 'four', 'ca', 'baby', 'boy', 'symptoms', "'" , "'s", 'afghan', 'eu', "n't", 'visual', 'isolation', 'italian', 'tracking', 'denies', 'music', 'israel', 'french', 'australian', 'abuse', 'theme', 'suspect', 'turkey', 'brazil', 'aged', 'london', 'japan', 'harry', 'since', 'mental', 'delhi',  'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became', 'money', 'politics', 'hot', 'defense', 'control', 'without', 'facing', 'billion', '.', ':', "’", '?', ",", 'summer' , "‘", 'schools', 'w.h.o', 'c.d.c', 'finally', 'street', 'g.o.p', 'outbreaks', 'stone',    'coronavirus', 'us', 'new', 'virus', 'says', 'biden', 'china', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.', 'president', 'amid', 'death', 'york', 'america', 'sanders', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'man', 'state', 'news', 'outbreak', 'people', '$', 'back', 'city', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'democrats', 'americans', '2020', 'media', 'take', 'life', 'updates', 'time', 'report', 'get', 'calls', 'fight', 'help', 'day', 'dies', 'american', '-', 'dr.', 'say', 'global', 'states', 'response', 'case', 'george', 'week', ';', 'bill', 'like', 'face', 'deaths', 'workers', 'campaign', 'dems', 'see', 'top', 'bloomberg', 'court', 'race', 'claims', 'economy', 'dead', 'super', 'big', 'judge', 'bbc', 'test', 'show', 'make', 'india', 'iowa', 'want', 'reopen', 'still', 'live', 'masks', 'found', 'go', 'obama', 'would', 'south', 'flynn', 'election', 'quarantine', 'work', 'need', 'democratic', 'vote', 'rep.', 'california', 'gov', 'best', 'sen.', 'reopening', 'trial', 'killed', 'plan', 'toll', 'mayor', 'woman', 'women', 'law', 'vaccine', 'deal', 'years', 'travel', 'end', 'care', 'italy', 'spread', 'impeachment', 'warns', 'last', 'behind', 'debate', 'country', 'protest', 'quiz', 'know', 'attack', 'russia', 'video', 'family', 'star', 'war', 'senate', 'service', 'two', 'officials', 'going', 'pictures', 'next', 'covid', 'follow', 'fears', 'former', 'inside', 'voters', 'pelosi', 'national', 'children', 'chief', 'ahead', 'business', "'we", 'murder', 'stop', 'testing', 'set', 'warren', 'tells', 'hospital', 'primary', 'win', 'party', 'shooting', '2', '3', 'tv', 'europe', 'briefing', 'much', 'economic', 'history', 'days', 'korea', 'weekend', 'iran', 'dem', 'many', 'mass', 'free', 'lives', 'order', 'bowl', 'hits', 'call', 'supreme', 'million', 'social', 'michael', 'aid', 'five', 'tucker', 'rise', 'times', 'hong', 'kong', 'florida', 'chinese', 'hannity', 'faces', 'cuomo', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'record', 'doctor', 'charged', 'force', 'governor', 'story', 'takes', 'change', 'exclusive', 'buttigieg', 'stimulus', 'public', 'gives', 'facebook', 'gop', 'bolton', 'listen', 'military', 'official', 'away', 'twitter', 'hit', 'open', 'year', 'never', 'way', 'good', 'despite', 'leader', 'mother', 'tuesday', 'john', 'arrested', 'spreads', 'online', 'radio', 'texas', 'got', 'reveals', 'save', 'start', 'stay', 'return', 'slams', 'africa', 'job', 'wants', 'oil', 'ny', '11', 'barr', 'relief', 'markets', 'must', 'making', 'makes', 'gets', 'long', 'rules', 'even', 'food', 'headlines', 'fall', 'fire', 'bryant', 'look', 'latest', 'ban', 'mask', 'risk', 'russian', 'doctors', 'presidential', 'surge', 'system', 'use', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'another', 'cities', 'think', 'safe', 'blasts', 'federal', 'restrictions', 'cut', 'seattle', 'made', 'team', 'reports', 'key', 'missing', 'lost', 'kobe', '4', 'move', 'probe', 'guide', 'countries', "'the", 'amazon', 'shot', 'political', 'minneapolis', 'wuhan', 'wins', 'students', 'threat', 'left', 'mark', 'kids', 'changed', 'close', 'pm', 'medical', 'study', 'around', 'spain', 'ever', 'ship', 'wrong', 'analysis', 'young', 'find', 'washington', 'france', 'government', 'weinstein', 'across', 'die', 'patients', 'goes', 'everything', 'deadly', 'aoc', 'real', 'west', 'experts', 'matter', 'johnson', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'nation', 'died', 'son', 'come', 'market', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'night', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'months', 'second', 'mr.', 'chris', 'administration', 'father', 'needs',  'major', 'wall', 'problem', 'really', 'might', 'hampshire', 'newt', 'jobs', 'de', 'germany', 'turn', 'message', 'memorial', 'stocks', 'cathedral', 'reads', 'businesses', 'give', '!', 'small', 'plans', 'event', 'near', 'secret', 'tom', 'trying', 'staff', 'coming', 'let', 'carolina', 'blasio', 'sign', 'unrest', 'secretary', 'elizabeth', 'union', 'seen', 'action', 'candidate', 'sick', 'church', 'prison', 'doj', 'patrick', '“', '”', 'canada', 'past', 'girl', 'leaves', 'tweet', 'caucuses', 'questions', 'meghan', 'crash', 'six', 'taking', 'things', 'stars', 'couple', 'congress', 'school', 'orders', '1', 'power', 'hospitals', 'hope', 'violence', 'access', 'fauci', 'mike', 'pompeo', 'clash', 'far', 'better', 'andrew', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'tech', 'fighting']


    top_words = []



    for i in list_of_top_words:
        if i[0] not in exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_words.append(interlist)





    overall_words = []
    for i in top_words:
        overall_words.append(i)



    for i in overall_words:
        paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
        i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





    best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
    worst_words = sorted(overall_words, key = lambda x: x[2],)

    best_and_worst = []
    best_and_worst.append(best_words)
    best_and_worst.append(worst_words[:20])
    best_and_worst.append(exceptions)

    return best_and_worst

nyt_rp = find_rp(1)
bbc_rp = find_rp(2)
fn_rp = find_rp(3)

nyt_rp_words = nyt_rp[0]
bbc_rp_words = bbc_rp[0]
fn_rp_words = fn_rp[0]
rp_exceptions = nyt_rp[2]

for i in nyt_rp_words:
  save_to_db = superlative_table(graphid=8, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in bbc_rp_words:
  save_to_db = superlative_table(graphid=8, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

for i in fn_rp_words:
  save_to_db = superlative_table(graphid=8, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
  save_to_db.save()

from django.db.models.functions import TruncDay

all_headlines = Headline.objects.filter(day_order__lte=25).values('headline')

all_headline_string = ""

for i in all_headlines:
    all_headline_string += " " + i['headline']


import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
stopword = stopwords.words('english')
text = all_headline_string
word_tokens = nltk.word_tokenize(text.lower())
removing_stopwords = [word for word in word_tokens if word not in stopword]
freq = FreqDist(removing_stopwords)
most_common = freq.most_common(500)

list_of_top_words = []

for i in most_common:
    interlist = []
    interlist.append(i[0])
    interlist.append(i[1])
    list_of_top_words.append(interlist)



top_exceptions = [',', '’', ':', "'", '.', "'s", '?', '‘'  ]

scrubbed_list = []

for i in list_of_top_words:
    if i[0] not in top_exceptions:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        scrubbed_list.append(interlist)



for i in scrubbed_list:
    nyt_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
    if not nyt_sent:
        nyt_sent = [{'newspaper': 1, 'Average': 0}]


    bbc_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
    if not bbc_sent:
        bbc_sent = [{'newspaper': 2, 'Average': 0}]

    fn_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
    if not fn_sent:
        fn_sent = [{'newspaper': 3, 'Average': 0}]

    i.append(nyt_sent[0]['Average'] * 100)
    i.append(bbc_sent[0]['Average']* 100)
    i.append(fn_sent[0]['Average']*100)




scrubbed_list_with_variances = []
for i in scrubbed_list:
    nyt_fn_variance = round(i[2] - i[4],2)
    nyt_bbc_variance = round(i[2]- i[3],2)
    fn_bbc_variance = round(i[4] - i[3],2)

    nyt_check = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=i[0])
    bbc_check = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=i[0])
    fn_check = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=i[0])

    if nyt_check and fn_check:
        i.append(nyt_fn_variance)
    else:
        i.append(0)

    if nyt_check and bbc_check:
        i.append(nyt_bbc_variance)
    else:
        i.append(0)

    if fn_check and bbc_check:
        i.append(fn_bbc_variance)
    else:
        i.append(0)



master_word_variance = []


for i in scrubbed_list:
    nyt_fn = []
    nyt_fn.append(i[0])
    nyt_fn.append(i[1])
    nyt_fn.append('NYT')
    nyt_fn.append('FN')
    nyt_fn.append(i[5])
    master_word_variance.append(nyt_fn)
    nyt_bbc = []
    nyt_bbc.append(i[0])
    nyt_bbc.append(i[1])
    nyt_bbc.append('NYT')
    nyt_bbc.append('BBC')
    nyt_bbc.append(i[6])
    master_word_variance.append(nyt_bbc)
    fn_bbc = []
    fn_bbc.append(i[0])
    fn_bbc.append(i[1])
    fn_bbc.append('FN')
    fn_bbc.append('BBC')
    fn_bbc.append(i[7])
    master_word_variance.append(fn_bbc)



most_variance = sorted(master_word_variance, key = lambda x: abs(x[4]), reverse=True)


most_variance_words = most_variance[:300]

print(most_variance_words)


for i in most_variance_words:
  save_to_db = variance_table_word(graphid=10, word = i[0], count = i[1], news1= i[2], news2 = i[3], sentiment = i[4])
  save_to_db.save()





#do not rerun queries. filter most_variance with exception lists to find people, places, political, etc.

most_variance_people = []

for i in most_variance_words:
    if i[0] not in people_exceptions:
        most_variance_people.append(i)

print(most_variance_people)

for i in most_variance_people:
  save_to_db = variance_table_word(graphid=11, word = i[0], count = i[1], news1= i[2], news2 = i[3], sentiment = i[4])
  save_to_db.save()


most_variance_places = []

for i in most_variance_words:
    if i[0] not in place_exceptions:
        most_variance_places.append(i)

for i in most_variance_places:
  save_to_db = variance_table_word(graphid=12, word = i[0], count = i[1], news1= i[2], news2 = i[3], sentiment = i[4])
  save_to_db.save()

most_variance_politics = []

for i in most_variance_words:
    if i[0] not in politics_exceptions:
        most_variance_politics.append(i)

for i in most_variance_politics:
  save_to_db = variance_table_word(graphid=13, word = i[0], count = i[1], news1= i[2], news2 = i[3], sentiment = i[4])
  save_to_db.save()

most_variance_economics = []

for i in most_variance_words:
    if i[0] not in economics_exceptions:
        most_variance_economics.append(i)

for i in most_variance_economics:
  save_to_db = variance_table_word(graphid=14, word = i[0], count = i[1], news1= i[2], news2 = i[3], sentiment = i[4])
  save_to_db.save()


most_variance_corona = []
for i in most_variance_words:
    if i[0] not in corona_exceptions:
        most_variance_corona.append(i)

for i in most_variance_corona:
  save_to_db = variance_table_word(graphid=15, word = i[0], count = i[1], news1= i[2], news2 = i[3], sentiment = i[4])
  save_to_db.save()

most_variance_rp = []
for i in most_variance_words:
    if i[0] not in rp_exceptions:
        most_variance_rp.append(i)

for i in most_variance_rp:
  save_to_db = variance_table_word(graphid=16, word = i[0], count = i[1], news1= i[2], news2 = i[3], sentiment = i[4])
  save_to_db.save()



daily_sent_var_query_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('Date')
daily_sent_var_query_bbc = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('Date')
daily_sent_var_query_fn = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('Date')


all_sents_by_day = []

for i in range(0,len(daily_sent_var_query_nyt)):
    interlist = []
    interlist.append(daily_sent_var_query_nyt[i]['Date'])
    interlist.append(round(daily_sent_var_query_nyt[i]['Average']*100,2))

    interlist.append(round(daily_sent_var_query_bbc[i]['Average']*100,2))
    interlist.append(round(daily_sent_var_query_fn[i]['Average']*100,2))
    all_sents_by_day.append(interlist)



daily_variances = []

for i in all_sents_by_day:
    interlist = []
    interlist.append(i[0])
    interlist.append('NYT')
    interlist.append('BBC')
    interlist.append(i[1] - i[2])
    interlist2 = []
    interlist2.append(i[0])
    interlist2.append('NYT')
    interlist2.append('FN')
    interlist2.append(i[1]-i[3])
    interlist3 = []
    interlist3.append(i[0])
    interlist3.append('FN')
    interlist3.append('BBC')
    interlist3.append(i[3]-i[2])
    daily_variances.append(interlist)
    daily_variances.append(interlist2)
    daily_variances.append(interlist3)



most_variance_dates = sorted(daily_variances, key = lambda x: abs(x[3]), reverse=True)


for i in most_variance_dates:
  save_to_db = variance_table(graphid=9, variance_date=i[0], news1=i[1], news2=i[2], sentiment=i[3])
  save_to_db.save()





def save_to_super_sentiment_newspaper_overall_top_worst_20():

  #original code
  all_headlines = Headline.objects.filter(day_order__lte=25).values('headline')



  all_headline_string = ""

  for i in all_headlines:
      all_headline_string += " " + i['headline']


  import nltk
  from nltk import FreqDist
  from nltk.corpus import stopwords
  stopword = stopwords.words('english')
  text = all_headline_string
  word_tokens = nltk.word_tokenize(text.lower())
  removing_stopwords = [word for word in word_tokens if word not in stopword]
  freq = FreqDist(removing_stopwords)
  most_common = freq.most_common(500)

  list_of_top_words = []

  for i in most_common:
      interlist = []
      interlist.append(i[0])
      interlist.append(i[1])
      list_of_top_words.append(interlist)



  exceptions = [',',':',"'",'.','?', "'s", '‘', "n't", '’']

  top_words = []

  for i in list_of_top_words:
      if i[0] not in exceptions:
          interlist = []
          interlist.append(i[0])
          interlist.append(i[1])
          top_words.append(interlist)



  total_exceptions = []

  for i in top_words:
      total_exceptions.append(i[0])



  overall_words = []
  for i in top_words:
      overall_words.append(i)

  #top people who show up in the top 500 most common words

  for i in overall_words:
      sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=i[0]).values('sentiment')
      total_for_average = 0

      for y in sent_average:
          total_for_average += y['sentiment']

      total_for_average = total_for_average * 100

      average_key = total_for_average/len(sent_average)

      average_key = round(average_key, 2)

      i.append(average_key)



  #final places lists
  worst_overall = sorted(overall_words, key = lambda x: x[2])
  top_overall = sorted(overall_words, key = lambda x: x[2], reverse=True)

  worst_overall = worst_overall[:20]
  top_overall = top_overall[:20]





  #filter by papernum

  def get_by_paper(paper_number):
    all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_number).values('headline')



    all_headline_string = ""

    for i in all_headlines:
        all_headline_string += " " + i['headline']


    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(500)

    list_of_top_words = []

    for i in most_common:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)



    exceptions = [',',':',"'",'.','?', "'s", '‘', "n't", '’']

    top_words = []

    for i in list_of_top_words:
        if i[0] not in exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_words.append(interlist)



    total_exceptions = []

    for i in top_words:
        total_exceptions.append(i[0])



    overall_words = []
    for i in top_words:
        overall_words.append(i)

    #top people who show up in the top 500 most common words

    for i in overall_words:
        sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=i[0]).values('sentiment')
        total_for_average = 0

        for y in sent_average:
            total_for_average += y['sentiment']

        total_for_average = total_for_average * 100

        average_key = total_for_average/len(sent_average)

        average_key = round(average_key, 2)

        i.append(average_key)



    #final places lists
    worst_overall = sorted(overall_words, key = lambda x: x[2])
    top_overall = sorted(overall_words, key = lambda x: x[2], reverse=True)

    worst_overall = worst_overall[:20]
    top_overall = top_overall[:20]

    return_output = []

    return_output.append(worst_overall)
    return_output.append(top_overall)

    return return_output


  worst_overall_nyt = get_by_paper(1)[0]
  worst_overall_bbc = get_by_paper(2)[0]
  worst_overall_fn = get_by_paper(3)[0]

  top_overall_nyt = get_by_paper(1)[1]
  top_overall_bbc = get_by_paper(2)[1]
  top_overall_fn = get_by_paper(3)[1]

  final_return = []

  for i in worst_overall:
    save_to_db = superlative_table(graphid=20, newspaper=4, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()

  for i in top_overall:
    save_to_db = superlative_table(graphid=21, newspaper=4, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()

  for i in worst_overall_nyt:
    save_to_db = superlative_table(graphid=20, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()

  for i in worst_overall_bbc:
    save_to_db = superlative_table(graphid=20, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()

  for i in worst_overall_fn:
    save_to_db = superlative_table(graphid=20, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()


  for i in top_overall_nyt:
    save_to_db = superlative_table(graphid=21, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()

  for i in top_overall_bbc:
    save_to_db = superlative_table(graphid=21, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()

  for i in top_overall_fn:
    save_to_db = superlative_table(graphid=21, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()




save_to_super_sentiment_newspaper_overall_top_worst_20()



#graph_ids

#name              = 30
#place             = 31
#political         = 32
#economic          = 33
#coronavirus       = 34
#policing/race     = 35


def get_superlatives_by_cat_in_database(graph_id_number,one, two, three, four, five, six):




  all_headlines = Headline.objects.filter(day_order__lte=25).values('headline')



  all_headline_string = ""

  for i in all_headlines:
      all_headline_string += " " + i['headline']


  import nltk
  from nltk import FreqDist
  from nltk.corpus import stopwords
  stopword = stopwords.words('english')
  text = all_headline_string
  word_tokens = nltk.word_tokenize(text.lower())
  removing_stopwords = [word for word in word_tokens if word not in stopword]
  freq = FreqDist(removing_stopwords)
  most_common = freq.most_common(500)

  list_of_top_words = []

  for i in most_common:
      interlist = []
      interlist.append(i[0])
      interlist.append(i[1])
      list_of_top_words.append(interlist)



  exceptions = [',',':',"'",'.','?', "'s", '‘', "n't", '’']

  top_words = []

  for i in list_of_top_words:
      if i[0] not in exceptions:
          interlist = []
          interlist.append(i[0])
          interlist.append(i[1])
          top_words.append(interlist)



  if graph_id_number == 30:
    people_exceptions = one
  elif graph_id_number == 31:
    people_exceptions = two
  elif graph_id_number == 32:
    people_exceptions = three
  elif graph_id_number == 33:
    people_exceptions = four
  elif graph_id_number == 34:
    people_exceptions = five
  elif graph_id_number == 35:
    people_exceptions = six

  top_people = []
  for i in top_words:
      if i[0] not in people_exceptions:
          interlist = []
          interlist.append(i[0])
          interlist.append(i[1])
          top_people.append(interlist)

  #top people who show up in the top 500 most common words

  for i in top_people:
      sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=i[0]).values('sentiment')
      total_for_average = 0

      for y in sent_average:
          total_for_average += y['sentiment']

      total_for_average = total_for_average * 100

      average_key = total_for_average/len(sent_average)

      average_key = round(average_key, 2)

      i.append(average_key)



  #final people list

  best_people = sorted(top_people, key = lambda x: x[2], reverse=True)


  def get_best_people_by_newspaper(paper_id, exceptions_variable):

    all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_id).values('headline')



    all_headline_string = ""

    for i in all_headlines:
        all_headline_string += " " + i['headline']


    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(500)

    list_of_top_words = []

    for i in most_common:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)



    exceptions = [',',':',"'",'.','?', "'s", '‘', "n't", '’']

    top_words = []

    for i in list_of_top_words:
        if i[0] not in exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_words.append(interlist)




    top_people = []
    for i in top_words:
        if i[0] not in exceptions_variable:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_people.append(interlist)

    #top people who show up in the top 500 most common words

    for i in top_people:
        sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=i[0]).values('sentiment')
        total_for_average = 0

        for y in sent_average:
            total_for_average += y['sentiment']

        total_for_average = total_for_average * 100

        average_key = total_for_average/len(sent_average)

        average_key = round(average_key, 2)

        i.append(average_key)



    #final people list

    best_people = sorted(top_people, key = lambda x: x[2], reverse=True)

    return best_people

  get_best_nyt = get_best_people_by_newspaper(1, people_exceptions)
  get_best_bbc = get_best_people_by_newspaper(2, people_exceptions)
  get_best_fn = get_best_people_by_newspaper(3, people_exceptions)

  for i in get_best_nyt:
    save_to_db = superlative_table(graphid=graph_id_number, newspaper=1, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()

  for i in get_best_bbc:
    save_to_db = superlative_table(graphid=graph_id_number, newspaper=2, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()

  for i in get_best_fn:
    save_to_db = superlative_table(graphid=graph_id_number, newspaper=3, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()

  for i in best_people:
    save_to_db = superlative_table(graphid=graph_id_number, newspaper=4, word=i[0], count=i[1], sentiment=i[2])
    save_to_db.save()


get_superlatives_by_cat_in_database(30, people_exceptions, place_exceptions, politics_exceptions, economics_exceptions, corona_exceptions, rp_exceptions)
get_superlatives_by_cat_in_database(31, people_exceptions, place_exceptions, politics_exceptions, economics_exceptions, corona_exceptions, rp_exceptions)
get_superlatives_by_cat_in_database(32, people_exceptions, place_exceptions, politics_exceptions, economics_exceptions, corona_exceptions, rp_exceptions)
get_superlatives_by_cat_in_database(33, people_exceptions, place_exceptions, politics_exceptions, economics_exceptions, corona_exceptions, rp_exceptions)
get_superlatives_by_cat_in_database(34, people_exceptions, place_exceptions, politics_exceptions, economics_exceptions, corona_exceptions, rp_exceptions)
get_superlatives_by_cat_in_database(35, people_exceptions, place_exceptions, politics_exceptions, economics_exceptions, corona_exceptions, rp_exceptions)


import nltk
from nltk import FreqDist
from nltk.corpus import stopwords

all_headlines = Headline.objects.filter(day_order__lte=25).values('headline')

all_headline_string = ""

for i in all_headlines:
    all_headline_string += " " + str(i['headline'])



stopword = ['the', 'to', ',', 'in', '’',"'", ':', 'of', 'a', '.','for', 'on', "'s",'s', 'is','and','‘','how', 'with', 'as', 'from', 'at', 'are', 'what', 'after', 'over', 'it', 'be', 'this', 'will', 'who', 'why', 'about', 'by', 'that', 't', 'has', 'have', 'can', 'out', 'up', 'was', 'here', 'more', 'do', 'could', 'an',  "n't", 'amid', 'your', 'my', 'into', 'if', 'did', 'does', '-', 'than',]
text = all_headline_string
word_tokens = nltk.word_tokenize(text.lower())
print(word_tokens)
removing_stopwords = [word for word in word_tokens if word not in stopword]
freq = FreqDist(removing_stopwords)
most_common = freq.most_common(500)
print(most_common)
most_common_list = []
for x, y in most_common:
    interlist = []
    interlist.append(x)
    interlist.append(y)
    most_common_list.append(interlist)
print(most_common_list)


top_100 = most_common_list[:100]
print(top_100)



def get_coocs(paper_num, search_term):
    headlines_with_base = Headlinewc.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=search_term[0]).values('headline')
    headlines_with_base_string = ""
    for i in headlines_with_base:
        headlines_with_base_string += " " + i['headline']
    stopword = ['the', 'to', ',', 'in', '’',"'", ':', 'of', 'a', '.','for', 'on', "'s",'s', 'is','and','‘','how', 'with', 'as', 'from', 'at', 'are', 'what', 'after', 'over', 'it', 'be', 'this', 'will', 'who', 'why', 'about', 'by', 'that', 't', 'has', 'have', 'can', 'out', 'up', 'was', 'here', 'more', 'do', 'could', 'an',  "n't", 'amid', 'your', 'my', 'into', 'if', 'did', 'does', '-', 'than',]
    text = headlines_with_base_string
    word_tokens = nltk.word_tokenize(text.lower())

    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(25)
    print(most_common)
    cooc_list = []
    for i in most_common:
        interlist = []
        interlist.append(search_term[0])
        interlist.append(i[0])
        interlist.append(paper_num)
        interlist.append(i[1])
        cooc_list.append(interlist)

    return cooc_list


coocs = []
for i in top_100:
  coocs.append(get_coocs(1,i))
  coocs.append(get_coocs(2,i))
  coocs.append(get_coocs(3,i))

print(coocs)

for i in coocs:
  for y in i:
      cooc_save_to_db = cooc(base_word=y[0], co_word=y[1], newspaper=y[2], co_word_count=y[3])
      cooc_save_to_db.save()



from django.core.exceptions import ObjectDoesNotExist
from custom_scraper.models import Headline
from custom_scraper.models import word_sentiment
from custom_scraper.models import word_count_general
from custom_scraper.models import style_wc
from custom_scraper.models import Headlinewc
from custom_scraper.models import Headlinewrl
from django.db.models import Avg
from custom_scraper.models import cooc_wc




#custom function to weed out stopwords, plurals and apostrophe s and get count of each word in a string
def get_sorted_word_count_by_string(all_headline_string):
    all_headline_test = all_headline_string
    # regex to isolate all "'s" = r" [^ ]*[^ ]['’]s"

    import re

    all_headlines_list = all_headline_test.split()




    #below removes all apostrophe s's from list made of all headlines string split
    for counter, i in enumerate(all_headlines_list):
        if re.findall(r"[^ ]*[^ ]['’]s", i):

            all_headlines_list[counter] = i[:len(i)-2]


    a = 0


    #remove all nonalphanumeric characters
    for counter,i in enumerate(all_headlines_list):
        if re.findall(r"\W",i):
            if not re.findall(r"-",i):

                new_i = re.sub(r"\W", '', i)
                all_headlines_list[counter] = new_i





    #ies number 1: takes 4 letter words ending with ies and removes s, to take care of cases similar to "dies", "vies", "ties"
    for counter, i in enumerate(all_headlines_list):
        if re.findall(r".*ies$",i):
            if len(i) == 4:

                new_i = i[:len(i)-1]
                all_headlines_list[counter] = new_i


    #ies number 2: end in "ies" but singular ends in "ie"
    for counter, i in enumerate(all_headlines_list):
        if re.findall(r".*ies$",i):
            if i in ["Zombies", "zombies", "Trekkies", "trekkies"]:

                new_i = i[:len(i)-1]
                all_headlines_list[counter] = new_i








    #erase stopwords
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    exceptions_ies = ['series', "Series", "monies", "Monies"]

    for counter, i in enumerate(all_headlines_list):
        if i.lower() in stopwords:
            all_headlines_list[counter] = ''




    #change "ies" plurals to end with "y"
    for counter, i in enumerate(all_headlines_list):
        if i.endswith("ies"):
            if i not in exceptions_ies:
                if len(i) > 4:

                    all_headlines_list[counter] = i[:len(i)-3] + "y"
            else:
                all_headlines_list[counter] = i + "donotdelete"



    #remove s from words ending with "ves"
    for counter, i in enumerate(all_headlines_list):
        if i.endswith("ves"):

            all_headlines_list[counter] = i[:len(i)-1]


    for counter, i in enumerate(all_headlines_list):
        if i.endswith("os"):

            if i.lower() in ['studios', 'photos']:
                all_headlines_list[counter] = i[:len(i)-1]



    #do not touch any words that end in "ess" make this an exception to s taking also "uss"




    for counter, i in enumerate(all_headlines_list):
        if i.endswith("as"):
            if i.lower() not in ['koalas', 'gorillas', 'areas', 'sherpas']:

                all_headlines_list[counter] = i + "donotdelete"



    #add a code to each word that we dont want to shave s off of.




    for counter,i in enumerate(all_headlines_list):
        if i.lower() in ['des', 'moines', 'holmes', 'bynes', 'angeles','philippines', 'nunes', 'thames']:
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if re.findall(r".shes$|.xes$|.sses$|.ches$|.uses$|.usses$", i):
            if i.lower() not in ['accuses', 'excuses']:
                all_headlines_list[counter] = i[:len(i)-2]
            else:
                all_headlines_list[counter] = i[:len(i)-1] + "donotdelete"


    #exceptions, words ending with s that want to flag to not eliminate
    for counter, i in enumerate(all_headlines_list):
        if i.lower() in ['sanders', 'news', 'collins', 'williams']:
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if i.endswith("is"):
            if i.lower() not in ['nazis']:
                all_headlines_list[counter] = i + "donotdelete"
            else:
                all_headlines_list[counter] = i[:len(i)-1]

    for counter, i in enumerate(all_headlines_list):
        if i.endswith("iss"):
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if i.endswith("ass"):
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if i.endswith("os"):
            all_headlines_list[counter] = i + "donotdelete"

    for counter, i in enumerate(all_headlines_list):
        if i.lower() in ['goes']:
            all_headlines_list[counter] = 'go'

    for counter, i in enumerate(all_headlines_list):
        if re.findall(r".us$|.ess$|.uss$|.ass$", i):
            all_headlines_list[counter] = i + "donotdelete"


    for counter, i in enumerate(all_headlines_list):
        if i.endswith("s"):
            all_headlines_list[counter] = i[:len(i)-1]


    all_headlines_list_lowered = []

    for i in all_headlines_list:
        all_headlines_list_lowered.append(i.lower())

    for counter, i in enumerate(all_headlines_list_lowered):
        if i.endswith("donotdelete"):
            all_headlines_list_lowered[counter] = i[:len(i)-11]

    word_count_dict = {}

    for i in all_headlines_list_lowered:
        if i not in word_count_dict:
            word_count_dict[i] = 1
        else:
            word_count_dict[i] += 1

    word_count_sorted = sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)

    return word_count_sorted


headlines_all = Headline.objects.filter(day_order__lte=25).values('headline')
headlines_all_string = ""
for i in headlines_all:
    headlines_all_string += " " + i['headline']

headlines_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).values('headline')
headlines_nyt_string = ""
for i in headlines_nyt:
    headlines_nyt_string += " " + i['headline']

headlines_bbc = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).values('headline')
headlines_bbc_string = ""
for i in headlines_bbc:
    headlines_bbc_string += " " + i['headline']

headlines_fn = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).values('headline')
headlines_fn_string = ""
for i in headlines_fn:
    headlines_fn_string += " " + i['headline']

overall_word_count_chart = get_sorted_word_count_by_string(headlines_all_string)
nyt_word_count_chart = get_sorted_word_count_by_string(headlines_nyt_string)
bbc_word_count_chart = get_sorted_word_count_by_string(headlines_bbc_string)
fn_word_count_chart = get_sorted_word_count_by_string(headlines_fn_string)

terms = []
ny_values_list = []
bbc_values_list = []
fn_values_list = []
for i in overall_word_count_chart[1:10]:
    terms.append(i[0])
    for y in nyt_word_count_chart:
        if i[0] == y[0]:
            ny_values_list.append(y[1])
    for z in bbc_word_count_chart:
        if i[0] == z[0]:
            bbc_values_list.append(z[1])
    for x in fn_word_count_chart:
        if i[0] == x[0]:
            fn_values_list.append(x[1])


nyt_most = []
bbc_most = []
fn_most = []
overall_most = []
for i in overall_word_count_chart[1:250]:
    interlist = []
    interlist.append(i[0])
    interlist.append(i[1])
    overall_most.append(interlist)

for i in nyt_word_count_chart[1:251]:
    interlist = []
    interlist.append(i[0])
    interlist.append(i[1])
    nyt_most.append(interlist)

for i in bbc_word_count_chart[1:251]:
    interlist = []
    interlist.append(i[0])
    interlist.append(i[1])
    bbc_most.append(interlist)

for i in fn_word_count_chart[1:251]:
    interlist = []
    interlist.append(i[0])
    interlist.append(i[1])
    fn_most.append(interlist)

print(nyt_most)

for i in nyt_most:
    save_to_db_wc = word_count_general(newspaper=1, word=i[0], word_count=i[1])
    save_to_db_wc.save()

for i in bbc_most:
    save_to_db_wc = word_count_general(newspaper=2, word=i[0], word_count=i[1])
    save_to_db_wc.save()

for i in fn_most:
    save_to_db_wc = word_count_general(newspaper=3, word=i[0], word_count=i[1])
    save_to_db_wc.save()

for i in overall_most:
    save_to_db_wc = word_count_general(newspaper=4, word=i[0], word_count=i[1])
    save_to_db_wc.save()


avg_wc_overall = Headlinewc.objects.all().filter(day_order__lte=25).aggregate(Avg('headline_wc'))
avg_wc_overall = round(avg_wc_overall['headline_wc__avg'],1)

avg_wc_nyt = Headlinewc.objects.all().filter(day_order__lte=25).filter(newspaper=1).aggregate(Avg('headline_wc'))
avg_wc_nyt = round(avg_wc_nyt['headline_wc__avg'],1)

avg_wc_bbc = Headlinewc.objects.all().filter(day_order__lte=25).filter(newspaper=2).aggregate(Avg('headline_wc'))
avg_wc_bbc = round(avg_wc_bbc['headline_wc__avg'],1)

avg_wc_fn = Headlinewc.objects.all().filter(day_order__lte=25).filter(newspaper=3).aggregate(Avg('headline_wc'))
avg_wc_fn = round(avg_wc_fn['headline_wc__avg'],1)


avg_rl_overall = Headlinewrl.objects.all().filter(day_order__lte=25).aggregate(Avg('reading_level'))
avg_rl_overall = round(avg_rl_overall['reading_level__avg'],1)

avg_rl_nyt = Headlinewrl.objects.all().filter(day_order__lte=25).filter(newspaper=1).aggregate(Avg('reading_level'))
avg_rl_nyt = round(avg_rl_nyt['reading_level__avg'],1)

avg_rl_bbc = Headlinewrl.objects.all().filter(day_order__lte=25).filter(newspaper=2).aggregate(Avg('reading_level'))
avg_rl_bbc = round(avg_rl_bbc['reading_level__avg'],1)

avg_rl_fn = Headlinewrl.objects.all().filter(day_order__lte=25).filter(newspaper=3).aggregate(Avg('reading_level'))
avg_rl_fn = round(avg_rl_fn['reading_level__avg'],1)



question_count = Headlinewrl.objects.filter(headline__icontains='?').count()
overall_hl_count = Headlinewrl.objects.count()
question_percent_overall = round(question_count/overall_hl_count,3) * 100
exclamation_count = Headlinewrl.objects.filter(headline__icontains='!').count()
exclamation_percent_overall = round(exclamation_count/overall_hl_count, 3) * 100

def get_qe_percent(paper_num):
    question_count = Headlinewrl.objects.filter(newspaper=paper_num).filter(headline__icontains='?').count()
    exclamation_count = Headlinewrl.objects.filter(newspaper=paper_num).filter(headline__icontains='!').count()
    overall_hl_count = Headlinewrl.objects.filter(newspaper=paper_num).count()

    question_percent = round(question_count/overall_hl_count, 3) * 100
    exclamation_percent = round(exclamation_count/overall_hl_count,3) * 100

    return question_percent, exclamation_percent

punc_nyt = get_qe_percent(1)
punc_bbc = get_qe_percent(2)
punc_fn = get_qe_percent(3)


question_percent_nyt = punc_nyt[0]
exclamation_percent_nyt = punc_nyt[1]

question_percent_bbc = punc_bbc[0]
exclamation_percent_bbc = punc_bbc[1]

question_percent_fn = punc_fn[0]
exclamation_percent_fn = punc_fn[1]

def avg_word_length(all_headlines_string):
    sum_letters = 0
    all_headlines_list = all_headlines_string.split(' ')
    for i in all_headlines_list:
        sum_letters += len(i)
    all_headlines_list_length = len(all_headlines_list)

    average_length = round(sum_letters/all_headlines_list_length,1)

    return average_length

all_avg_word_length = avg_word_length(headlines_all_string)
nyt_avg_word_length = avg_word_length(headlines_nyt_string)

bbc_avg_word_length = avg_word_length(headlines_bbc_string)

fn_avg_word_length = avg_word_length(headlines_fn_string)


all_unique_words = len(overall_word_count_chart)
nyt_unique_words = len(nyt_word_count_chart)
bbc_unique_words = len(bbc_word_count_chart)
fn_unique_words = len(fn_word_count_chart)


def find_top_50_percent(word_count_chart):
    nyt_word_count = 0
    for i in word_count_chart[1:]:
        nyt_word_count += i[1]
    top_50_count = 0
    for i in word_count_chart[1:51]:
        top_50_count += i[1]

    percent_of_words_that_are_top_50_words = round((top_50_count*100)/nyt_word_count,3)

    return percent_of_words_that_are_top_50_words

overall_top_50 = find_top_50_percent(overall_word_count_chart)
nyt_top_50 = find_top_50_percent(nyt_word_count_chart)
bbc_top_50 = find_top_50_percent(bbc_word_count_chart)
fn_top_50 = find_top_50_percent(fn_word_count_chart)

print(avg_wc_nyt)
print(avg_rl_nyt)
print(question_percent_nyt)
print(exclamation_percent_nyt)
print(nyt_avg_word_length)
print(nyt_unique_words)
print(nyt_top_50)



nyt_style_save_to_db = style_wc(newspaper=1,awc=avg_wc_nyt, ahrl=avg_rl_nyt, percent_quest=question_percent_nyt, percent_exclam=exclamation_percent_nyt, ahwl=nyt_avg_word_length, uw=nyt_unique_words, wd=nyt_top_50)
nyt_style_save_to_db.save()

bbc_style_save_to_db = style_wc(newspaper=2,awc=avg_wc_bbc, ahrl=avg_rl_bbc, percent_quest=question_percent_bbc, percent_exclam=exclamation_percent_bbc, ahwl=bbc_avg_word_length, uw=bbc_unique_words, wd=bbc_top_50)
bbc_style_save_to_db.save()

fn_style_save_to_db = style_wc(newspaper=3,awc=avg_wc_fn, ahrl=avg_rl_fn, percent_quest=question_percent_fn, percent_exclam=exclamation_percent_fn, ahwl=fn_avg_word_length, uw=fn_unique_words, wd=fn_top_50)
fn_style_save_to_db.save()

overall_style_save_to_db = style_wc(newspaper=4,awc=avg_wc_overall, ahrl=avg_rl_overall, percent_quest=question_percent_overall, percent_exclam=exclamation_percent_overall, ahwl=all_avg_word_length, uw=all_unique_words, wd=overall_top_50)
overall_style_save_to_db.save()

base_words = []
for i in overall_word_count_chart[1:101]:
    base_words.append(i[0])

base_words_nyt = []
for i in nyt_word_count_chart[1:101]:
    base_words_nyt.append(i[0])

base_words_bbc = []
for i in bbc_word_count_chart[1:101]:
    base_words_bbc.append(i[0])

base_words_fn = []
for i in fn_word_count_chart[1:101]:
    base_words_fn.append(i[0])

coocs_list = []
for i in base_words[:100]:
    print(i)
    all_headlines_with_i = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=i).values('headline')
    all_headlines_with_i_string = ""
    for y in all_headlines_with_i:
        all_headlines_with_i_string += " " + y['headline']

    i_coocs_word_count = get_sorted_word_count_by_string(all_headlines_with_i_string)
    print(i_coocs_word_count)
    list_for_this_words_coocs = []
    for z in i_coocs_word_count[:100]:
        interlist = []
        interlist.append(z[0])
        interlist.append(z[1])
        list_for_this_words_coocs.append(interlist)
    coocs_list.append(list_for_this_words_coocs[2:100])


def coocs_by_paper(paper_num, paper_base_list):
        coocs_list = []
        for i in paper_base_list:
            print(i)
            all_headlines_with_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i).values('headline')
            all_headlines_with_i_string = ""
            for y in all_headlines_with_i:
                all_headlines_with_i_string += " " + y['headline']

            i_coocs_word_count = get_sorted_word_count_by_string(all_headlines_with_i_string)
            print(i_coocs_word_count)
            list_for_this_words_coocs = []
            for z in i_coocs_word_count[:100]:
                interlist = []
                interlist.append(z[0])
                interlist.append(z[1])
                list_for_this_words_coocs.append(interlist)
            coocs_list.append(list_for_this_words_coocs[2:100])

        return coocs_list

numbered_base_words = enumerate(base_words,1)

numbered_base_word_nyt = enumerate(base_words_nyt,1)
numbered_base_word_bbc = enumerate(base_words_bbc,1)
numbered_base_word_fn = enumerate(base_words_fn,1)

coocs_list_nyt = coocs_by_paper(1, base_words_nyt)
coocs_list_bbc = coocs_by_paper(2, base_words_nyt)
coocs_list_fn = coocs_by_paper(3, base_words_nyt)

print(numbered_base_word_nyt)
print(coocs_list_nyt)
print(base_words_nyt)
print(len(base_words_nyt))

def make_cooc_dict(base_words, cooc_list):
    new_dict = {}
    for i in range(len(base_words)):
        new_dict[base_words[i]] = cooc_list[i]
    return new_dict

nyt_cooc_dict = make_cooc_dict(base_words_nyt, coocs_list_nyt)
bbc_cooc_dict = make_cooc_dict(base_words_bbc, coocs_list_bbc)
fn_cooc_dict = make_cooc_dict(base_words_fn, coocs_list_fn)
overall_cooc_dict = make_cooc_dict(base_words, coocs_list)

for term in nyt_cooc_dict:
    for cooc_list in nyt_cooc_dict[term]:
        cooc_save_to_db = cooc_wc(newspaper=1,base_word=term,cooc=cooc_list[0],coocc=cooc_list[1])
        cooc_save_to_db.save()

for term in bbc_cooc_dict:
    for cooc_list in bbc_cooc_dict[term]:
        cooc_save_to_db = cooc_wc(newspaper=2,base_word=term,cooc=cooc_list[0],coocc=cooc_list[1])
        cooc_save_to_db.save()

for term in fn_cooc_dict:
    for cooc_list in fn_cooc_dict[term]:
        cooc_save_to_db = cooc_wc(newspaper=3,base_word=term,cooc=cooc_list[0],coocc=cooc_list[1])
        cooc_save_to_db.save()

for term in overall_cooc_dict:
    for cooc_list in overall_cooc_dict[term]:
        cooc_save_to_db = cooc_wc(newspaper=4,base_word=term,cooc=cooc_list[0],coocc=cooc_list[1])
        cooc_save_to_db.save()



from django.db.models import Max





highest_headline_id = hl_tokens_emotions.objects.aggregate(Max('headline_id'))
print(highest_headline_id['headline_id__max'])
all_headlines = Headline.objects.filter(id__gt=highest_headline_id['headline_id__max']).values('id','newspaper', 'headline', 'date', 'link', 'day_order')


for query_result in all_headlines:
    headline_tokenized = get_sorted_word_count_by_string(query_result['headline'])

    for token, token_count in headline_tokenized:
        if token != '':
            token_emotion_dict = {}
            token_emotion_query = emotion.objects.filter(word=token).values('fear', 'anger', 'anticip', 'trust', 'surprise','sadness', 'disgust', 'joy', 'positive', 'negative')
            if len(token_emotion_query) > 0:
                token_emotion_dict['fear'] = token_emotion_query[0]['fear']
                token_emotion_dict['anger'] = token_emotion_query[0]['anger']
                token_emotion_dict['anticip'] = token_emotion_query[0]['anticip']
                token_emotion_dict['trust'] = token_emotion_query[0]['trust']
                token_emotion_dict['surprise'] = token_emotion_query[0]['surprise']
                token_emotion_dict['sadness'] = token_emotion_query[0]['sadness']
                token_emotion_dict['disgust'] = token_emotion_query[0]['disgust']
                token_emotion_dict['joy'] = token_emotion_query[0]['joy']
                token_emotion_dict['positive'] = token_emotion_query[0]['positive']
                token_emotion_dict['negative'] = token_emotion_query[0]['negative']
            else:
                token_emotion_dict = {'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'sadness':0, 'disgust':0, 'joy':0, 'positive': 0, 'negative':0}

            token_save_to_db = hl_tokens_emotions(headline_id=query_result['id'], newspaper=query_result['newspaper'], word=token, date=query_result['date'], link=query_result['link'], day_order=query_result['day_order'], fear=token_emotion_dict['fear'], anger=token_emotion_dict['anger'], anticip=token_emotion_dict['anticip'], trust=token_emotion_dict['trust'], surprise=token_emotion_dict['surprise'], sadness=token_emotion_dict['sadness'], disgust=token_emotion_dict['disgust'], joy=token_emotion_dict['joy'], positive=token_emotion_dict['positive'],negative=token_emotion_dict['negative'],)
            token_save_to_db.save()


def get_top_100_words_by_paper(paper_num):
    top_word_count_query = word_count_general.objects.filter(newspaper=paper_num).values("word")
    top_words = []
    for result in top_word_count_query:
        top_words.append(result['word'])
    return top_words

nyt_top_words = get_top_100_words_by_paper(1)[:50]
bbc_top_words = get_top_100_words_by_paper(2)[:50]
fn_top_words = get_top_100_words_by_paper(3)[:50]
overall_top_words = get_top_100_words_by_paper(4)[:50]

print(nyt_top_words)





today = date.today()
yesterday = date.today() - timedelta(days=1)

#overall (use function based on the below code for by paper)

tally_list = []
total_hls = []
for word in overall_top_words:
    all_headline_ids_query = hl_tokens_emotions.objects.filter(date__contains=today).filter(day_order__lte=25).filter(word=word).values("headline_id")
    all_headline_id_list = []
    all_headlines_emotion_tally_dict = {'word':word,'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'sadness':0, 'disgust':0, 'joy':0}
    for query_result in all_headline_ids_query:
        if query_result['headline_id'] not in all_headline_id_list:
            all_headline_id_list.append(query_result['headline_id'])
    total_hl_length = len(all_headline_id_list)
    total_hls.append(total_hl_length)

    for each_headline_id in all_headline_id_list:
        headline_word_data = hl_tokens_emotions.objects.filter(headline_id=each_headline_id).values('word', 'fear', 'anger', 'anticip', 'trust', 'surprise', 'sadness', 'disgust', 'joy' )
        headline_word_data_list = []
        for headline_word_data_result in headline_word_data:
            if headline_word_data_result['word'] != word:
                this_word_dict = {}
                this_word_dict['word'] = headline_word_data_result['word']
                this_word_dict['fear'] = headline_word_data_result['fear']
                this_word_dict['anger'] = headline_word_data_result['anger']
                this_word_dict['anticip'] = headline_word_data_result['anticip']
                this_word_dict['trust'] = headline_word_data_result['trust']
                this_word_dict['surprise'] = headline_word_data_result['surprise']
                this_word_dict['sadness'] = headline_word_data_result['sadness']
                this_word_dict['disgust'] = headline_word_data_result['disgust']
                this_word_dict['joy'] = headline_word_data_result['joy']
                headline_word_data_list.append(this_word_dict)
        for emotion in all_headlines_emotion_tally_dict:
            for word_dict in headline_word_data_list:

                if emotion != "word" and word_dict[emotion] > 0:
                    all_headlines_emotion_tally_dict[emotion] += 1

    tally_list.append(all_headlines_emotion_tally_dict)

tally_percent = []


overall_emotions = tally_list, total_hls, tally_percent













def get_headline_tally_by_emotion(top_words_list, paper_num):
    tally_list = []
    total_hls = []
    for word in top_words_list:
        all_headline_ids_query = hl_tokens_emotions.objects.filter(date__contains=today).filter(day_order__lte=25).filter(newspaper=paper_num).filter(word=word).values("headline_id")
        all_headline_id_list = []
        all_headlines_emotion_tally_dict = {'word':word,'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'sadness':0, 'disgust':0, 'joy':0}
        for query_result in all_headline_ids_query:
            if query_result['headline_id'] not in all_headline_id_list:
                all_headline_id_list.append(query_result['headline_id'])
        total_hl_length = len(all_headline_id_list)
        total_hls.append(total_hl_length)

        for each_headline_id in all_headline_id_list:
            headline_word_data = hl_tokens_emotions.objects.filter(headline_id=each_headline_id).values('word', 'fear', 'anger', 'anticip', 'trust', 'surprise', 'sadness', 'disgust', 'joy' )
            headline_word_data_list = []
            for headline_word_data_result in headline_word_data:
                if headline_word_data_result['word'] != word:
                    this_word_dict = {}
                    this_word_dict['word'] = headline_word_data_result['word']
                    this_word_dict['fear'] = headline_word_data_result['fear']
                    this_word_dict['anger'] = headline_word_data_result['anger']
                    this_word_dict['anticip'] = headline_word_data_result['anticip']
                    this_word_dict['trust'] = headline_word_data_result['trust']
                    this_word_dict['surprise'] = headline_word_data_result['surprise']
                    this_word_dict['sadness'] = headline_word_data_result['sadness']
                    this_word_dict['disgust'] = headline_word_data_result['disgust']
                    this_word_dict['joy'] = headline_word_data_result['joy']
                    headline_word_data_list.append(this_word_dict)
            for emotion in all_headlines_emotion_tally_dict:
                for word_dict in headline_word_data_list:

                    if emotion != "word" and word_dict[emotion] > 0:
                        all_headlines_emotion_tally_dict[emotion] += 1

        tally_list.append(all_headlines_emotion_tally_dict)

    tally_percent = []




    return tally_list, total_hls, tally_percent








nyt_emotions = get_headline_tally_by_emotion(nyt_top_words, 1)
bbc_emotions = get_headline_tally_by_emotion(bbc_top_words, 2)
fn_emotions = get_headline_tally_by_emotion(fn_top_words, 3)


from django.db.models import Count


def save_to_db(emotion_set, paper_num):
    for word_dict in emotion_set[0]:
        yesterday_tally = top_words_emotions_tally.objects.filter(date__contains=yesterday).filter(word=word_dict['word']).filter(newspaper=paper_num).values('fear', 'anger', 'anticip', 'trust', 'surprise', 'sadness', 'disgust', 'joy')[0]
        word_tally_save_to_db = top_words_emotions_tally(newspaper=paper_num, word=word_dict['word'], fear=yesterday_tally['fear']+word_dict['fear'], anger=yesterday_tally['anger']+word_dict['anger'],anticip=yesterday_tally['anticip']+word_dict['anticip'],trust=yesterday_tally['trust']+word_dict['trust'],surprise=yesterday_tally['surprise']+word_dict['surprise'],sadness=yesterday_tally['sadness']+word_dict['sadness'],disgust=yesterday_tally['disgust']+word_dict['disgust'],joy=yesterday_tally['joy']+word_dict['joy'], )
        word_tally_save_to_db.save()

        if paper_num == 4:
            word_count = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(word=word_dict['word']).count()
        else:
            word_count = hl_tokens_emotions.objects.filter(newspaper=paper_num).filter(day_order__lte=25).filter(word=word_dict['word']).count()
        word_percent_save_to_db = top_words_emotions_percent(newspaper=paper_num, word=word_dict['word'], fear_percent=round((yesterday_tally['fear']+word_dict['fear'])/word_count,2), anger_percent=round((yesterday_tally['anger']+word_dict['anger'])/word_count,2),anticip_percent=round((yesterday_tally['anticip']+word_dict['anticip'])/word_count,2),trust_percent=round((yesterday_tally['trust']+word_dict['trust'])/word_count,2),surprise_percent=round((yesterday_tally['surprise']+word_dict['surprise'])/word_count,2),sadness_percent=round((yesterday_tally['sadness']+word_dict['sadness'])/word_count,2),disgust_percent=round((yesterday_tally['disgust']+word_dict['disgust'])/word_count,2),joy_percent=round((yesterday_tally['joy']+word_dict['joy'])/word_count,2), )
        word_percent_save_to_db.save()


save_to_db(nyt_emotions, 1)
save_to_db(bbc_emotions, 2)
save_to_db(fn_emotions, 3)
save_to_db(overall_emotions, 4)

#delete redundant html_caches to save space
html_cache_1 = html_cache.objects.filter(page_num=1).values('date')
html_cache_2 = html_cache.objects.filter(page_num=2).values('date')
html_cache_3 = html_cache.objects.filter(page_num=3).values('date')
html_cache_4 = html_cache.objects.filter(page_num=4).values('date')
html_cache_5 = html_cache.objects.filter(page_num=5).values('date')

if len(html_cache_1) > 2:
    html_cache.objects.filter(page_num=1).delete()
    print("deleted html_cache for page 1")
else:
    print('did not delete html_cache for page 1')

if len(html_cache_2) > 2:
    html_cache.objects.filter(page_num=2).delete()
    print("deleted html_cache for page 2")
else:
    print('did not delete html_cache for page 2')

if len(html_cache_3) > 2:
    html_cache.objects.filter(page_num=3).delete()
    print("deleted html_cache for page 3")
else:
    print('did not delete html_cache for page 3')

if len(html_cache_4) > 2:
    html_cache.objects.filter(page_num=4).delete()
    print("deleted html_cache for page 4")
else:
    print('did not delete html_cache for page 4')

if len(html_cache_5) > 2:
    html_cache.objects.filter(page_num=5).delete()
    print("deleted html_cache for page 5")
else:
    print('did not delete html_cache for page 5')