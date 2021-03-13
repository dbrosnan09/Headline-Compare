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
from custom_scraper.models import html_cache
from custom_scraper.models import hl_tokens_emotions
from datetime import date, timedelta
today = date.today() 
yesterday = date.today() - timedelta(days=1)
top_words_lista = ['biden']

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


a = get_headline_tally_by_emotion(top_words_lista,2)

print(a[0])
print(a[1])
print(a[2])