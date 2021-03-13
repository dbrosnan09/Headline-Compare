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




class CustomScraper(object):
    def __init__(self):
        self.url = ""

    def scrape(self):
        print('scraping...')

if __name__ == '__main__':
    scraper = CustomScraper()
    scraper.scrape()


import re

keyword_regex = r"([a-z]*)--.*	([a-z]*)	([0-9])"

with open("NRC.txt") as f:
    emotion_lex_dict = {}
    for i in f.readlines():
        if re.search(keyword_regex, i):
            keyword = re.search(keyword_regex, i).group(1)
            emotional = re.search(keyword_regex, i).group(2)
            score = re.search(keyword_regex, i).group(3)
            if keyword not in emotion_lex_dict:
                emotion_lex_dict[keyword] = {}
                emotion_lex_dict[keyword][emotional] = score
            else:
                emotion_lex_dict[keyword][emotional] = score
            

for i in emotion_lex_dict:
    emotion_save_to_db = emotion(word=i,fear=emotion_lex_dict[i]['fear'], anger=emotion_lex_dict[i]['anger'], anticip=emotion_lex_dict[i]['anticip'], trust=emotion_lex_dict[i]['trust'], surprise=emotion_lex_dict[i]['surprise'], positive=emotion_lex_dict[i]['positive'], negative=emotion_lex_dict[i]['negative'], sadness=emotion_lex_dict[i]['sadness'], disgust=emotion_lex_dict[i]['disgust'], joy=emotion_lex_dict[i]['joy'],          )
    emotion_save_to_db.save()
"""
      cooc_save_to_db = cooc(base_word=y[0], co_word=y[1], newspaper=y[2], co_word_count=y[3])
      cooc_save_to_db.save()
"""     