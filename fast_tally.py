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
from custom_scraper.models import hl_tokenized_id
from custom_scraper.models import hl_tokens_emotions
from django.db.models import Avg
from custom_scraper.models import cooc_wc
import plotly.graph_objects as go
import plotly
from custom_scraper.models import emotion
from django.db.models import Max

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



#goal: tally the top word emotions

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



today = date.today() 


#find tally added by just scraped headlines:


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

for i in overall_emotions:
    print(i)