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
from custom_scraper.models import Headlinewrl
from custom_scraper.models import Headlinewc
from custom_scraper.models import total_word_count
from custom_scraper.models import cooc
from custom_scraper.models import Headline_emotion
from custom_scraper.models import emotion
from custom_scraper.models import hl_tokens_emotions
from custom_scraper.models import top_words_emotions_tally
from custom_scraper.models import top_words_emotions_percent
from custom_scraper.models import word_count_general
from datetime import date, timedelta

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

#find top words for each newspaper
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
yesterday = date.today() - timedelta(days=1)
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


#get tally for the required date range (Dec 23 to Dec 30)

def get_headline_tally_by_emotion(top_words_list, paper_num):
    tally_list = []
    total_hls = []
    for word in top_words_list:
        all_headline_ids_query = hl_tokens_emotions.objects.filter(date__range=["2020-12-23", "2020-12-30"]).filter(day_order__lte=25).filter(newspaper=paper_num).filter(word=word).values("headline_id")
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

print("Should be right below:")
print(nyt_emotions[0])


def save_to_db(emotion_set, paper_num):
    for word_dict in emotion_set[0]:
        yesterday_tally = top_words_emotions_tally.objects.filter(date__contains="2020-12-22").filter(word=word_dict['word']).filter(newspaper=paper_num).values('fear', 'anger', 'anticip', 'trust', 'surprise', 'sadness', 'disgust', 'joy')[0]
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