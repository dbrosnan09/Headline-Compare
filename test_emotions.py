#!/usr/bin/env python                                                                                                                                                                

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
from custom_scraper.models import word_count_general
from custom_scraper.models import style_wc
from custom_scraper.models import Headlinewc
from custom_scraper.models import Headlinewrl
from custom_scraper.models import emotion
from django.db.models import Avg
from custom_scraper.models import cooc_wc
from custom_scraper.models import Headline_emotion



class CustomScraper(object):
    def __init__(self):
        self.url = ""

    def scrape(self):
        print('scraping...')

if __name__ == '__main__':
    scraper = CustomScraper()
    scraper.scrape()


all_headline_data = Headline_emotion.objects.filter(day_order__lte=25).values('headline', 'newspaper', 'date', 'link', 'day_order', 'sentiment', 'reading_level', 'headline_wc', 'fear', 'anger', 'anticip', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy')

nyt_emotions = {'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'positive':0, 'negative':0, 'sadness':0, 'disgust':0, 'joy':0}
bbc_emotions = {'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'positive':0, 'negative':0, 'sadness':0, 'disgust':0, 'joy':0}
fn_emotions = {'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'positive':0, 'negative':0, 'sadness':0, 'disgust':0, 'joy':0}

for i in all_headline_data:
    if i['newspaper'] == 1:
        nyt_emotions['fear'] += i['fear']
        nyt_emotions['anger'] += i['anger']
        nyt_emotions['anticip'] += i['anticip']
        nyt_emotions['trust'] += i['trust']
        nyt_emotions['surprise'] += i['surprise']
        nyt_emotions['positive'] += i['positive']
        nyt_emotions['negative'] += i['negative']
        nyt_emotions['sadness'] += i['sadness']
        nyt_emotions['disgust'] += i['disgust']
        nyt_emotions['joy'] += i['joy']
    if i['newspaper'] == 2:
        bbc_emotions['fear'] += i['fear']
        bbc_emotions['anger'] += i['anger']
        bbc_emotions['anticip'] += i['anticip']
        bbc_emotions['trust'] += i['trust']
        bbc_emotions['surprise'] += i['surprise']
        bbc_emotions['positive'] += i['positive']
        bbc_emotions['negative'] += i['negative']
        bbc_emotions['sadness'] += i['sadness']
        bbc_emotions['disgust'] += i['disgust']
        bbc_emotions['joy'] += i['joy']
    if i['newspaper'] == 3:
        fn_emotions['fear'] += i['fear']
        fn_emotions['anger'] += i['anger']
        fn_emotions['anticip'] += i['anticip']
        fn_emotions['trust'] += i['trust']
        fn_emotions['surprise'] += i['surprise']
        fn_emotions['positive'] += i['positive']
        fn_emotions['negative'] += i['negative']
        fn_emotions['sadness'] += i['sadness']
        fn_emotions['disgust'] += i['disgust']
        fn_emotions['joy'] += i['joy']


print(nyt_emotions)
print(bbc_emotions)
print(fn_emotions)

