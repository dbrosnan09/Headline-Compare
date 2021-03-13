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
from django.db.models import Count
from custom_scraper.models import top_words_emotions_tally
from custom_scraper.models import top_words_emotions_percent


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


