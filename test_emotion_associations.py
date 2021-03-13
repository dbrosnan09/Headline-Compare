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

from custom_scraper.models import emotion



class CustomScraper(object):
    def __init__(self):
        self.url = ""

    def scrape(self):
        print('scraping...')

if __name__ == '__main__':
    scraper = CustomScraper()
    scraper.scrape()





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


emotion_list_2 = [ 'trust', 'joy', 'anticipation', 'surprise', 'fear', 'sadness', 'anger','disgust']


trust_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(trust__gte=1).values('headline')

trust_headlines_string = ""

for i in trust_headlines:
    trust_headlines_string += " " + i['headline']


trust_sorted_word_count = get_sorted_word_count_by_string(trust_headlines_string)[1:]


trust_associated_words = []

for x,y in trust_sorted_word_count:
    if not emotion.objects.filter(word=x).values('word') or x =="trump":
        interlist = []
        interlist.append(x)
        interlist.append(y)
        trust_associated_words.append(interlist)


joy_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(joy__gte=1).values('headline')

joy_headlines_string = ""

for i in joy_headlines:
    joy_headlines_string += " " + i['headline']


joy_sorted_word_count = get_sorted_word_count_by_string(joy_headlines_string)[1:]


joy_associated_words = []

for x,y in joy_sorted_word_count:
    if not emotion.objects.filter(word=x).values('word') or x =="trump":
        interlist = []
        interlist.append(x)
        interlist.append(y)
        joy_associated_words.append(interlist)

anticip_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(anticip__gte=1).values('headline')

anticip_headlines_string = ""

for i in anticip_headlines:
    anticip_headlines_string += " " + i['headline']


anticip_sorted_word_count = get_sorted_word_count_by_string(anticip_headlines_string)[1:]


anticip_associated_words = []

for x,y in anticip_sorted_word_count:
    if not emotion.objects.filter(word=x).values('word') or x =="trump":
        interlist = []
        interlist.append(x)
        interlist.append(y)
        anticip_associated_words.append(interlist)




surprise_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(surprise__gte=1).values('headline')

surprise_headlines_string = ""

for i in surprise_headlines:
    surprise_headlines_string += " " + i['headline']


surprise_sorted_word_count = get_sorted_word_count_by_string(surprise_headlines_string)[1:]


surprise_associated_words = []

for x,y in surprise_sorted_word_count:
    if not emotion.objects.filter(word=x).values('word') or x =="trump":
        interlist = []
        interlist.append(x)
        interlist.append(y)
        surprise_associated_words.append(interlist)




fear_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(fear__gte=1).values('headline')

fear_headlines_string = ""

for i in fear_headlines:
    fear_headlines_string += " " + i['headline']


fear_sorted_word_count = get_sorted_word_count_by_string(fear_headlines_string)[1:]


fear_associated_words = []

for x,y in fear_sorted_word_count:
    if not emotion.objects.filter(word=x).values('word') or x =="trump":
        interlist = []
        interlist.append(x)
        interlist.append(y)
        fear_associated_words.append(interlist)



sadness_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(sadness__gte=1).values('headline')

sadness_headlines_string = ""

for i in sadness_headlines:
    sadness_headlines_string += " " + i['headline']


sadness_sorted_word_count = get_sorted_word_count_by_string(sadness_headlines_string)[1:]


sadness_associated_words = []

for x,y in sadness_sorted_word_count:
    if not emotion.objects.filter(word=x).values('word') or x =="trump":
        interlist = []
        interlist.append(x)
        interlist.append(y)
        sadness_associated_words.append(interlist)



anger_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(anger__gte=1).values('headline')

anger_headlines_string = ""

for i in anger_headlines:
    anger_headlines_string += " " + i['headline']


anger_sorted_word_count = get_sorted_word_count_by_string(anger_headlines_string)[1:]


anger_associated_words = []

for x,y in anger_sorted_word_count:
    if not emotion.objects.filter(word=x).values('word') or x =="trump":
        interlist = []
        interlist.append(x)
        interlist.append(y)
        anger_associated_words.append(interlist)



disgust_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(disgust__gte=1).values('headline')

disgust_headlines_string = ""

for i in disgust_headlines:
    disgust_headlines_string += " " + i['headline']


disgust_sorted_word_count = get_sorted_word_count_by_string(disgust_headlines_string)[1:]


disgust_associated_words = []

for x,y in disgust_sorted_word_count:
    if not emotion.objects.filter(word=x).values('word') or x =="trump":
        interlist = []
        interlist.append(x)
        interlist.append(y)
        disgust_associated_words.append(interlist)


trust_associated_words = trust_associated_words[:100]
joy_associated_words = joy_associated_words[:100]
anticip_associated_words = anticip_associated_words[:100]
surprise_associated_words = surprise_associated_words[:100]
fear_associated_words = fear_associated_words[:100]
sadness_associated_words = sadness_associated_words[:100]
anger_associated_words = anger_associated_words[:100]
disgust_associated_words = disgust_associated_words[:100]

"""
      cooc_save_to_db = cooc(base_word=y[0], co_word=y[1], newspaper=y[2], co_word_count=y[3])
      cooc_save_to_db.save()
"""

for x,y in trust_associated_words:
    assocs_save_to_db = emotion_associated(newspaper=4, emotion='trust', word=x, word_count=y)
    assocs_save_to_db.save()


for x,y in joy_associated_words:
    assocs_save_to_db = emotion_associated(newspaper=4, emotion='joy', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in anticip_associated_words:
    assocs_save_to_db = emotion_associated(newspaper=4, emotion='anticip', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in surprise_associated_words:
    assocs_save_to_db = emotion_associated(newspaper=4, emotion='surprise', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in fear_associated_words:
    assocs_save_to_db = emotion_associated(newspaper=4, emotion='fear', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in sadness_associated_words:
    assocs_save_to_db = emotion_associated(newspaper=4, emotion='sadness', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in anger_associated_words:
    assocs_save_to_db = emotion_associated(newspaper=4, emotion='anger', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in disgust_associated_words:
    assocs_save_to_db = emotion_associated(newspaper=4, emotion='disgust', word=x, word_count=y)
    assocs_save_to_db.save()








def get_associated_words_by_paper(paper_num):
    trust_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(trust__gte=1).values('headline')

    trust_headlines_string = ""

    for i in trust_headlines:
        trust_headlines_string += " " + i['headline']


    trust_sorted_word_count = get_sorted_word_count_by_string(trust_headlines_string)[1:]


    trust_associated_words = []

    for x,y in trust_sorted_word_count:
        if not emotion.objects.filter(word=x).values('word') or x =="trump":
            interlist = []
            interlist.append(x)
            interlist.append(y)
            trust_associated_words.append(interlist)


    joy_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(joy__gte=1).values('headline')

    joy_headlines_string = ""

    for i in joy_headlines:
        joy_headlines_string += " " + i['headline']


    joy_sorted_word_count = get_sorted_word_count_by_string(joy_headlines_string)[1:]


    joy_associated_words = []

    for x,y in joy_sorted_word_count:
        if not emotion.objects.filter(word=x).values('word') or x =="trump":
            interlist = []
            interlist.append(x)
            interlist.append(y)
            joy_associated_words.append(interlist)

    anticip_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(anticip__gte=1).values('headline')

    anticip_headlines_string = ""

    for i in anticip_headlines:
        anticip_headlines_string += " " + i['headline']


    anticip_sorted_word_count = get_sorted_word_count_by_string(anticip_headlines_string)[1:]


    anticip_associated_words = []

    for x,y in anticip_sorted_word_count:
        if not emotion.objects.filter(word=x).values('word') or x =="trump":
            interlist = []
            interlist.append(x)
            interlist.append(y)
            anticip_associated_words.append(interlist)




    surprise_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(surprise__gte=1).values('headline')

    surprise_headlines_string = ""

    for i in surprise_headlines:
        surprise_headlines_string += " " + i['headline']


    surprise_sorted_word_count = get_sorted_word_count_by_string(surprise_headlines_string)[1:]


    surprise_associated_words = []

    for x,y in surprise_sorted_word_count:
        if not emotion.objects.filter(word=x).values('word') or x =="trump":
            interlist = []
            interlist.append(x)
            interlist.append(y)
            surprise_associated_words.append(interlist)




    fear_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(fear__gte=1).values('headline')

    fear_headlines_string = ""

    for i in fear_headlines:
        fear_headlines_string += " " + i['headline']


    fear_sorted_word_count = get_sorted_word_count_by_string(fear_headlines_string)[1:]


    fear_associated_words = []

    for x,y in fear_sorted_word_count:
        if not emotion.objects.filter(word=x).values('word') or x =="trump":
            interlist = []
            interlist.append(x)
            interlist.append(y)
            fear_associated_words.append(interlist)



    sadness_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(sadness__gte=1).values('headline')

    sadness_headlines_string = ""

    for i in sadness_headlines:
        sadness_headlines_string += " " + i['headline']


    sadness_sorted_word_count = get_sorted_word_count_by_string(sadness_headlines_string)[1:]


    sadness_associated_words = []

    for x,y in sadness_sorted_word_count:
        if not emotion.objects.filter(word=x).values('word') or x =="trump":
            interlist = []
            interlist.append(x)
            interlist.append(y)
            sadness_associated_words.append(interlist)



    anger_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(anger__gte=1).values('headline')

    anger_headlines_string = ""

    for i in anger_headlines:
        anger_headlines_string += " " + i['headline']


    anger_sorted_word_count = get_sorted_word_count_by_string(anger_headlines_string)[1:]


    anger_associated_words = []

    for x,y in anger_sorted_word_count:
        if not emotion.objects.filter(word=x).values('word') or x =="trump":
            interlist = []
            interlist.append(x)
            interlist.append(y)
            anger_associated_words.append(interlist)



    disgust_headlines = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(disgust__gte=1).values('headline')

    disgust_headlines_string = ""

    for i in disgust_headlines:
        disgust_headlines_string += " " + i['headline']


    disgust_sorted_word_count = get_sorted_word_count_by_string(disgust_headlines_string)[1:]


    disgust_associated_words = []

    for x,y in disgust_sorted_word_count:
        if not emotion.objects.filter(word=x).values('word') or x =="trump":
            interlist = []
            interlist.append(x)
            interlist.append(y)
            disgust_associated_words.append(interlist)


    trust_associated_words = trust_associated_words[:100]
    joy_associated_words = joy_associated_words[:100]
    anticip_associated_words = anticip_associated_words[:100]
    surprise_associated_words = surprise_associated_words[:100]
    fear_associated_words = fear_associated_words[:100]
    sadness_associated_words = sadness_associated_words[:100]
    anger_associated_words = anger_associated_words[:100]
    disgust_associated_words = disgust_associated_words[:100]

    return trust_associated_words, joy_associated_words, anticip_associated_words, surprise_associated_words, fear_associated_words, sadness_associated_words, anger_associated_words, disgust_associated_words

nyt_associated_words = get_associated_words_by_paper(1)

for x,y in nyt_associated_words[0]:
    assocs_save_to_db = emotion_associated(newspaper=1, emotion='trust', word=x, word_count=y)
    assocs_save_to_db.save()


for x,y in nyt_associated_words[1]:
    assocs_save_to_db = emotion_associated(newspaper=1, emotion='joy', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in nyt_associated_words[2]:
    assocs_save_to_db = emotion_associated(newspaper=1, emotion='anticip', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in nyt_associated_words[3]:
    assocs_save_to_db = emotion_associated(newspaper=1, emotion='surprise', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in nyt_associated_words[4]:
    assocs_save_to_db = emotion_associated(newspaper=1, emotion='fear', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in nyt_associated_words[5]:
    assocs_save_to_db = emotion_associated(newspaper=1, emotion='sadness', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in nyt_associated_words[6]:
    assocs_save_to_db = emotion_associated(newspaper=1, emotion='anger', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in nyt_associated_words[7]:
    assocs_save_to_db = emotion_associated(newspaper=1, emotion='disgust', word=x, word_count=y)
    assocs_save_to_db.save()




bbc_associated_words = get_associated_words_by_paper(2)
for x,y in bbc_associated_words[0]:
    assocs_save_to_db = emotion_associated(newspaper=2, emotion='trust', word=x, word_count=y)
    assocs_save_to_db.save()


for x,y in bbc_associated_words[1]:
    assocs_save_to_db = emotion_associated(newspaper=2, emotion='joy', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in bbc_associated_words[2]:
    assocs_save_to_db = emotion_associated(newspaper=2, emotion='anticip', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in bbc_associated_words[3]:
    assocs_save_to_db = emotion_associated(newspaper=2, emotion='surprise', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in bbc_associated_words[4]:
    assocs_save_to_db = emotion_associated(newspaper=2, emotion='fear', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in bbc_associated_words[5]:
    assocs_save_to_db = emotion_associated(newspaper=2, emotion='sadness', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in bbc_associated_words[6]:
    assocs_save_to_db = emotion_associated(newspaper=2, emotion='anger', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in bbc_associated_words[7]:
    assocs_save_to_db = emotion_associated(newspaper=2, emotion='disgust', word=x, word_count=y)
    assocs_save_to_db.save()






fn_associated_words = get_associated_words_by_paper(3)
for x,y in fn_associated_words[0]:
    assocs_save_to_db = emotion_associated(newspaper=3, emotion='trust', word=x, word_count=y)
    assocs_save_to_db.save()


for x,y in fn_associated_words[1]:
    assocs_save_to_db = emotion_associated(newspaper=3, emotion='joy', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in fn_associated_words[2]:
    assocs_save_to_db = emotion_associated(newspaper=3, emotion='anticip', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in fn_associated_words[3]:
    assocs_save_to_db = emotion_associated(newspaper=3, emotion='surprise', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in fn_associated_words[4]:
    assocs_save_to_db = emotion_associated(newspaper=3, emotion='fear', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in fn_associated_words[5]:
    assocs_save_to_db = emotion_associated(newspaper=3, emotion='sadness', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in fn_associated_words[6]:
    assocs_save_to_db = emotion_associated(newspaper=3, emotion='anger', word=x, word_count=y)
    assocs_save_to_db.save()

for x,y in fn_associated_words[7]:
    assocs_save_to_db = emotion_associated(newspaper=3, emotion='disgust', word=x, word_count=y)
    assocs_save_to_db.save()


