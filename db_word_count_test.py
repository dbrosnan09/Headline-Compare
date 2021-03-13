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





"""
      cooc_save_to_db = cooc(base_word=y[0], co_word=y[1], newspaper=y[2], co_word_count=y[3])
      cooc_save_to_db.save()
"""