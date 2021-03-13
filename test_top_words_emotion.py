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
from custom_scraper.models import Headline_emotion
from custom_scraper.models import emotion_associated
from django.db.models import Avg
from custom_scraper.models import cooc_wc
from custom_scraper.models import hl_tokens

from custom_scraper.models import emotion
from datetime import date, timedelta
from datetime import datetime


class CustomScraper(object):
    def __init__(self):
        self.url = ""

    def scrape(self):
        print('scraping...')

if __name__ == '__main__':
    scraper = CustomScraper()
    scraper.scrape()


#Goal: database which lists top 50 words (overall, nytimes, bbc, fn), tallies the amount of headlines containing that word that indicate each type of emotion
#Result for transcription in db should be dict {  "word":{"newspaper": "fear": tally of headlines containing "word" that have words that indicate fear}, {"anger": ""} and so on}

#Get top 50 words dict for each newspaper and initialize dict for each word with each emotion headline count as 0
today = date.today() 

def get_top_50_words(paper_num):
    top_50_dict_for_paper = {}
    top_50_words_query = word_count_general.objects.filter(date__contains=today).filter(newspaper=paper_num).values("word")[:50]
    for result in top_50_words_query:
        top_50_dict_for_paper[result['word']] = {'fear':0, 'anger':0, 'anticip':0, 'trust':0, 'surprise':0, 'sadness':0, 'disgust':0, 'joy':0}
    

    return top_50_dict_for_paper
    
nyt_top_50_dict = get_top_50_words(1)
bbc_top_50_dict = get_top_50_words(2)
fn_top_50_dict = get_top_50_words(3)
overall_top_50_dict = get_top_50_words(4)

#For each word tally headlines containing that word that have words that indicate each emotion

def get_emotion(top_50_dict, paper_num):
    unique_headline_ids = []
    for top_word, emotions_tally in top_50_dict:
        

