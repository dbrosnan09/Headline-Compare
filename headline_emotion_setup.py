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

all_headline_data = Headline.objects.values('headline', 'newspaper', 'date', 'link', 'day_order', 'sentiment', )

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

for i in all_headline_data:
    headline_string = i['headline']
    list_of_words = get_sorted_word_count_by_string(headline_string)
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

    emotion_save_to_db = Headline_emotion(date=i['date'], headline=i['headline'], newspaper=i['newspaper'],link=i['link'], day_order=i['day_order'], sentiment=i['sentiment'], reading_level=0, headline_wc=0, fear=emotion_dict['fear'], anger=emotion_dict['anger'], anticip=emotion_dict['anticip'], trust=emotion_dict['trust'], surprise=emotion_dict['surprise'], positive=emotion_dict['positive'], negative=emotion_dict['negative'], sadness=emotion_dict['sadness'], disgust=emotion_dict['disgust'], joy=emotion_dict['joy'],  )
    emotion_save_to_db.save()

           



        




"""
      cooc_save_to_db = cooc(base_word=y[0], co_word=y[1], newspaper=y[2], co_word_count=y[3])
      cooc_save_to_db.save()
"""