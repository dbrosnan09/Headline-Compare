from django.shortcuts import render
from django.utils import timezone
from .models import Headline
# Create your views here.
from datetime import date, timedelta
from textblob import TextBlob
from .models import Photos
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import WordCountSearch
from .forms import SentimentWordSearch
from .forms import SentimentDateSearch
from .forms import DateForm
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models.functions import TruncDay
from django.db.models import Avg
import pandas as pd 
import plotly.express as px
import plotly
from django.db.models.functions import TruncMonth








today = date.today() 
yesterday = date.today() - timedelta(days=1)

def mainpage(request):

    today1 = today
    print(today)
    nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
    if not nytheadlines:
        nytheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1).filter(day_order__lte=25)

    bbcheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=2).filter(day_order__lte=25)
    if not bbcheadlines:
        bbcheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2).filter(day_order__lte=25)

    fnheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=3).filter(day_order__lte=25)
    if not fnheadlines:
        fnheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3).filter(day_order__lte=25)
    
    nyt_sentiment_score = Headline.objects.filter(date__contains=today).filter(newspaper=1)
    if not nyt_sentiment_score:
        nyt_sentiment_score = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1)
    
    bbc_sentiment_score = Headline.objects.filter(date__contains=today).filter(newspaper=2)
    if not bbc_sentiment_score:
        bbc_sentiment_score = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2)
    
    fn_sentiment_score = Headline.objects.filter(date__contains=today).filter(newspaper=3)
    if not fn_sentiment_score:
        fn_sentiment_score = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3)
        today1=yesterday


    ny_score = 0
    for i in nyt_sentiment_score:
        ny_score += i.sentiment
    ny_score = ny_score/len(nyt_sentiment_score)
    ny_score = round(ny_score*100,1)
    
    bbc_score = 0
    for i in bbc_sentiment_score:
        bbc_score += i.sentiment
    bbc_score = bbc_score/len(bbc_sentiment_score)
    bbc_score = round(bbc_score*100,1)

    fn_score = 0
    for i in fn_sentiment_score:
        fn_score += i.sentiment
    fn_score = fn_score/len(fn_sentiment_score)
    fn_score = round(fn_score*100,1)  

    overall_score = round((ny_score + bbc_score + fn_score)/3,1)
    
    import nltk
    from nltk.corpus import stopwords
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list
        
    
    
    allkeywords = nytheadlines | bbcheadlines | fnheadlines
    allkeywords = find_keywords(allkeywords)

    nykeywords = find_keywords(nytheadlines)
    bbckeywords = find_keywords(bbcheadlines)
    fnkeywords = find_keywords(fnheadlines)


    all_wf_keys = []
    all_wf_values = []    
    keyword_counter = 0
    for v in allkeywords:
        if keyword_counter < 5:
            all_wf_values.append(v[0])
            all_wf_keys.append(v[1])
        keyword_counter += 1
    
    key1 = all_wf_keys[0]
    freq1 = all_wf_values[0]
    key2 = all_wf_keys[1]
    freq2 = all_wf_values[1]
    key3 = all_wf_keys[2]
    freq3 = all_wf_values[2]


    stopwords = nltk.corpus.stopwords.words('english')
        
        
        
    headlineslist = []
    for i in (nytheadlines | bbcheadlines | fnheadlines):
        headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
    for i in headlineslist:
        if i.lower() not in stopwords:
            without_stopwords.append(i)
        
    without_stopwords_string = " ".join(without_stopwords)
        
    texta = TextBlob(without_stopwords_string)

    import nltk, collections
    from nltk.util import ngrams
    ##bigrams today
    texta = str(texta).lower()
    tokenized = texta.split()
    hlBigrams = ngrams(tokenized, 2)
    hlBigramFreq = collections.Counter(hlBigrams)
    
    mostpopular = []
    for i in hlBigramFreq.most_common(3):
        mostpopular.append(i)
    
    phrase1 = str(mostpopular[0][0][0]) + " " + str(mostpopular[0][0][1])
    phrase1freq = str(mostpopular[0][1])
    

    phrase2 = str(mostpopular[1][0][0]) + " " + str(mostpopular[1][0][1])
    phrase2freq = str(mostpopular[1][1])

    phrase3 = str(mostpopular[2][0][0]) + " " + str(mostpopular[2][0][1])
    phrase3freq = str(mostpopular[2][1])  

    headlines_for_country = []
    for i in (nytheadlines | bbcheadlines | fnheadlines):
        headlines_for_country.append(i.headline)
        headlines_for_country_string = " ".join(headlineslist)
    
    from geotext import GeoText

    places = GeoText(headlines_for_country_string)
    cities_mentioned_today = places.cities
    countries_mentioned_today = places.country_mentions
    print(cities_mentioned_today)
    print(countries_mentioned_today)

    cities_mentioned = list((x,cities_mentioned_today.count(x))for x in set(cities_mentioned_today))
    cities_sorted = sorted(cities_mentioned, key=lambda x: x[1],reverse=True)
    
    city1 = cities_sorted[0][0]
    if len(cities_sorted) < 2:
        city2 = "None"
    else:
        city2 = cities_sorted[1][0]
    if len(cities_sorted) < 3:
        city3 ="None"
    else:
        city3 = cities_sorted[2][0]
    
        

    city1freq = cities_sorted[0][1]
    if len(cities_sorted) < 2:
        city2freq = 0
    else:
        city2freq = cities_sorted[1][1]
    if len(cities_sorted) < 3:
        city3freq = 0
    else:
        city3freq = cities_sorted[2][1]

    from iso3166 import countries

    top_countries = []
    for key, value in countries_mentioned_today.items():
        interlist = []
        interlist.append(key)
        interlist.append(value)
        top_countries.append(interlist)
    
    for i in top_countries:
        i[0] = countries.get(i[0]).name

    country1 = top_countries[0][0]
    country2 = top_countries[1][0]
    country3 = top_countries[2][0]

    country1freq = top_countries[0][1]
    country2freq = top_countries[1][1]
    country3freq = top_countries[2][1]

    print(top_countries)
    
    nyt_question_count = 0
    for i in nytheadlines:
        if "?" in str(i.headline):
            nyt_question_count += 1
    
    bbc_question_count = 0
    for i in bbcheadlines:
        if "?" in str(i.headline):
            bbc_question_count += 1
        
    fn_question_count = 0
    for i in fnheadlines:
        if "?" in str(i.headline):
            fn_question_count += 1

    
    nyt_exclamation_count = 0
    for i in nytheadlines:
        if "!" in str(i.headline):
            
            nyt_exclamation_count += 1
    
    bbc_exclamation_count = 0
    for i in bbcheadlines:
        if "!" in str(i.headline):
            bbc_exclamation_count += 1
        
    fn_exclamation_count = 0
    for i in fnheadlines:
        if "!" in str(i.headline):
            fn_exclamation_count += 1

    print(key1)
    key1_photo_link = Photos.objects.filter(keyword=key1).filter(date__contains=today).first()
    print(today1)


    form = DateForm()
    
    
    
    



   




    


    return render(request, 'custom_scraper/mainpage.html', {"nytheadlines":nytheadlines,"bbcheadlines":bbcheadlines,"fnheadlines":fnheadlines,"ny_score":ny_score, "bbc_score":bbc_score, "fn_score":fn_score, "overall_score":overall_score, "today1":today1,"allkeywords":allkeywords,"key1":key1,"key2":key2,"key3":key3,"freq1":freq1,"freq2":freq2,"freq3":freq3, "phrase1":phrase1, "phrase2":phrase2, "phrase3":phrase3, "phrase1freq":phrase1freq, "phrase2freq":phrase2freq, "phrase3freq":phrase3freq, "city1":city1, "city2":city2, "city3":city3, "city1freq": city1freq, "city2freq":city2freq, "city3freq":city3freq, "country1":country1, "country2":country2, "country3":country3, "country1freq":country1freq, "country2freq":country2freq, "country3freq":country3freq, "nyt_question_count":nyt_question_count,"bbc_question_count":bbc_question_count, "fn_question_count":fn_question_count,"nyt_exclamation_count":nyt_exclamation_count,"bbc_exclamation_count":bbc_exclamation_count,"fn_exclamation_count":fn_exclamation_count, "nytheadlines":nytheadlines, "bbcheadlines":bbcheadlines, "fnheadlines":fnheadlines, "key1_photo_link":key1_photo_link, "form":form,})

def Key1(request):
       
    import pandas as pd 
    import datetime
    form = WordCountSearch()
    import nltk
    from nltk.corpus import stopwords
    from django.db.models import Avg
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list
        
    today1 = today
    nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
    if not nytheadlines:
        nytheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1).filter(day_order__lte=25)

    bbcheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=2).filter(day_order__lte=25)
    if not bbcheadlines:
        bbcheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2).filter(day_order__lte=25)

    fnheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=3).filter(day_order__lte=25)
    if not fnheadlines:
        fnheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3).filter(day_order__lte=25)
    
    allkeywords = nytheadlines | bbcheadlines | fnheadlines
    allkeywords = find_keywords(allkeywords)

    nykeywords = find_keywords(nytheadlines)
    bbckeywords = find_keywords(bbcheadlines)
    fnkeywords = find_keywords(fnheadlines)


    all_wf_keys = []
    all_wf_values = []    
    keyword_counter = 0
    for v in allkeywords:
        if keyword_counter < 5:
            all_wf_values.append(v[0])
            all_wf_keys.append(v[1])
        keyword_counter += 1
    
    key1 = all_wf_keys[0]
    freq1 = all_wf_values[0]
    key2 = all_wf_keys[1]
    freq2 = all_wf_values[1]
    key3 = all_wf_keys[2]
    freq3 = all_wf_values[2]

    from django.db.models.functions import TruncDay
    from django.db.models import Count
    
    key1data = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date').annotate(Count=Count('id')).order_by("-Date")
    for i in key1data:
        print(i)
    
    import pandas as pd
    df = pd.DataFrame(list(key1data))

    import plotly.express as px
    fig = px.line(df, x="Date", y="Count", title='"' + str(key1.capitalize()) + '":' + " Total Count")
    fig.update_layout(
        font=dict(family="Roboto", size=15,color="black"), plot_bgcolor='white', xaxis_title='', margin=dict(pad=50)
    )

    
    import plotly
    

    html_div = str(plotly.offline.plot(fig, output_type='div'))

    key1data_by_paper = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Count=Count('id')).order_by("-Date")

    df2 = pd.DataFrame(list(key1data_by_paper))
    df2['newspaper'] = df2['newspaper'].replace(1, 'The New York Times')
    df2['newspaper'] = df2['newspaper'].replace(2, 'BBC News')
    df2['newspaper'] = df2['newspaper'].replace(3, 'Fox News')
    df2.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    print(df2)

    fig2 = px.line(df2, x="Date", y="Count", color='Newspaper', title='"' + str(key1.capitalize()) + '":' + " Count by Newspaper" )
    fig2.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(pad=50)
    )

    html_div2 = str(plotly.offline.plot(fig2, output_type='div'))

    average_key1_sentiment = Headline.objects.filter(headline__contains=key1).values('newspaper').annotate(Average=Avg('sentiment')).order_by("newspaper")
    df_average_key1_sentiment = pd.DataFrame(list(average_key1_sentiment))
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(1, 'The New York Times')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(2, 'BBC News')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(3, 'Fox News')
    df_average_key1_sentiment.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    df_average_key1_sentiment.rename(columns={'Average':'Sentiment Score'}, inplace= True)
    df_average_key1_sentiment['Sentiment Score'] = df_average_key1_sentiment['Sentiment Score'] * 100
    fig_average_key1_sentiment = px.bar(df_average_key1_sentiment, x='Newspaper', y='Sentiment Score', title='"'+str(key1.capitalize()) + '": ' + 'Average Sentiment by Newspaper')
    fig_average_key1_sentiment.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(pad=50)
    )

    html_div_average_key1_sentiment = str(plotly.offline.plot(fig_average_key1_sentiment, output_type='div'))

    print(key1)
    
    """
    dfkey1data = pd.DataFrame(list(Headline.objects.filter(headline__contains=key1).values('headline', 'date')))

    import plotly.express as px

    fig = px.line(dfkey1data, x="date") 
    
    for i in key1data:
        print(i)
    """
    nytkey1img = Photos.objects.filter(keyword=key1).filter(newspaper=1).filter(date__contains=today).first()
    fnkey1img = Photos.objects.filter(keyword=key1).filter(newspaper=3).filter(date__contains=today).first()
    bbckey1img = Photos.objects.filter(keyword=key1).filter(newspaper=2).filter(date__contains=today).first()
    print(nytkey1img)
    keystring = str(key1)
    return render(request, 'custom_scraper/key1.html',{'html_div':html_div,'html_div2':html_div2,'html_div_average_key1_sentiment':html_div_average_key1_sentiment, "nytkey1img":nytkey1img,'fnkey1img':fnkey1img, 'bbckey1img':bbckey1img,"keystring":keystring, "key1":key1, "form":form})


def Key2(request):

    import pandas as pd 
    import datetime
    form = WordCountSearch()
    import nltk
    from nltk.corpus import stopwords
    from django.db.models import Avg
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list
        
    today1 = today
    nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
    if not nytheadlines:
        nytheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1).filter(day_order__lte=25)

    bbcheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=2).filter(day_order__lte=25)
    if not bbcheadlines:
        bbcheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2).filter(day_order__lte=25)

    fnheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=3).filter(day_order__lte=25)
    if not fnheadlines:
        fnheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3).filter(day_order__lte=25)
    
    allkeywords = nytheadlines | bbcheadlines | fnheadlines
    allkeywords = find_keywords(allkeywords)

    nykeywords = find_keywords(nytheadlines)
    bbckeywords = find_keywords(bbcheadlines)
    fnkeywords = find_keywords(fnheadlines)


    all_wf_keys = []
    all_wf_values = []    
    keyword_counter = 0
    for v in allkeywords:
        if keyword_counter < 5:
            all_wf_values.append(v[0])
            all_wf_keys.append(v[1])
        keyword_counter += 1
    
    key1 = all_wf_keys[1]
    freq1 = all_wf_values[0]
    

    from django.db.models.functions import TruncDay
    from django.db.models import Count
    
    key1data = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date').annotate(Count=Count('id')).order_by("-Date")
    for i in key1data:
        print(i)
    
    import pandas as pd
    df = pd.DataFrame(list(key1data))

    import plotly.express as px
    fig = px.line(df, x="Date", y="Count", title='"' + str(key1.capitalize()) + '":' + " Total Count")
    fig.update_layout(
        font=dict(family="Roboto", size=15,color="black"), plot_bgcolor='white', xaxis_title='', margin=dict(pad=50)
    )

    
    import plotly
    

    html_div = str(plotly.offline.plot(fig, output_type='div'))

    key1data_by_paper = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Count=Count('id')).order_by("-Date")

    df2 = pd.DataFrame(list(key1data_by_paper))
    df2['newspaper'] = df2['newspaper'].replace(1, 'The New York Times')
    df2['newspaper'] = df2['newspaper'].replace(2, 'BBC News')
    df2['newspaper'] = df2['newspaper'].replace(3, 'Fox News')
    df2.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    print(df2)

    fig2 = px.line(df2, x="Date", y="Count", color='Newspaper', title='"' + str(key1.capitalize()) + '":' + " Count by Newspaper" )
    fig2.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(pad=50)
    )

    html_div2 = str(plotly.offline.plot(fig2, output_type='div'))

    average_key1_sentiment = Headline.objects.filter(headline__contains=key1).values('newspaper').annotate(Average=Avg('sentiment')).order_by("newspaper")
    df_average_key1_sentiment = pd.DataFrame(list(average_key1_sentiment))
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(1, 'The New York Times')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(2, 'BBC News')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(3, 'Fox News')
    df_average_key1_sentiment.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    df_average_key1_sentiment.rename(columns={'Average':'Sentiment Score'}, inplace= True)
    df_average_key1_sentiment['Sentiment Score'] = df_average_key1_sentiment['Sentiment Score'] * 100
    fig_average_key1_sentiment = px.bar(df_average_key1_sentiment, x='Newspaper', y='Sentiment Score', title='"'+str(key1.capitalize()) + '": ' + 'Average Sentiment by Newspaper')
    fig_average_key1_sentiment.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(pad=50)
    )

    html_div_average_key1_sentiment = str(plotly.offline.plot(fig_average_key1_sentiment, output_type='div'))

    print(key1)
    
    """
    dfkey1data = pd.DataFrame(list(Headline.objects.filter(headline__contains=key1).values('headline', 'date')))

    import plotly.express as px

    fig = px.line(dfkey1data, x="date") 
    
    for i in key1data:
        print(i)
    """
    nytkey1img = Photos.objects.filter(keyword=key1).filter(newspaper=1).filter(date__contains=today).first()
    fnkey1img = Photos.objects.filter(keyword=key1).filter(newspaper=3).filter(date__contains=today).first()
    bbckey1img = Photos.objects.filter(keyword=key1).filter(newspaper=2).filter(date__contains=today).first()
    print(nytkey1img)
    keystring = str(key1)
    return render(request, 'custom_scraper/key1.html',{'html_div':html_div,'html_div2':html_div2,'html_div_average_key1_sentiment':html_div_average_key1_sentiment, "nytkey1img":nytkey1img,'fnkey1img':fnkey1img, 'bbckey1img':bbckey1img,"keystring":keystring, "key1":key1, "form":form})       


def Key3(request):

    import pandas as pd 
    import datetime
    form = WordCountSearch()
    import nltk
    from nltk.corpus import stopwords
    from django.db.models import Avg
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list
        
    today1 = today
    nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
    if not nytheadlines:
        nytheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1).filter(day_order__lte=25)

    bbcheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=2).filter(day_order__lte=25)
    if not bbcheadlines:
        bbcheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2).filter(day_order__lte=25)

    fnheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=3).filter(day_order__lte=25)
    if not fnheadlines:
        fnheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3).filter(day_order__lte=25)
    
    allkeywords = nytheadlines | bbcheadlines | fnheadlines
    allkeywords = find_keywords(allkeywords)

    nykeywords = find_keywords(nytheadlines)
    bbckeywords = find_keywords(bbcheadlines)
    fnkeywords = find_keywords(fnheadlines)


    all_wf_keys = []
    all_wf_values = []    
    keyword_counter = 0
    for v in allkeywords:
        if keyword_counter < 5:
            all_wf_values.append(v[0])
            all_wf_keys.append(v[1])
        keyword_counter += 1
    
    key1 = all_wf_keys[2]
    freq1 = all_wf_values[0]
    

    from django.db.models.functions import TruncDay
    from django.db.models import Count
    
    key1data = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date').annotate(Count=Count('id')).order_by("-Date")
    for i in key1data:
        print(i)
    
    import pandas as pd
    df = pd.DataFrame(list(key1data))

    import plotly.express as px
    fig = px.line(df, x="Date", y="Count", title='"' + str(key1.capitalize()) + '":' + " Total Count")
    fig.update_layout(
        font=dict(family="Roboto", size=15,color="black"), plot_bgcolor='white', xaxis_title='', margin=dict(pad=50)
    )

    
    import plotly
    

    html_div = str(plotly.offline.plot(fig, output_type='div'))

    key1data_by_paper = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Count=Count('id')).order_by("-Date")

    df2 = pd.DataFrame(list(key1data_by_paper))
    df2['newspaper'] = df2['newspaper'].replace(1, 'The New York Times')
    df2['newspaper'] = df2['newspaper'].replace(2, 'BBC News')
    df2['newspaper'] = df2['newspaper'].replace(3, 'Fox News')
    df2.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    print(df2)

    fig2 = px.line(df2, x="Date", y="Count", color='Newspaper', title='"' + str(key1.capitalize()) + '":' + " Count by Newspaper" )
    fig2.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(pad=50)
    )

    html_div2 = str(plotly.offline.plot(fig2, output_type='div'))

    average_key1_sentiment = Headline.objects.filter(headline__contains=key1).values('newspaper').annotate(Average=Avg('sentiment')).order_by("newspaper")
    df_average_key1_sentiment = pd.DataFrame(list(average_key1_sentiment))
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(1, 'The New York Times')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(2, 'BBC News')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(3, 'Fox News')
    df_average_key1_sentiment.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    df_average_key1_sentiment.rename(columns={'Average':'Sentiment Score'}, inplace= True)
    df_average_key1_sentiment['Sentiment Score'] = df_average_key1_sentiment['Sentiment Score'] * 100
    fig_average_key1_sentiment = px.bar(df_average_key1_sentiment, x='Newspaper', y='Sentiment Score', title='"'+str(key1.capitalize()) + '": ' + 'Average Sentiment by Newspaper')
    fig_average_key1_sentiment.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(pad=50)
    )

    html_div_average_key1_sentiment = str(plotly.offline.plot(fig_average_key1_sentiment, output_type='div'))

    print(key1)
    
    """
    dfkey1data = pd.DataFrame(list(Headline.objects.filter(headline__contains=key1).values('headline', 'date')))

    import plotly.express as px

    fig = px.line(dfkey1data, x="date") 
    
    for i in key1data:
        print(i)
    """
    nytkey1img = Photos.objects.filter(keyword=key1).filter(newspaper=1).filter(date__contains=today).first()
    fnkey1img = Photos.objects.filter(keyword=key1).filter(newspaper=3).filter(date__contains=today).first()
    bbckey1img = Photos.objects.filter(keyword=key1).filter(newspaper=2).filter(date__contains=today).first()
    print(nytkey1img)
    keystring = str(key1)
    return render(request, 'custom_scraper/key1.html',{'html_div':html_div,'html_div2':html_div2,'html_div_average_key1_sentiment':html_div_average_key1_sentiment, "nytkey1img":nytkey1img,'fnkey1img':fnkey1img, 'bbckey1img':bbckey1img,"keystring":keystring, "key1":key1, "form":form})        



def SentimentScore(request):

    from django.db.models.functions import TruncDay
    from django.db.models import Avg

    overall_sentiment_by_date = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("-Date")
    
    import pandas as pd

    df3 = pd.DataFrame(list(overall_sentiment_by_date))
    df3['Average'] = df3['Average'] * 100
    

    import plotly.express as px
    fig = px.line(df3, x="Date", y="Average", title="Average Sentiment Score by Date")
    print(fig.data[0].name)

    import plotly

    html_div3 = str(plotly.offline.plot(fig, output_type='div'))

    average_sentiment_by_date_by_newspaper = Headline.objects.annotate(Date=TruncDay('date')).values('Date','newspaper').annotate(Average=Avg('sentiment')).order_by("-Date","newspaper")

    df4 = pd.DataFrame(list(average_sentiment_by_date_by_newspaper))
    df4['Average'] = df4['Average'] * 100
    df4['newspaper'] = df4['newspaper'].replace(1, 'The New York Times')
    df4['newspaper'] = df4['newspaper'].replace(2, 'BBC News')
    df4['newspaper'] = df4['newspaper'].replace(3, 'Fox News')


    fig4 = px.line(df4, x="Date", y="Average", color='newspaper', title="Daily Average Sentiment Score by Newspaper" )

    html_div4 = str(plotly.offline.plot(fig4, output_type='div'))

    for i in average_sentiment_by_date_by_newspaper:
        print(i)

    """
    key3data = Headline.objects.filter(headline__contains=key3).annotate(Date=TruncDay('date')).values('Date').annotate(Count=Count('id')).order_by("-Date")
    for i in key3data:
        print(i)
    
    import pandas as pd
    df = pd.DataFrame(list(key3data))

    import plotly.express as px
    fig = px.line(df, x="Date", y="Count", title='"' + str(key3.capitalize()) + '":' + " Total Count")
    print(fig.data[0].name)

    import plotly

    html_div = str(plotly.offline.plot(fig, output_type='div'))
    """

    
    import plotly.express as px
    import plotly
    from django.db.models import Count
    form = WordCountSearch()
    
    import pandas as pd 
    import datetime

    import nltk
    from nltk.corpus import stopwords
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list


    allheadlines = Headline.objects.all()
    

    allkeywords = find_keywords(allheadlines)
    
    print(allkeywords)

    top_100 = allkeywords[:100]
    """Most negative nytimes word"""
    
    wordsentiment_by_newspaper = []
    for i in top_100:
        word = i[1]
        average_key_sentiment = Headline.objects.filter(headline__contains=word).values('newspaper').annotate(Average=Avg('sentiment')).order_by("newspaper")
        wordsentiment_by_newspaper.append(list(average_key_sentiment))
    
    y = 0 
    for i in wordsentiment_by_newspaper:
        i.append(top_100[y][1])
        number = y + 1
        i.append(number)

        y += 1

    
    
   
    
    
    
    print(wordsentiment_by_newspaper) 
    
    
    """
   

    for i in wordsentiment_by_newspaper:
        if i[0]['newspaper'] == 1 and i[1]['newspaper'] == 2 and i[2]['newspaper'] == 3:
            print("OK")
        else:
            print("problem")       
            
    for i in wordsentiment_by_newspaper:
        if len(i) < 5:
            if i[0]['newspaper'] == 3:
                i[:0] = {'newspaper': 2, 'Average': 0}
    
    for i in wordsentiment_by_newspaper:
        if len(i) < 5:
            if i[0]['newspaper'] == 2:
                i[:0] = {'newspaper': 1, 'Average': 0}
    
    for i in wordsentiment_by_newspaper:
        if len(i) == 3 and i[0]['newspaper'] == 1:
            i.append({'newspaper': 2, 'Average': 0})
            
        elif len(i) == 3 and i[0]['newspaper'] == 2:
            i[:0] = {'newspaper': 1, 'Average': 0}
            
    
    
    
    for i in wordsentiment_by_newspaper:
        if len(i) < 5:
            if i[1]['newspaper'] != 2:
                i[:1] = {'newspaper': 2, 'Average': 0}
    for i in wordsentiment_by_newspaper:
        if len(i) < 5:
            if i[2]['newspaper'] != 3:
                i.append({'newspaper': 3, 'Average': 0})
    for i in wordsentiment_by_newspaper:
        if len(i) == 4 and i[0]['newspaper'] == 1 and i[1]['newspaper'] == 3:
            i[:1] = {'newspaper': 2, 'Average': 0}

    
    for i in wordsentiment_by_newspaper:
        if i[0]['newspaper'] == 1 and i[1]['newspaper'] == 2 and i[2]['newspaper'] == 3:
            print(i)
            print("OK")
        else:
            print(i)
            print("problem")  

    """


    """ the following ensures all words searched have a newspaper 1, 2 and 3 value so that the info can be used to create a graph"""
    key_default = "newspaper"
    nyt_value = 1
    y = 1 
    for i in wordsentiment_by_newspaper:
        if key_default in i[0] and i[0]['newspaper'] == 1:
            print("True")
            print(y)
            print(i)
            print(i[0])
            print(type(i[0]))
            y += 1
        else:
            print("False")
            print(y)
            print(i)
            print(y)
            i.insert(0,{'newspaper': 1, 'Average': 0})
            
            print(i)
            y += 1
    
    for i in wordsentiment_by_newspaper:
        if key_default in i[1] and i[1]['newspaper'] == 2:
            print("True")
            print(y)
            print(i)
            print(i[1])
            print(type(i[1]))
            y += 1
        else:
            print("False")
            print(y)
            print(i)
            print(y)
            i.insert(1,{'newspaper': 2, 'Average': 0})
            
            print(i)
            y += 1            


    for i in wordsentiment_by_newspaper:
        if key_default in i[2] and i[2]['newspaper'] == 3:
            print("True")
            print(y)
            print(i)
            print(i[2])
            print(type(i[2]))
            y += 1
        else:
            print("False")
            print(y)
            print(i)
            print(y)
            i.insert(2,{'newspaper': 3, 'Average': 0})
            
            print(i)
            y += 1      

    for i in wordsentiment_by_newspaper:
        if len(i) == 5:
            print("True")
        else:
            print("False")


   
    print(wordsentiment_by_newspaper)

    nyt_top_100_by_sentiment = []
    for i in wordsentiment_by_newspaper:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[3])
        nyt_top_100_by_sentiment.append(interlist)
    


    print(nyt_top_100_by_sentiment)

    sorted_nyt = sorted(nyt_top_100_by_sentiment, key = lambda i: i[0]['Average'] )
    
    worst3_nyt = sorted_nyt[:3]
    best3_nyt = sorted_nyt[(len(sorted_nyt)-3):]

    print(sorted_nyt)
    print(worst3_nyt)
    print(best3_nyt)


    bbc_top_100_by_sentiment = []
    for i in wordsentiment_by_newspaper:
        interlist = []
        interlist.append(i[1])
        interlist.append(i[3])
        bbc_top_100_by_sentiment.append(interlist)
    
    sorted_bbc = sorted(bbc_top_100_by_sentiment, key = lambda i: i[0]['Average'] )

    worst3_bbc = sorted_bbc[:3]
    best3_bbc = sorted_bbc[(len(sorted_bbc)-3):]

    fn_top_100_by_sentiment = []
    for i in wordsentiment_by_newspaper:
        interlist = []
        interlist.append(i[2])
        interlist.append(i[3])
        fn_top_100_by_sentiment.append(interlist)
    
    sorted_fn = sorted(fn_top_100_by_sentiment, key = lambda i: i[0]['Average'] )

    worst3_fn = sorted_fn[:3]
    best3_fn = sorted_fn[(len(sorted_fn)-3):]

    print(worst3_nyt)
    print(best3_nyt)
    print(worst3_bbc)
    print(best3_bbc)
    print(worst3_fn)
    print(best3_fn)




    
    
    

    return render(request, 'custom_scraper/SentimentScore.html', {'html_div3':html_div3,'html_div4':html_div4})

    
def WordCount(request):
    import plotly.express as px
    import plotly
    from django.db.models import Count
    form = WordCountSearch()
    
    import pandas as pd 
    import datetime

    import nltk
    from nltk.corpus import stopwords
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list


    allheadlines = Headline.objects.all()
    

    allkeywords = find_keywords(allheadlines)
    
    print(allheadlines)

    all_wf_keys = []
    all_wf_values = []    
    keyword_counter = 0
    for v in allkeywords:
        if keyword_counter < 11:
            all_wf_values.append(v[0])
            all_wf_keys.append(v[1])
        keyword_counter += 1
    
    key1 = all_wf_keys[0]
    
    key2 = all_wf_keys[1]
    
    key3 = all_wf_keys[2]

    key4 = all_wf_keys[3]
    
    key5 = all_wf_keys[4]
    
    key6 = all_wf_keys[5]

    key7 = all_wf_keys[6]
    
    key8 = all_wf_keys[7]
    
    key9 = all_wf_keys[8]
    
    key10 = all_wf_keys[9]

    def produce_data_list_of_freq_by_newspaper(freq_list, number_of_keys):
        counter = 0
        all_terms_list = []
        for i in freq_list:
            if  counter < number_of_keys:
                key = all_wf_keys[counter]
                print(key)
                if key == "us":
                    counter += 1
                    continue
                if key == "virus":
                    counter += 1
                    continue
                counter += 1
                key_count_by_paper = Headline.objects.filter(headline__contains=key).filter(day_order__lte=25).values("newspaper").annotate(Count=Count('id')).order_by("newspaper")
                print(list(key_count_by_paper))
                keylist = []
                keylist.append(key)
                
                nytimescount = key_count_by_paper[0]['Count']
                bbccount = key_count_by_paper[1]['Count']
                fncount = key_count_by_paper[2]['Count']
                keylist.append(nytimescount)
                keylist.append(bbccount)
                keylist.append(fncount)
                print(keylist)
                all_terms_list.append(keylist)
                
        return all_terms_list

    
    
    terms_nums = produce_data_list_of_freq_by_newspaper(all_wf_keys, 10)
    print(terms_nums)
    
    

    import plotly.graph_objects as go
    terms = []
    for i in terms_nums:
        terms.append(i[0])
    
    ny_values_list = []
    for i in terms_nums:
        ny_values_list.append(i[1])
    
    bbc_values_list = []
    for i in terms_nums:
        bbc_values_list.append(i[2])
    
    fn_values_list = []
    for i in terms_nums:
        fn_values_list.append(i[3])
    
    

    
    


    values_fig = go.Figure(data=[
        go.Bar(name='New York Times', y=terms, x=ny_values_list, orientation='h', marker_color="#2d2e30"),
        go.Bar(name='BBC News', y=terms, x=bbc_values_list, orientation = 'h', marker_color="#bb1919"),
        go.Bar(name='Fox News', y=terms, x=fn_values_list, orientation = 'h', marker_color="rgba(0,51,102,.99)"),
    ], )
    values_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, yaxis=dict(autorange="reversed"), margin=dict(t=10,pad=10), )
    
    
    

    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))   
    print(html_div_values)

    index = []
    nytimes = []
    bbc = []
    fn = []

    

    for i in produce_data_list_of_freq_by_newspaper(all_wf_keys, 10):
        index.append(i[0])
        nytimes.append(i[1])
        bbc.append(i[2])
        fn.append(i[3])
        
    


    
    produce_data_list_of_freq_by_newspaper = pd.DataFrame({'New York Times': nytimes, 'BBC News':bbc, 'Fox News':fn}, index=index) 
    print(produce_data_list_of_freq_by_newspaper)
   
    fig_produce = px.bar(produce_data_list_of_freq_by_newspaper, y= 'New York Times', x=produce_data_list_of_freq_by_newspaper.index)  
    html_div_produce = str(plotly.offline.plot(fig_produce, output_type='div'))    
          
    """           
    produce_data_list_of_freq_by_newspaper = pd.DataFrame(produce_data_list_of_freq_by_newspaper)
    print(produce_data_list_of_freq_by_newspaper)
    """
    

    key_data = list(zip(all_wf_keys, all_wf_values))
    print(key_data)
    key_data = pd.DataFrame(key_data)
    print(key_data)
    key_data.rename(columns={0:'Word'}, inplace=True)
    key_data.rename(columns={1:'Count'}, inplace=True)
    fig_key_data = px.bar(key_data, x='Count', y='Word', orientation='h', title="Most Common Words")
    fig_key_data.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', yaxis=dict(autorange="reversed")
    )


    html_div_key_data = str(plotly.offline.plot(fig_key_data, output_type='div'))

    """
    average_key1_sentiment = Headline.objects.filter(headline__contains=key1).values('newspaper').annotate(Average=Avg('sentiment')).order_by("newspaper")
    df_average_key1_sentiment = pd.DataFrame(list(average_key1_sentiment))
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(1, 'The New York Times')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(2, 'BBC News')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(3, 'Fox News')
    df_average_key1_sentiment.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    df_average_key1_sentiment.rename(columns={'Average':'Sentiment Score'}, inplace= True)
    df_average_key1_sentiment['Sentiment Score'] = df_average_key1_sentiment['Sentiment Score'] * 100
    fig_average_key1_sentiment = px.bar(df_average_key1_sentiment, x='Newspaper', y='Sentiment Score', title='"'+str(key1.capitalize()) + '": ' + 'Average Sentiment by Newspaper')
    fig_average_key1_sentiment.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white'
    )

    html_div_average_key1_sentiment = str(plotly.offline.plot(fig_average_key1_sentiment, output_type='div'))

    """
    return render(request, 'custom_scraper/WordCount.html', {'form':form,'key1':key1, 'key2': key2, 'key3': key3, 'key4':key4, 'key5': key5, 'key6': key6,  'key7':key7, 'key8': key8, 'key9': key9, 'key10':key10, 'html_div_key_data':html_div_key_data, 'html_div_produce':html_div_produce, 'html_div_values':html_div_values})


def word_count(request):
    search = request.GET.get('word_count')
    print(search)
    from django.db.models.functions import TruncDay
    from django.db.models import Count
    
    key1data = Headline.objects.filter(headline__contains=search).annotate(Date=TruncDay('date')).values('Date').annotate(Count=Count('id')).order_by("-Date")
    for i in key1data:
        print(i)
    
    from django.shortcuts import redirect
    if not key1data:
        
        request.session['search'] = search
        return redirect('research')

    import pandas as pd 
    import datetime
    form = WordCountSearch()
    import nltk
    from nltk.corpus import stopwords
    from django.db.models import Avg
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list
        
    today1 = today
    nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
    if not nytheadlines:
        nytheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1).filter(day_order__lte=25)

    bbcheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=2).filter(day_order__lte=25)
    if not bbcheadlines:
        bbcheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2).filter(day_order__lte=25)

    fnheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=3).filter(day_order__lte=25)
    if not fnheadlines:
        fnheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3).filter(day_order__lte=25)
    
    allkeywords = nytheadlines | bbcheadlines | fnheadlines
    allkeywords = find_keywords(allkeywords)

    nykeywords = find_keywords(nytheadlines)
    bbckeywords = find_keywords(bbcheadlines)
    fnkeywords = find_keywords(fnheadlines)


    all_wf_keys = []
    all_wf_values = []    
    keyword_counter = 0
    for v in allkeywords:
        if keyword_counter < 5:
            all_wf_values.append(v[0])
            all_wf_keys.append(v[1])
        keyword_counter += 1
    
    key1 = search
    freq1 = all_wf_values[0]
    

    from django.db.models.functions import TruncDay
    from django.db.models import Count
    
    key1data = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date').annotate(Count=Count('id')).order_by("-Date")
    for i in key1data:
        print(i)
    
    import pandas as pd
    df = pd.DataFrame(list(key1data))

    import plotly.express as px
    fig = px.line(df, x="Date", y="Count", title="Overall Count by Date",  color_discrete_sequence=['black'])
    fig.update_layout(
        font=dict(family="Roboto", size=15,color="black"), plot_bgcolor='white', xaxis_title='', margin=dict(pad=50),
    )
   
    
    import plotly
    

    html_div = str(plotly.offline.plot(fig, output_type='div',config = {'displayModeBar': False}, ))

    key1data_by_paper = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Count=Count('id')).order_by("-Date")

    df2 = pd.DataFrame(list(key1data_by_paper))
    df2['newspaper'] = df2['newspaper'].replace(1, 'The New York Times')
    df2['newspaper'] = df2['newspaper'].replace(2, 'BBC News')
    df2['newspaper'] = df2['newspaper'].replace(3, 'Fox News')
    df2.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    print(df2)

    fig2 = px.line(df2, x="Date", y="Count", color='Newspaper', color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }, title="Count by Newspaper by Date" )
    fig2.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',xaxis_title='', margin=dict(pad=50)
    )

    

    html_div2 = str(plotly.offline.plot(fig2, output_type='div',config = {'displayModeBar': False}))

    average_key1_sentiment = Headline.objects.filter(headline__contains=key1).values('newspaper').annotate(Average=Avg('sentiment')).order_by("newspaper")
    df_average_key1_sentiment = pd.DataFrame(list(average_key1_sentiment))
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(1, 'The New York Times')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(2, 'BBC News')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(3, 'Fox News')
    df_average_key1_sentiment.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    df_average_key1_sentiment.rename(columns={'Average':'Sentiment Score'}, inplace= True)
    df_average_key1_sentiment['Sentiment Score'] = df_average_key1_sentiment['Sentiment Score'] * 100
    fig_average_key1_sentiment = px.bar(df_average_key1_sentiment, x='Newspaper', y='Sentiment Score', title='"'+str(key1.capitalize()) + '": ' + 'Average Sentiment by Newspaper')
    fig_average_key1_sentiment.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(pad=50)
    )

    html_div_average_key1_sentiment = str(plotly.offline.plot(fig_average_key1_sentiment, output_type='div'))

    print(key1)
    
    """
    dfkey1data = pd.DataFrame(list(Headline.objects.filter(headline__contains=key1).values('headline', 'date')))

    import plotly.express as px

    fig = px.line(dfkey1data, x="date") 
    
    for i in key1data:
        print(i)
    """
    nytkey1img = Photos.objects.filter(keyword=key1).first()
    print(nytkey1img)
    img_html = "<img src=" + str(nytkey1img) + ">"
    dataflex_padding = "padding-top: 230px;"
    centered_font = "font-size:80px;"
   
    picflex_padding = "padding-top:150px;"
    centered_hover_color = "white"
    
    if not nytkey1img:
        img_html = ""
        dataflex_padding = "padding-top: 80px;"
        centered_font = "font-size:120px;"
        centered_hover_color = "black"
        picflex_padding = "padding-top: 30px;"
        
    print(nytkey1img)
    keystring = str(key1)
    print("This request went to word_count")

    headlines_contain_search = Headline.objects.filter(headline__contains=search)
    
    print(headlines_contain_search)
    
    nyt_hl_list = []
    bbc_hl_list = []
    fn_hl_list = []
    
    for i in headlines_contain_search:
        if i.newspaper == 1:
            nyt_hl_list.append(i)
        if i.newspaper == 2:
            bbc_hl_list.append(i)
        if i.newspaper == 3:
            fn_hl_list.append(i)

    print(nyt_hl_list)
    print(bbc_hl_list)
    print(fn_hl_list)

    print(len(nyt_hl_list))
    print(len(bbc_hl_list))
    print(len(fn_hl_list))

    

    nytl = len(nyt_hl_list)
    bbcl = len(bbc_hl_list)
    fnl = len(fn_hl_list)

    len_compare_list = []
    len_compare_list.append(nytl)
    len_compare_list.append(bbcl)
    len_compare_list.append(fnl)

    len_compare_list.sort()

    len_of_compare = len_compare_list[2]

    nyt_hl_list = nyt_hl_list[:len_of_compare]
    bbc_hl_list = bbc_hl_list[:len_of_compare]
    fn_hl_list = fn_hl_list[:len_of_compare]

    print(nyt_hl_list)
    print(bbc_hl_list)
    print(fn_hl_list)
    all_hl_list = []



    for i in range(len_of_compare):
        if i < len(nyt_hl_list):
            all_hl_list.append(nyt_hl_list[i].headline)
            all_hl_list.append(nyt_hl_list[i].date)
            all_hl_list.append(nyt_hl_list[i].link)
            all_hl_list.append(round(nyt_hl_list[i].sentiment * 100))
            
        else:
            all_hl_list.append("No further headlines from this newspaper")
            all_hl_list.append(" ")
            all_hl_list.append('https://www.nytimes.com')
            all_hl_list.append(0)
           
        if i < len(bbc_hl_list):
            all_hl_list.append(bbc_hl_list[i].headline)
            all_hl_list.append(bbc_hl_list[i].date)
            all_hl_list.append(bbc_hl_list[i].link)
            all_hl_list.append(round(bbc_hl_list[i].sentiment * 100))
           
        else:
            all_hl_list.append("No further headlines from this newspaper")
            all_hl_list.append(" ")
            all_hl_list.append('https://www.bbc.com/news')
            all_hl_list.append(0)
        
        if i < len(fn_hl_list):
            all_hl_list.append(fn_hl_list[i].headline)
            all_hl_list.append(fn_hl_list[i].date)
            all_hl_list.append(fn_hl_list[i].link)
            all_hl_list.append(round(fn_hl_list[i].sentiment *100))

        else:
            all_hl_list.append("No further headlines from this newspaper")
            all_hl_list.append(" ")
            all_hl_list.append("https://www.foxnews.com")
            all_hl_list.append(0)
    all_hl_only = []
   
    for i in range(0,len(all_hl_list)):
        all_hl_only.append(all_hl_list[i])
        


    print(all_hl_list)
    
    list_of_hl = []

    for i in range(0,len(all_hl_list), 4):
        interlist = []
        interlist.append(all_hl_list[i])
        interlist.append(all_hl_list[i+1])
        interlist.append(all_hl_list[i+2])
        interlist.append(all_hl_list[i + 3])
        list_of_hl.append(interlist)
    
    print(list_of_hl)

    """Count by Newspaper Graph"""

    nytimes_newscount = Headline.objects.filter(headline__contains=key1).filter(newspaper=1).filter(day_order__lte=25).annotate(Count=Count('id'))
    bbc_newscount = Headline.objects.filter(headline__contains=key1).filter(newspaper=2).filter(day_order__lte=25).annotate(Count=Count('id'))
    fn_newscount = Headline.objects.filter(headline__contains=key1).filter(newspaper=3).filter(day_order__lte=25).annotate(Count=Count('id'))
    
    bar_list = []
    bar_list.append(len(nytimes_newscount))
    bar_list.append(len(bbc_newscount))
    bar_list.append(len(fn_newscount))
    
    import plotly.graph_objects as go
    

    fig = go.Figure([go.Bar(x=['The New York Times','BBC News', 'Fox News'],  y=bar_list, marker_color=["#2d2e30","#bb1919","rgba(0,51,102,.99)"])])

    fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', title="Count by Newspaper",orientation=90, margin=dict(pad=50), )


    html_div_news_bar = str(plotly.offline.plot(fig, output_type='div', config = {'displayModeBar': False}))
    
    
    ny_sentiment = Headline.objects.filter(newspaper=1).filter(headline__contains=key1)
    bbc_sentiment = Headline.objects.filter(newspaper=2).filter(headline__contains=key1)
    fn_sentiment = Headline.objects.filter(newspaper=3).filter(headline__contains=key1)

    nyt_average = 0
    for i in ny_sentiment:
        nyt_average += i.sentiment
    
    if len(ny_sentiment) == 0:
        nyt_average = 0
    else:
        nyt_average = nyt_average/len(ny_sentiment)
        nyt_average = 100 * nyt_average
        nyt_average = round(nyt_average,2)
    
    bbc_average = 0
    for i in bbc_sentiment:
        bbc_average += i.sentiment
    
    if len(bbc_sentiment) == 0:
        bbc_average = 0
    else:
        bbc_average = bbc_average/len(bbc_sentiment)
        bbc_average = 100 * bbc_average
        bbc_average = round(bbc_average,2)

    fn_average = 0
    for i in fn_sentiment:
        fn_average += i.sentiment
    
    if len(fn_sentiment) == 0:
        fn_average = 0
    else:
        fn_average = fn_average/len(fn_sentiment)
        fn_average = 100 * fn_average
        fn_average = round(fn_average,2)

    averages = []
    averages.append(nyt_average)
    averages.append(bbc_average)
    averages.append(fn_average)

    average_sentiment_title = ["The New York Times", "BBC News", "Fox News"]

    sentiment_fig = go.Figure([go.Bar(x=average_sentiment_title, y=averages, marker_color=["#2d2e30","#bb1919","rgba(0,51,102,.99)" ])])

    sentiment_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', title="Average Sentiment by Newspaper",orientation=90, margin=dict(pad=50), )


    html_div_sentiment = str(plotly.offline.plot(sentiment_fig, output_type='div', config = {'displayModeBar': False}))

    from django.db.models.functions import TruncMonth

    average_sentiment_by_month_by_newspaper = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncMonth('date')).values('Date','newspaper').annotate(Average=Avg('sentiment')).order_by("-Date","newspaper")
    
    for i in average_sentiment_by_month_by_newspaper:
        print(i)

    dfas = pd.DataFrame(list(average_sentiment_by_month_by_newspaper))
    dfas['Average'] = dfas['Average'] * 100
    dfas['newspaper'] = dfas['newspaper'].replace(1, 'The New York Times')
    dfas['newspaper'] = dfas['newspaper'].replace(2, 'BBC News')
    dfas['newspaper'] = dfas['newspaper'].replace(3, 'Fox News')
    dfas.rename(columns={'newspaper':'Newspaper'}, inplace= True)


    figas = px.line(dfas, x="Date", y="Average", color='Newspaper', color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }, title="Average Sentiment by Newspaper by Month" )

    figas.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',xaxis_title='', margin=dict(pad=50))

    html_divas = str(plotly.offline.plot(figas, output_type='div', config = {'displayModeBar': False}))

    nyt_sentiment_pos = Headline.objects.filter(newspaper=1).filter(headline__contains=key1).filter(sentiment__gt=0)
    nyt_sentiment_neg = Headline.objects.filter(newspaper=1).filter(headline__contains=key1).filter(sentiment__lt=0)
    nyt_sentiment_pos = len(nyt_sentiment_pos)
    print(nyt_sentiment_pos)
    nyt_sentiment_neg = len(nyt_sentiment_neg)
    print(nyt_sentiment_neg)


    bbc_sentiment_pos = Headline.objects.filter(newspaper=2).filter(headline__contains=key1).filter(sentiment__gt=0)
    bbc_sentiment_neg = Headline.objects.filter(newspaper=2).filter(headline__contains=key1).filter(sentiment__lt=0)
    bbc_sentiment_pos = len(bbc_sentiment_pos)
    print(bbc_sentiment_pos)
    bbc_sentiment_neg = len(bbc_sentiment_neg)
    print(bbc_sentiment_neg)

    fn_sentiment_pos = Headline.objects.filter(newspaper=3).filter(headline__contains=key1).filter(sentiment__gt=0)
    fn_sentiment_neg = Headline.objects.filter(newspaper=3).filter(headline__contains=key1).filter(sentiment__lt=0)
    fn_sentiment_pos = len(fn_sentiment_pos)
    print(fn_sentiment_pos)
    fn_sentiment_neg = len(fn_sentiment_neg)
    print(fn_sentiment_neg)


    nyt_pie_labels = ['Positive Sentiment', 'Negative Sentiment']
    nyt_pie_values = []
    nyt_pie_values.append(nyt_sentiment_pos)
    nyt_pie_values.append(nyt_sentiment_neg)

    nytp_fig = go.Figure(data=[go.Pie(labels=nyt_pie_labels, values=nyt_pie_values), ])

    nytp_fig.update_layout(
       font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', title="New York Times", margin=dict(pad=50),showlegend=False )

    nytp_fig.update_traces(marker=dict(colors=['green', 'red']))

    nytp_fig.update_layout(
    title={
        'text': "The New York Times",
        'y':0.78,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})


    html_div_nytp = str(plotly.offline.plot(nytp_fig, output_type='div',config = {'displayModeBar': False},))



    bbc_pie_labels = ['Positive Sentiment', 'Negative Sentiment']
    bbc_pie_values = []
    bbc_pie_values.append(bbc_sentiment_pos)
    bbc_pie_values.append(bbc_sentiment_neg)

    bbcp_fig = go.Figure(data=[go.Pie(labels=bbc_pie_labels, values=bbc_pie_values), ])

    bbcp_fig.update_layout(
       font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', title="BBC News", margin=dict(pad=50), showlegend=False )

    bbcp_fig.update_traces(marker=dict(colors=['green', 'red']))

    bbcp_fig.update_layout(
    title={
        'text': "BBC News",
        'y':0.78,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})


    html_div_bbcp = str(plotly.offline.plot(bbcp_fig, output_type='div', config = {'displayModeBar': False}))


    fn_pie_labels = ['Positive Sentiment', 'Negative Sentiment']
    fn_pie_values = []
    fn_pie_values.append(fn_sentiment_pos)
    fn_pie_values.append(fn_sentiment_neg)

    fnp_fig = go.Figure(data=[go.Pie(labels=fn_pie_labels, values=fn_pie_values), ])

    fnp_fig.update_layout(
       font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', title="Fox News", margin=dict(pad=50), showlegend=False)

    fnp_fig.update_traces(marker=dict(colors=['green', 'red']))

    fnp_fig.update_layout(
    title={
        'text': "Fox News",
        'y':0.78,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},)


    html_div_fnp = str(plotly.offline.plot(fnp_fig, output_type='div', config = {'displayModeBar': False}))

    """priority calc"""
    
    nyt_priority = Headline.objects.filter(headline__contains=key1).filter(newspaper=1)
    nyt_priority_list = []

    for i in nyt_priority:
        nyt_priority_list.append(i.day_order)
    
    nyt_sum_priority = 0
    for i in nyt_priority_list:
        nyt_sum_priority += i
    
    if len(nyt_priority_list) > 0:
        nyt_average_priority = round(nyt_sum_priority/len(nyt_priority_list))
    else:
        nyt_average_priority = "NA"
    

    bbc_priority = Headline.objects.filter(headline__contains=key1).filter(newspaper=2)
    bbc_priority_list = []

    for i in bbc_priority:
        bbc_priority_list.append(i.day_order)
    
    bbc_sum_priority = 0
    for i in bbc_priority_list:
        bbc_sum_priority += i
    
    if len(bbc_priority_list) > 0:
        bbc_average_priority = round(bbc_sum_priority/len(bbc_priority_list))
    else:
        bbc_average_priority = "NA"


    fn_priority = Headline.objects.filter(headline__contains=key1).filter(newspaper=3)
    fn_priority_list = []

    for i in fn_priority:
        fn_priority_list.append(i.day_order)
    
    fn_sum_priority = 0
    for i in fn_priority_list:
        fn_sum_priority += i
    
    if len(fn_priority_list) > 0:
        fn_average_priority = round(fn_sum_priority/len(fn_priority_list))
    else:
        fn_average_priority = "NA"

    all_priority_time = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncMonth('date')).values('Date','newspaper').annotate(Average=Avg('day_order')).order_by("Date","newspaper")

    for i in all_priority_time:
        print(i)
    
    dfar = pd.DataFrame(list(all_priority_time))
    dfar['Average'] = round(dfar['Average'])
    dfar['newspaper'] = dfar['newspaper'].replace(1, 'The New York Times')
    dfar['newspaper'] = dfar['newspaper'].replace(2, 'BBC News')
    dfar['newspaper'] = dfar['newspaper'].replace(3, 'Fox News')
    dfar.rename(columns={'newspaper':'Newspaper'}, inplace= True)


    figar = px.line(dfar, x="Date", y="Average", color='Newspaper', color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }, title="Average Rank by Newspaper by Month" )

    figar.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',xaxis_title='', margin=dict(pad=50),)
    figar.update_yaxes(autorange="reversed")

    html_divar = str(plotly.offline.plot(figar, output_type='div', config = {'displayModeBar': False}))



    return render(request, 'custom_scraper/word_count.html',{'html_div':html_div,'html_div2':html_div2,'html_div_average_key1_sentiment':html_div_average_key1_sentiment, "nytkey1img":nytkey1img,"keystring":keystring, "key1":key1, "form":form, 'img_html':img_html, 'dataflex_padding': dataflex_padding, "centered_font": centered_font, "picflex_padding": picflex_padding, "centered_hover_color": centered_hover_color, "len_of_compare":len_of_compare,"all_hl_list": all_hl_list, "list_of_hl":list_of_hl, "html_div_news_bar":html_div_news_bar, "html_div_sentiment":html_div_sentiment, "html_divas":html_divas, "html_div_nytp":html_div_nytp, "html_div_bbcp":html_div_bbcp, "html_div_fnp": html_div_fnp, "nyt_average_priority":nyt_average_priority, "bbc_average_priority": bbc_average_priority, "fn_average_priority": fn_average_priority, "html_divar":html_divar})   



   
def research(request):
    
    form = WordCountSearch()
    
    search = request.session['search']
    return render(request, 'custom_scraper/research.html',{'form':form, 'search':search},)

def Sentiment_Main(request):

    from django.db.models.functions import TruncDay
    from django.db.models import Avg

   
    
    import pandas as pd



    import plotly.express as px
  

    import plotly
    
    average_sentiment_by_date_by_newspaper = Headline.objects.annotate(Date=TruncDay('date')).values('Date','newspaper').annotate(Average=Avg('sentiment')).order_by("-Date","newspaper")

    df4 = pd.DataFrame(list(average_sentiment_by_date_by_newspaper))
    df4['Average'] = df4['Average'] * 100
    df4['newspaper'] = df4['newspaper'].replace(1, 'The New York Times')
    df4['newspaper'] = df4['newspaper'].replace(2, 'BBC News')
    df4['newspaper'] = df4['newspaper'].replace(3, 'Fox News')


    fig4 = px.line(df4, x="Date", y="Average", color='newspaper')

    fig4.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(t=10,pad=10))

    html_div4 = str(plotly.offline.plot(fig4, output_type='div'))

    form1 = SentimentWordSearch()
    form2 = SentimentDateSearch()

    from django.db.models.functions import TruncDay
    from django.db.models import Avg

    

    """
    key3data = Headline.objects.filter(headline__contains=key3).annotate(Date=TruncDay('date')).values('Date').annotate(Count=Count('id')).order_by("-Date")
    for i in key3data:
        print(i)
    
    import pandas as pd
    df = pd.DataFrame(list(key3data))

    import plotly.express as px
    fig = px.line(df, x="Date", y="Count", title='"' + str(key3.capitalize()) + '":' + " Total Count")
    print(fig.data[0].name)

    import plotly

    html_div = str(plotly.offline.plot(fig, output_type='div'))
    """

    
    import plotly.express as px
    import plotly
    from django.db.models import Count
    form = WordCountSearch()
    
    import pandas as pd 
    import datetime

    import nltk
    from nltk.corpus import stopwords
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list


    allheadlines = Headline.objects.all()
    

    allkeywords = find_keywords(allheadlines)
    
    print(allkeywords)

    top_100 = allkeywords[:100]
    """Most negative nytimes word"""
    
    wordsentiment_by_newspaper = []
    for i in top_100:
        word = i[1]
        average_key_sentiment = Headline.objects.filter(headline__contains=word).values('newspaper').annotate(Average=Avg('sentiment')).order_by("newspaper")
        wordsentiment_by_newspaper.append(list(average_key_sentiment))
    
    y = 0 
    for i in wordsentiment_by_newspaper:
        i.append(top_100[y][1])
        number = y + 1
        i.append(number)

        y += 1

    
    
   
    
    
    
    print(wordsentiment_by_newspaper) 
    
    
    """
   

    for i in wordsentiment_by_newspaper:
        if i[0]['newspaper'] == 1 and i[1]['newspaper'] == 2 and i[2]['newspaper'] == 3:
            print("OK")
        else:
            print("problem")       
            
    for i in wordsentiment_by_newspaper:
        if len(i) < 5:
            if i[0]['newspaper'] == 3:
                i[:0] = {'newspaper': 2, 'Average': 0}
    
    for i in wordsentiment_by_newspaper:
        if len(i) < 5:
            if i[0]['newspaper'] == 2:
                i[:0] = {'newspaper': 1, 'Average': 0}
    
    for i in wordsentiment_by_newspaper:
        if len(i) == 3 and i[0]['newspaper'] == 1:
            i.append({'newspaper': 2, 'Average': 0})
            
        elif len(i) == 3 and i[0]['newspaper'] == 2:
            i[:0] = {'newspaper': 1, 'Average': 0}
            
    
    
    
    for i in wordsentiment_by_newspaper:
        if len(i) < 5:
            if i[1]['newspaper'] != 2:
                i[:1] = {'newspaper': 2, 'Average': 0}
    for i in wordsentiment_by_newspaper:
        if len(i) < 5:
            if i[2]['newspaper'] != 3:
                i.append({'newspaper': 3, 'Average': 0})
    for i in wordsentiment_by_newspaper:
        if len(i) == 4 and i[0]['newspaper'] == 1 and i[1]['newspaper'] == 3:
            i[:1] = {'newspaper': 2, 'Average': 0}

    
    for i in wordsentiment_by_newspaper:
        if i[0]['newspaper'] == 1 and i[1]['newspaper'] == 2 and i[2]['newspaper'] == 3:
            print(i)
            print("OK")
        else:
            print(i)
            print("problem")  

    """


    """ the following ensures all words searched have a newspaper 1, 2 and 3 value so that the info can be used to create a graph"""
    key_default = "newspaper"
    nyt_value = 1
    y = 1 
    for i in wordsentiment_by_newspaper:
        if key_default in i[0] and i[0]['newspaper'] == 1:
            print("True")
            print(y)
            print(i)
            print(i[0])
            print(type(i[0]))
            y += 1
        else:
            print("False")
            print(y)
            print(i)
            print(y)
            i.insert(0,{'newspaper': 1, 'Average': 0})
            
            print(i)
            y += 1
    
    for i in wordsentiment_by_newspaper:
        if key_default in i[1] and i[1]['newspaper'] == 2:
            print("True")
            print(y)
            print(i)
            print(i[1])
            print(type(i[1]))
            y += 1
        else:
            print("False")
            print(y)
            print(i)
            print(y)
            i.insert(1,{'newspaper': 2, 'Average': 0})
            
            print(i)
            y += 1            


    for i in wordsentiment_by_newspaper:
        if key_default in i[2] and i[2]['newspaper'] == 3:
            print("True")
            print(y)
            print(i)
            print(i[2])
            print(type(i[2]))
            y += 1
        else:
            print("False")
            print(y)
            print(i)
            print(y)
            i.insert(2,{'newspaper': 3, 'Average': 0})
            
            print(i)
            y += 1      

    for i in wordsentiment_by_newspaper:
        if len(i) == 5:
            print("True")
        else:
            print("False")


   
    print(wordsentiment_by_newspaper)

    nyt_top_100_by_sentiment = []
    for i in wordsentiment_by_newspaper:
        interlist = []
        interlist.append(i[0])
        interlist.append(i[3])
        nyt_top_100_by_sentiment.append(interlist)
    


    print(nyt_top_100_by_sentiment)

    sorted_nyt = sorted(nyt_top_100_by_sentiment, key = lambda i: i[0]['Average'] )
    
    worst3_nyt = sorted_nyt[:3]
    best3_nyt = sorted_nyt[(len(sorted_nyt)-3):]

    print(sorted_nyt)
    print(worst3_nyt)
    print(best3_nyt)


    bbc_top_100_by_sentiment = []
    for i in wordsentiment_by_newspaper:
        interlist = []
        interlist.append(i[1])
        interlist.append(i[3])
        bbc_top_100_by_sentiment.append(interlist)
    
    sorted_bbc = sorted(bbc_top_100_by_sentiment, key = lambda i: i[0]['Average'] )

    worst3_bbc = sorted_bbc[:3]
    best3_bbc = sorted_bbc[(len(sorted_bbc)-3):]

    fn_top_100_by_sentiment = []
    for i in wordsentiment_by_newspaper:
        interlist = []
        interlist.append(i[2])
        interlist.append(i[3])
        fn_top_100_by_sentiment.append(interlist)
    
    sorted_fn = sorted(fn_top_100_by_sentiment, key = lambda i: i[0]['Average'] )

    worst3_fn = sorted_fn[:3]
    best3_fn = sorted_fn[(len(sorted_fn)-3):]

    print(worst3_nyt)
    print(best3_nyt)
    print(worst3_bbc)
    print(best3_bbc)
    print(worst3_fn)
    print(best3_fn)
    
    nyttop1 = best3_nyt[0][1]
    nyttop2 = best3_nyt[1][1]
    nyttop3 = best3_nyt[2][1]

    nyttopdict = {}
    nyttopdict[nyttop1] = best3_nyt[0][0]['Average']
    nyttopdict[nyttop2] = best3_nyt[1][0]['Average']
    nyttopdict[nyttop3] = best3_nyt[2][0]['Average']
    print(nyttopdict)
   
    from collections import OrderedDict
    nyttopdict = OrderedDict(nyttopdict)

    nyttopdict = list(nyttopdict.items())

    print(nyttopdict)
    print(nyttopdict[0][0])
    

    bbctop1 = best3_bbc[0][1]
    bbctop2 = best3_bbc[1][1]
    bbctop3 = best3_bbc[2][1]

    bbctopdict = {}
    bbctopdict[bbctop1] = best3_bbc[0][0]['Average']
    bbctopdict[bbctop2] = best3_bbc[1][0]['Average']
    bbctopdict[bbctop3] = best3_bbc[2][0]['Average']
    print(bbctopdict)
   
    from collections import OrderedDict
    bbctopdict = OrderedDict(bbctopdict)

    bbctopdict = list(bbctopdict.items())

    print(bbctopdict)
    print(bbctopdict[0][0])

    fntop1 = best3_fn[0][1]
    fntop2 = best3_fn[1][1]
    fntop3 = best3_fn[2][1]

    fntopdict = {}
    fntopdict[bbctop1] = best3_fn[0][0]['Average']
    fntopdict[bbctop2] = best3_fn[1][0]['Average']
    fntopdict[bbctop3] = best3_fn[2][0]['Average']
    print(fntopdict)
   
    from collections import OrderedDict
    fntopdict = OrderedDict(fntopdict)

    fntopdict = list(fntopdict.items())

    print(fntopdict)
    print(fntopdict[0][0])

    search = ''

    def session_get1():
        request.session['search'] = nyttop1
    
    def session_get2():
        request.session['search'] = nyttop2

    def session_get3():
        request.session['search'] = nyttop3

    def session_get4():
        request.session['search'] = bbctop1

    def session_get5():
        request.session['search'] = bbctop2

    def session_get6():
        request.session['search'] = bbctop3

    def session_get7():
        request.session['search'] = fntop1

    def session_get8():
        request.session['search'] = fntop2

    def session_get9():
        request.session['search'] = fntop3

    average_sentiment_by_date_nyt_may = Headline.objects.filter(newspaper=1).filter(date__month=5).annotate(Date=TruncDay('date')).values('Date','newspaper').annotate(Average=Avg('sentiment')).order_by("Date","newspaper")

    for i in average_sentiment_by_date_nyt_may:
        print(i)
    
    

    



            
    


    return render(request, 'custom_scraper/Sentiment_Main.html', {'html_div4':html_div4, 'form1':form1, 'form2': form2, 'nyttop1':nyttop1, 'nyttop2':nyttop2, 'nyttop3':nyttop3, 'bbctop1':bbctop1, 'bbctop2':bbctop2, 'bbctop3':bbctop3, 'fntop1':fntop1, 'fntop2':fntop2, 'fntop3':fntop3, 'session_get1':session_get1, 'session_get1':session_get1, 'session_get2':session_get2, 'session_get3':session_get3, 'session_get4':session_get4, 'session_get5':session_get5, 'session_get6':session_get6, 'session_get7':session_get7, 'session_get8':session_get8, 'session_get9':session_get9, 'search':search})

def sentiment_word(request):

    
    

    return render(request, 'custom_scraper/sentiment_word.html', )

def sentiment_date(request):



    return render(request, 'custom_scraper/sentiment_date.html',)



def word_count_session(request):
    search = request.session['search']
    print(search)
    from django.db.models.functions import TruncDay
    from django.db.models import Count
    
    key1data = Headline.objects.filter(headline__contains=search).annotate(Date=TruncDay('date')).values('Date').annotate(Count=Count('id')).order_by("-Date")
    for i in key1data:
        print(i)
    
    from django.shortcuts import redirect
    if not key1data:
        
        request.session['search'] = search
        return redirect('research')

    import pandas as pd 
    import datetime
    form = WordCountSearch()
    import nltk
    from nltk.corpus import stopwords
    from django.db.models import Avg
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list
        
    today1 = today
    nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
    if not nytheadlines:
        nytheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1).filter(day_order__lte=25)

    bbcheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=2).filter(day_order__lte=25)
    if not bbcheadlines:
        bbcheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2).filter(day_order__lte=25)

    fnheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=3).filter(day_order__lte=25)
    if not fnheadlines:
        fnheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3).filter(day_order__lte=25)
    
    allkeywords = nytheadlines | bbcheadlines | fnheadlines
    allkeywords = find_keywords(allkeywords)

    nykeywords = find_keywords(nytheadlines)
    bbckeywords = find_keywords(bbcheadlines)
    fnkeywords = find_keywords(fnheadlines)


    all_wf_keys = []
    all_wf_values = []    
    keyword_counter = 0
    for v in allkeywords:
        if keyword_counter < 5:
            all_wf_values.append(v[0])
            all_wf_keys.append(v[1])
        keyword_counter += 1
    
    key1 = search
    freq1 = all_wf_values[0]
    

    from django.db.models.functions import TruncDay
    from django.db.models import Count
    
    key1data = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date').annotate(Count=Count('id')).order_by("-Date")
    for i in key1data:
        print(i)
    
    import pandas as pd
    df = pd.DataFrame(list(key1data))

    import plotly.express as px
    fig = px.line(df, x="Date", y="Count", title='"' + str(key1.capitalize()) + '":' + " Total Count")
    fig.update_layout(
        font=dict(family="Roboto", size=15,color="black"), plot_bgcolor='white', xaxis_title='', margin=dict(pad=50)
    )

    
    import plotly
    

    html_div = str(plotly.offline.plot(fig, output_type='div'))

    key1data_by_paper = Headline.objects.filter(headline__contains=key1).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Count=Count('id')).order_by("-Date")

    df2 = pd.DataFrame(list(key1data_by_paper))
    df2['newspaper'] = df2['newspaper'].replace(1, 'The New York Times')
    df2['newspaper'] = df2['newspaper'].replace(2, 'BBC News')
    df2['newspaper'] = df2['newspaper'].replace(3, 'Fox News')
    df2.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    print(df2)

    fig2 = px.line(df2, x="Date", y="Count", color='Newspaper', title='"' + str(key1.capitalize()) + '":' + " Count by Newspaper" )
    fig2.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(pad=50)
    )

    html_div2 = str(plotly.offline.plot(fig2, output_type='div'))

    average_key1_sentiment = Headline.objects.filter(headline__contains=key1).values('newspaper').annotate(Average=Avg('sentiment')).order_by("newspaper")
    df_average_key1_sentiment = pd.DataFrame(list(average_key1_sentiment))
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(1, 'The New York Times')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(2, 'BBC News')
    df_average_key1_sentiment['newspaper'] = df_average_key1_sentiment['newspaper'].replace(3, 'Fox News')
    df_average_key1_sentiment.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    df_average_key1_sentiment.rename(columns={'Average':'Sentiment Score'}, inplace= True)
    df_average_key1_sentiment['Sentiment Score'] = df_average_key1_sentiment['Sentiment Score'] * 100
    fig_average_key1_sentiment = px.bar(df_average_key1_sentiment, x='Newspaper', y='Sentiment Score', title='"'+str(key1.capitalize()) + '": ' + 'Average Sentiment by Newspaper')
    fig_average_key1_sentiment.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', margin=dict(pad=50)
    )

    html_div_average_key1_sentiment = str(plotly.offline.plot(fig_average_key1_sentiment, output_type='div'))

    print(key1)
    
    """
    dfkey1data = pd.DataFrame(list(Headline.objects.filter(headline__contains=key1).values('headline', 'date')))

    import plotly.express as px

    fig = px.line(dfkey1data, x="date") 
    
    for i in key1data:
        print(i)
    """
    nytkey1img = Photos.objects.filter(keyword=key1).first()
    print(nytkey1img)
    img_html = "<img src=" + str(nytkey1img) + ">"
    dataflex_padding = "padding-top: 230px;"
    centered_font = "font-size:80px;"
   
    picflex_padding = "padding-top:150px;"
    centered_hover_color = "white"
    
    if not nytkey1img:
        img_html = ""
        dataflex_padding = "padding-top: 80px;"
        centered_font = "font-size:120px;"
        centered_hover_color = "black"
        picflex_padding = "padding-top: 30px;"
        
    print(nytkey1img)
    keystring = str(key1)
    print("This request went to word_count")
    
    
    return render(request, 'custom_scraper/word_count_session.html',{'html_div':html_div,'html_div2':html_div2,'html_div_average_key1_sentiment':html_div_average_key1_sentiment, "nytkey1img":nytkey1img,"keystring":keystring, "key1":key1, "form":form, 'img_html':img_html, 'dataflex_padding': dataflex_padding, "centered_font": centered_font, "picflex_padding": picflex_padding, "centered_hover_color": centered_hover_color})   

def date_search(request):
    import datetime
    search = request.GET.get('date')
    today = search
    print(today)
    today_year = today[6:10]
    today_date = today[3:5]
    today_month = today[:2]
    today = today_year + "-" + today_month + "-" + today_date
    header_date = datetime.datetime.strptime(today, '%Y-%m-%d').date()
    print(today_date)
    print(today_year)
    print(today_month)
    print(today)
    scraped = True
    nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
    if not nytheadlines:
        scraped = False
        nytheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1).filter(day_order__lte=25)

    bbcheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=2).filter(day_order__lte=25)
    if not bbcheadlines:
        bbcheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2).filter(day_order__lte=25)

    fnheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=3).filter(day_order__lte=25)
    if not fnheadlines:
        fnheadlines = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3).filter(day_order__lte=25)
    
    nyt_sentiment_score = Headline.objects.filter(date__contains=today).filter(newspaper=1)
    if not nyt_sentiment_score:
        nyt_sentiment_score = Headline.objects.filter(date__contains=yesterday).filter(newspaper=1)
    
    bbc_sentiment_score = Headline.objects.filter(date__contains=today).filter(newspaper=2)
    if not bbc_sentiment_score:
        bbc_sentiment_score = Headline.objects.filter(date__contains=yesterday).filter(newspaper=2)
    
    fn_sentiment_score = Headline.objects.filter(date__contains=today).filter(newspaper=3)
    if not fn_sentiment_score:
        fn_sentiment_score = Headline.objects.filter(date__contains=yesterday).filter(newspaper=3)
        today1=yesterday


    ny_score = 0
    for i in nyt_sentiment_score:
        ny_score += i.sentiment
    ny_score = ny_score/len(nyt_sentiment_score)
    ny_score = round(ny_score*100,1)
    
    bbc_score = 0
    for i in bbc_sentiment_score:
        bbc_score += i.sentiment
    bbc_score = bbc_score/len(bbc_sentiment_score)
    bbc_score = round(bbc_score*100,1)

    fn_score = 0
    for i in fn_sentiment_score:
        fn_score += i.sentiment
    fn_score = fn_score/len(fn_sentiment_score)
    fn_score = round(fn_score*100,1)  

    overall_score = round((ny_score + bbc_score + fn_score)/3,1)
    
    import nltk
    from nltk.corpus import stopwords
    
    def find_keywords(headlines):
        stopwords = nltk.corpus.stopwords.words('english')
        
        
        
        headlineslist = []
        for i in headlines:
            headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
        for i in headlineslist:
            if i.lower() not in stopwords:
                
                without_stopwords.append(i)
        
        without_stopwords_string = " ".join(without_stopwords)
        
        texta = TextBlob(without_stopwords_string)
        
        a = texta.word_counts
        
        nytimes_word_count_list = []
        for key, value in sorted(a.items(), reverse=True, key=lambda item: item[1]):
            interlist = []
            if key != "s" and key != "’" and key != "‘":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list
        
    
    
    allkeywords = nytheadlines | bbcheadlines | fnheadlines
    allkeywords = find_keywords(allkeywords)

    nykeywords = find_keywords(nytheadlines)
    bbckeywords = find_keywords(bbcheadlines)
    fnkeywords = find_keywords(fnheadlines)


    all_wf_keys = []
    all_wf_values = []    
    keyword_counter = 0
    for v in allkeywords:
        if keyword_counter < 5:
            all_wf_values.append(v[0])
            all_wf_keys.append(v[1])
        keyword_counter += 1
    
    key1 = all_wf_keys[0]
    freq1 = all_wf_values[0]
    key2 = all_wf_keys[1]
    freq2 = all_wf_values[1]
    key3 = all_wf_keys[2]
    freq3 = all_wf_values[2]


    stopwords = nltk.corpus.stopwords.words('english')
        
        
        
    headlineslist = []
    for i in (nytheadlines | bbcheadlines | fnheadlines):
        headlineslist.append(i.headline)
        headlineslist = " ".join(headlineslist)
        headlineslist = headlineslist.split()
        without_stopwords = []
        
    for i in headlineslist:
        if i.lower() not in stopwords:
            without_stopwords.append(i)
        
    without_stopwords_string = " ".join(without_stopwords)
        
    texta = TextBlob(without_stopwords_string)

    import nltk, collections
    from nltk.util import ngrams
    ##bigrams today
    texta = str(texta).lower()
    tokenized = texta.split()
    hlBigrams = ngrams(tokenized, 2)
    hlBigramFreq = collections.Counter(hlBigrams)
    
    mostpopular = []
    for i in hlBigramFreq.most_common(3):
        mostpopular.append(i)
    
    phrase1 = str(mostpopular[0][0][0]) + " " + str(mostpopular[0][0][1])
    phrase1freq = str(mostpopular[0][1])
    

    phrase2 = str(mostpopular[1][0][0]) + " " + str(mostpopular[1][0][1])
    phrase2freq = str(mostpopular[1][1])

    phrase3 = str(mostpopular[2][0][0]) + " " + str(mostpopular[2][0][1])
    phrase3freq = str(mostpopular[2][1])  

    headlines_for_country = []
    for i in (nytheadlines | bbcheadlines | fnheadlines):
        headlines_for_country.append(i.headline)
        headlines_for_country_string = " ".join(headlineslist)
    
    from geotext import GeoText

    places = GeoText(headlines_for_country_string)
    cities_mentioned_today = places.cities
    countries_mentioned_today = places.country_mentions
    print(cities_mentioned_today)
    print(countries_mentioned_today)

    cities_mentioned = list((x,cities_mentioned_today.count(x))for x in set(cities_mentioned_today))
    cities_sorted = sorted(cities_mentioned, key=lambda x: x[1],reverse=True)
    
    city1 = cities_sorted[0][0]
    if len(cities_sorted) < 2:
        city2 = "None"
    else:
        city2 = cities_sorted[1][0]
    if len(cities_sorted) < 3:
        city3 ="None"
    else:
        city3 = cities_sorted[2][0]
    
        

    city1freq = cities_sorted[0][1]
    if len(cities_sorted) < 2:
        city2freq = 0
    else:
        city2freq = cities_sorted[1][1]
    if len(cities_sorted) < 3:
        city3freq = 0
    else:
        city3freq = cities_sorted[2][1]

    from iso3166 import countries

    top_countries = []
    for key, value in countries_mentioned_today.items():
        interlist = []
        interlist.append(key)
        interlist.append(value)
        top_countries.append(interlist)
    
    for i in top_countries:
        i[0] = countries.get(i[0]).name

    country1 = top_countries[0][0]
    country2 = top_countries[1][0]
    country3 = top_countries[2][0]

    country1freq = top_countries[0][1]
    country2freq = top_countries[1][1]
    country3freq = top_countries[2][1]

    print(top_countries)
    
    nyt_question_count = 0
    for i in nytheadlines:
        if "?" in str(i.headline):
            nyt_question_count += 1
    
    bbc_question_count = 0
    for i in bbcheadlines:
        if "?" in str(i.headline):
            bbc_question_count += 1
        
    fn_question_count = 0
    for i in fnheadlines:
        if "?" in str(i.headline):
            fn_question_count += 1

    
    nyt_exclamation_count = 0
    for i in nytheadlines:
        if "!" in str(i.headline):
            
            nyt_exclamation_count += 1
    
    bbc_exclamation_count = 0
    for i in bbcheadlines:
        if "!" in str(i.headline):
            bbc_exclamation_count += 1
        
    fn_exclamation_count = 0
    for i in fnheadlines:
        if "!" in str(i.headline):
            fn_exclamation_count += 1

    print(key1)
    key1_photo_link = Photos.objects.filter(keyword=key1).filter(date__contains=today).first()
    


    form = DateForm()
    
    
    print(scraped)
    



   




    


    return render(request, 'custom_scraper/date_search.html', {"search":search, "nytheadlines":nytheadlines,"bbcheadlines":bbcheadlines,"fnheadlines":fnheadlines,"ny_score":ny_score, "bbc_score":bbc_score, "fn_score":fn_score, "overall_score":overall_score,"allkeywords":allkeywords,"key1":key1,"key2":key2,"key3":key3,"freq1":freq1,"freq2":freq2,"freq3":freq3, "phrase1":phrase1, "phrase2":phrase2, "phrase3":phrase3, "phrase1freq":phrase1freq, "phrase2freq":phrase2freq, "phrase3freq":phrase3freq, "city1":city1, "city2":city2, "city3":city3, "city1freq": city1freq, "city2freq":city2freq, "city3freq":city3freq, "country1":country1, "country2":country2, "country3":country3, "country1freq":country1freq, "country2freq":country2freq, "country3freq":country3freq, "nyt_question_count":nyt_question_count,"bbc_question_count":bbc_question_count, "fn_question_count":fn_question_count,"nyt_exclamation_count":nyt_exclamation_count,"bbc_exclamation_count":bbc_exclamation_count,"fn_exclamation_count":fn_exclamation_count, "nytheadlines":nytheadlines, "bbcheadlines":bbcheadlines, "fnheadlines":fnheadlines, "key1_photo_link":key1_photo_link, "form":form,"header_date":header_date, "scraped":scraped})


def Sentiment(request):
    from django.db.models import Avg
    from django.db.models.functions import TruncDay
    import datetime

    average_sentiment_by_date_nyt_may = Headline.objects.filter(newspaper=1).filter(date__month=5).annotate(Date=TruncDay('date')).values('Date','newspaper').annotate(Average=Avg('sentiment')).order_by("Date","newspaper")
    for i in average_sentiment_by_date_nyt_may:
        print(i)
    
    may_list = []
    for i in average_sentiment_by_date_nyt_may:
        may_list.append(i['Date'])  
    
    may_check = [datetime.datetime(2020, 5, 1, 0, 0)]

    for i in may_list:
        may_check.append(i)
    
    add_to = []
    for i in may_check:
        if i not in may_list:
            interlist = [i]
            interlist.append("NA")
            add_to.append(interlist)
    
    final_may_list = []

    for i in average_sentiment_by_date_nyt_may:
        interlist = []
        interlist.append(i["Date"])
        interlist.append(round(i["Average"] * 100, 2))
        final_may_list.append(interlist)
    for i in add_to:
        final_may_list.append(i)
    

    print(final_may_list)
        
    for i in final_may_list:
        number_date = i[0].strftime("%d")
        print(number_date)
        i.append(int(number_date))
    
    final_may_list.sort(key = lambda x: x[2])

    print(final_may_list)


    average_sentiment_by_date_fn_may = Headline.objects.filter(newspaper=2).filter(date__month=5).annotate(Date=TruncDay('date')).values('Date','newspaper').annotate(Average=Avg('sentiment')).order_by("Date","newspaper")
    for i in average_sentiment_by_date_fn_may:
        print(i)
    
    may_list_fn = []
    for i in average_sentiment_by_date_fn_may:
        may_list_fn.append(i['Date'])  
    
    may_check_fn = [datetime.datetime(2020, 5, 1, 0, 0)]

    for i in may_list_fn:
        may_check_fn.append(i)
    
    add_to = []
    for i in may_check_fn:
        if i not in may_list_fn:
            interlist = [i]
            interlist.append("NA")
            add_to.append(interlist)
    
    final_may_list_fn = []

    for i in average_sentiment_by_date_fn_may:
        interlist = []
        interlist.append(i["Date"])
        interlist.append(round(i["Average"] * 100, 2))
        final_may_list_fn.append(interlist)
    for i in add_to:
        final_may_list_fn.append(i)
    

    print(final_may_list_fn)
        
    for i in final_may_list_fn:
        number_date = i[0].strftime("%d")
        print(number_date)
        i.append(int(number_date))
    
    final_may_list_fn.sort(key = lambda x: x[2])

    print(final_may_list)

    
    


    return render(request, 'custom_scraper/Sentiment.html', {"final_may_list":final_may_list, "final_may_list_fn": final_may_list_fn} )

def sentiment_landing(request):
    from django.db.models.functions import TruncDay
    from django.db.models import Avg
    import pandas as pd 
    import plotly.express as px
    import plotly

    average_sentiment_by_date_all = Headline.objects.annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date",)
    print(average_sentiment_by_date_all)

    combsent = pd.DataFrame(list(average_sentiment_by_date_all))
    combsent['Average'] = combsent['Average'] * 100
    combsent.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    print(combsent)

    figcomb = px.line(combsent, x="Date", y="Average", title="Combined Sentiment by Date", color_discrete_sequence=['black'] )
    figcomb.update_yaxes(showline=False, linewidth=2, linecolor='rgba(0,0,0,0)')

    figcomb.update_layout(
        font=dict(family="Roboto",size=10,color="black"), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title='', margin=dict(pad=50),)
    
    html_div_comb = str(plotly.offline.plot(figcomb, output_type='div', config = {'displayModeBar': False}))

    average_sentiment_by_date_compare = Headline.objects.annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by("Date",)
    

    comparesent = pd.DataFrame(list(average_sentiment_by_date_compare))
    comparesent['Average'] = comparesent['Average'] * 100
    comparesent['newspaper'] = comparesent['newspaper'].replace(1, 'The New York Times')
    comparesent['newspaper'] = comparesent['newspaper'].replace(2, 'BBC News')
    comparesent['newspaper'] = comparesent['newspaper'].replace(3, 'Fox News')
    comparesent.rename(columns={'newspaper':'Newspaper'}, inplace= True)


    figcompare = px.line(comparesent, x="Date", y="Average", color="Newspaper", title="Combined Sentiment by Date",color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )
   

    figcompare.update_layout(
        font=dict(family="Roboto",size=10,color="black"), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', margin=dict(pad=50),)
    
    
    html_div_compare = str(plotly.offline.plot(figcompare, output_type='div', config = {'displayModeBar': False}))

    form = WordCountSearch()


    


    return render(request, 'custom_scraper/sentiment_landing.html', {"html_div_comb":html_div_comb, "html_div_compare":html_div_compare, "form":form})


def overall_sentiment(request):

    from django.db.models.functions import TruncMonth
    from django.db.models.functions import TruncYear
    from django.db.models import Avg
    import pandas as pd 
    import plotly.express as px
    import plotly
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    from datetime import datetime
    from django.db.models.functions import TruncDay
    from calendar import monthrange
    from django.db.models import Count

    average_sentiment_by_month = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncMonth('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date")
    
    for i in average_sentiment_by_month:
        print(i)

    dfos = pd.DataFrame(list(average_sentiment_by_month))
    dfos['Average'] = dfos['Average'] * 100
   


    figos = px.line(dfos, x="Date", y="Average",  color_discrete_sequence=['black'] , title="Average Sentiment by Month" )

    figos.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',xaxis_title='', margin=dict(pad=50))

    html_divos = str(plotly.offline.plot(figos, output_type='div', config = {'displayModeBar': False}))

    average_sentiment_by_month_one = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncYear('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date")

    
    for i in average_sentiment_by_month_one:
        average_sent = i['Average']
    
    average_sent = average_sent * 100
    average_sent = round(average_sent, 2)
    

    average_sentiment_by_hr = Headline.objects.filter(day_order__lte=25).values('day_order').annotate(Average=Avg('sentiment'))
    for i in average_sentiment_by_hr:
        print(i)

    x_sent_hr = []
    y_sent_hr = []
    for i in average_sentiment_by_hr:
        x_sent_hr.append(i['day_order'])
        y_sent_hr.append(round(i['Average'] * 100,1))
    
    fig_sent_hr = px.bar(y=x_sent_hr, x=y_sent_hr, orientation='h', title="Headline Rank Sentiment")
    fig_sent_hr.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', yaxis=dict(autorange="reversed")
    )
    
    html_div_sent_hr = str(plotly.offline.plot(fig_sent_hr, output_type='div'))

    overall_pos = Headline.objects.filter(day_order__lte=25).filter(sentiment__gt=0).values('sentiment')

    overall_neg = Headline.objects.filter(day_order__lte=25).filter(sentiment__lt=0).values('sentiment')

    overall_zero = Headline.objects.filter(day_order__lte=25).filter(sentiment=0).values('sentiment')

    pie_labels = ['Positive', 'Negative', 'Neutral']

    pie_values = []

    pie_values.append(len(overall_pos))
    pie_values.append(len(overall_neg))
    pie_values.append(len(overall_zero))


    pie_fig = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values), ])

    pie_fig.update_layout(
       font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', margin=dict(pad=50),showlegend=False )

    pie_fig.update_traces(marker=dict(colors=['green','red', 'gray']))

    


    html_div_pie = str(plotly.offline.plot(pie_fig, output_type='div',config = {'displayModeBar': False},))


    all_sentiments = Headline.objects.filter(day_order__lte=25).values('sentiment')
 
    sent_hist = []
    for i in all_sentiments:
        if i['sentiment'] != 0:
            sent_hist.append(round(i['sentiment'] * 100))

    

    
    fig_sent_hist = px.histogram( x=sent_hist, nbins=30)
    
    """
    sent_hist = [sent_hist]
    fig_sent_hist = ff.create_distplot(sent_hist, 'Sentiment')
    """

    fig_sent_hist_div = str(plotly.offline.plot(fig_sent_hist, output_type='div',config = {'displayModeBar': False},))
    
    today = datetime.today()

    

  
    selected_month = today.month

    month_sent = Headline.objects.filter(day_order__lte=25).filter(date__month=selected_month).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
    for i in month_sent:
        print(i)
    
    dates = []
    sentiments = []

    current_month_days = monthrange(today.year, selected_month)

    print(current_month_days)

    current_month_check = [] 
    for i in range(1,current_month_days[1]+1):
        current_month_check.append(datetime(today.year, selected_month, i, 0, 0))
    
    print(current_month_check)
    for i in month_sent:
        dates.append(i['Date'])
       

    print(dates)

    for i in current_month_check:
        if i not in dates:
            dates.append(i)
    
    print(dates)

    final_list = []

    for i in month_sent:
        if i['Date'] in dates:
            interlist = []
            interlist.append(i['Date'])
            interlist.append(round(i['Average']*100,1))
            final_list.append(interlist)
    
    print(final_list)

    for i in range(len(final_list), len(dates)):
        interlist = []
        interlist.append(dates[i])
        interlist.append('')
        final_list.append(interlist)
    
    print(final_list)
    
    final_list.sort(key = lambda x: x[0])

    print(final_list)

    for i in final_list:
        number_date = i[0].strftime("%d")
        print(number_date)
        i.append(int(number_date))
    
    print(final_list)

    from datetime import date
    import calendar
    my_date = final_list[0][0]
    day_of_week = calendar.day_name[my_date.weekday()]
    print(day_of_week)
    
    if day_of_week == "Monday":
        final_list.insert(0,[' ',' ',' '])
    elif day_of_week == "Wednesday":
        final_list.insert(0,[' ',' ',' '])
        final_list.insert(0,[' ',' ',' '])
        final_list.insert(0,[' ',' ',' '])
    print(final_list)

    this_month = calendar.month_name[my_date.month]

    pos_by_month = Headline.objects.filter(day_order__lte=25).filter(sentiment__gt=0).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id'))

    neg_by_month = Headline.objects.filter(day_order__lte=25).filter(sentiment__lt=0).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id'))
    
    month_list = []

    for i in pos_by_month:
        month_list.append(i['Date'])
    
    pos_values = []

    for i in pos_by_month:
        pos_values.append(i['Count'])
    
    neg_values = []

    for i in neg_by_month:
        neg_values.append(i['Count'])
    
    fig_pn = go.Figure(data=[
    go.Bar(name='Positive Sentiment', x=month_list, y=pos_values),
    go.Bar(name='Negative Sentiment', x=month_list, y=neg_values)])

    fig_pn.update_layout( legend={'traceorder':'normal'}, )
    fig_pn.update_layout( font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )
    
    
    

    html_div_fig_pn = str(plotly.offline.plot(fig_pn, output_type='div', config = {'displayModeBar': False}))   



    month_sent_overall = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('-Average')

    
    
    month_sent_overall = month_sent_overall[:10]
    
   

    top10list = []

    for i in month_sent_overall:
        interlist = []
        interlist.append(i['Date'].date())
        interlist.append(round(i['Average']*100,1))
        interlist.append("{:02d}".format(i['Date'].month))
        interlist.append("{:02d}".format(i['Date'].day))
        interlist.append(i['Date'].year)
        top10list.append(interlist)
    
   

    month_sent_overall_neg = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('Average')

    
    
    month_sent_overall_neg = month_sent_overall_neg[:10]

    bottom10list = []

    for i in month_sent_overall_neg:
        interlist = []
        interlist.append(i['Date'].date())
        interlist.append(round(i['Average']*100,1))
        interlist.append("{:02d}".format(i['Date'].month))
        interlist.append("{:02d}".format(i['Date'].day))
        interlist.append(i['Date'].year)

        bottom10list.append(interlist)
    

    

    
    most_positive_hls = Headline.objects.filter(sentiment=1).values('date', 'newspaper', 'headline', 'sentiment',).order_by('date')

    

    

    most_negative_hls = Headline.objects.filter(sentiment=-1).values('date', 'newspaper', 'headline', 'sentiment').order_by('date')

    

    
    
    positive = []
    for i in most_positive_hls:
        interlist = []
        interlist.append(i['date'].date())
        if i['newspaper'] == 1:
            interlist.append("The New York Times")
        elif i['newspaper'] == 2:
            interlist.append("BBC News")
        elif i['newspaper'] == 3:
            interlist.append("Fox News")  
        interlist.append(i['headline'])
        interlist.append(round(i['sentiment'] * 100, 1))
        positive.append(interlist)
    
    negative = []
    for i in most_negative_hls:
        interlist = []
        interlist.append(i['date'].date())
        if i['newspaper'] == 1:
            interlist.append("The New York Times")
        elif i['newspaper'] == 2:
            interlist.append("BBC News")
        elif i['newspaper'] == 3:
            interlist.append("Fox News")
        interlist.append(i['headline'])
        interlist.append(round(i['sentiment'] * 100, 1))
        negative.append(interlist)

    

    average_sentiment_by_day = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date")
    
    

    dfosd = pd.DataFrame(list(average_sentiment_by_day))
    dfosd['Average'] = dfosd['Average'] * 100
   


    figosd = px.line(dfosd, x="Date", y="Average",  color_discrete_sequence=['black'] , title="Average Sentiment by Day" )

    figosd.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',xaxis_title='', margin=dict(pad=50))

    html_divosd = str(plotly.offline.plot(figosd, output_type='div', config = {'displayModeBar': False}))


    
    average_by_day_of_week = []
    for i in range(1,8):
        average_by_named_day = Headline.objects.filter(day_order__lte=25).filter(date__week_day=i).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
        summed = 0
        for i in average_by_named_day:
            summed += i['Average'] 
        averaged = summed/len(average_by_named_day)
        averaged = round(averaged *100,1)
        average_by_day_of_week.append(averaged)
    
    
    days_of_the_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']

    figdow = go.Figure([go.Bar(x=days_of_the_week,  y=average_by_day_of_week, marker_color=["black"])])

    figdow.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', title="Average Sentiment by Day of the Week",orientation=90, margin=dict(pad=50), )


    html_div_figdow = str(plotly.offline.plot(figdow, output_type='div', config = {'displayModeBar': False}))
    



    
   

    
    



    


    return render(request, 'custom_scraper/overall_sentiment.html', {'html_divos':html_divos, "average_sent":average_sent, "html_div_sent_hr": html_div_sent_hr, "html_div_pie": html_div_pie, "fig_sent_hist_div": fig_sent_hist_div, 'final_list': final_list, 'html_div_fig_pn': html_div_fig_pn, "top10list":top10list, "bottom10list":bottom10list, "positive":positive, "negative":negative, 'html_divosd':html_divosd, 'html_div_figdow': html_div_figdow})


def sentiment_overall_ajax(request):

    from django.db.models.functions import TruncMonth
    from django.db.models.functions import TruncYear
    from django.db.models import Avg
    import pandas as pd 
    import plotly.express as px
    import plotly
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    from datetime import datetime
    from django.db.models.functions import TruncDay
    from calendar import monthrange
    from django.db.models import Count

    average_sentiment_by_month = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncMonth('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date")
    
    for i in average_sentiment_by_month:
        print(i)

    dfos = pd.DataFrame(list(average_sentiment_by_month))
    dfos['Average'] = dfos['Average'] * 100
   


    figos = px.line(dfos, x="Date", y="Average",  color_discrete_sequence=['black'] , title="Average Sentiment by Month" )

    figos.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',xaxis_title='', margin=dict(pad=50))

    html_divos = str(plotly.offline.plot(figos, output_type='div', config = {'displayModeBar': False}))

    average_sentiment_by_month_one = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncYear('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date")

    
    for i in average_sentiment_by_month_one:
        average_sent = i['Average']
    
    average_sent = average_sent * 100
    average_sent = round(average_sent, 2)
    

    average_sentiment_by_hr = Headline.objects.filter(day_order__lte=25).values('day_order').annotate(Average=Avg('sentiment'))
    for i in average_sentiment_by_hr:
        print(i)

    x_sent_hr = []
    y_sent_hr = []
    for i in average_sentiment_by_hr:
        x_sent_hr.append(i['day_order'])
        y_sent_hr.append(round(i['Average'] * 100,1))
    
    fig_sent_hr = px.bar(y=x_sent_hr, x=y_sent_hr, orientation='h',color_discrete_sequence=['rgb(33,102,172)'])
    fig_sent_hr.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', yaxis=dict(autorange="reversed"), margin=dict(l=5, r=5, t=0, b=0, pad=0),showlegend=False, xaxis_title='', yaxis_title='',  
    )
    
    html_div_sent_hr = str(plotly.offline.plot(fig_sent_hr, output_type='div', config = {'displayModeBar': False}))

    overall_pos = Headline.objects.filter(day_order__lte=25).filter(sentiment__gt=0).values('sentiment')

    overall_neg = Headline.objects.filter(day_order__lte=25).filter(sentiment__lt=0).values('sentiment')

    overall_zero = Headline.objects.filter(day_order__lte=25).filter(sentiment=0).values('sentiment')

    pie_labels = ['Positive', 'Negative', 'Neutral']

    pie_values = []

    pie_values.append(len(overall_pos))
    pie_values.append(len(overall_neg))
    pie_values.append(len(overall_zero))


    pie_fig = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values), ])

    pie_fig.update_layout(
       font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', margin=dict(l=5, r=5, t=5, b=5, pad=10),showlegend=False )

    pie_fig.update_traces(marker=dict(colors=["rgb(33,102,172)",'rgb(178,24,43)', 'whitesmoke']))

    


    html_div_pie = str(plotly.offline.plot(pie_fig, output_type='div',config = {'displayModeBar': False},))


    all_sentiments = Headline.objects.filter(day_order__lte=25).values('sentiment')
 
    sent_hist = []
    for i in all_sentiments:
        if i['sentiment'] != 0:
            sent_hist.append(round(i['sentiment'] * 100))

    

    
    fig_sent_hist = px.histogram( x=sent_hist, nbins=30, color_discrete_sequence=['rgb(33,102,172)'])
    fig_sent_hist.update_layout(plot_bgcolor='white', margin=dict(l=5, r=5, t=5, b=5, pad=10),showlegend=False, yaxis=dict(dtick=200), xaxis_title='', yaxis_title='')
    
    """
    sent_hist = [sent_hist]
    fig_sent_hist = ff.create_distplot(sent_hist, 'Sentiment')
    """

    fig_sent_hist_div = str(plotly.offline.plot(fig_sent_hist, output_type='div',config = {'displayModeBar': False},))
    
    today = datetime.today()

    

  
    selected_month = today.month

    month_sent = Headline.objects.filter(day_order__lte=25).filter(date__month=selected_month).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
    for i in month_sent:
        print(i)
    
    dates = []
    sentiments = []

    current_month_days = monthrange(today.year, selected_month)

    print(current_month_days)

    current_month_check = [] 
    for i in range(1,current_month_days[1]+1):
        current_month_check.append(datetime(today.year, selected_month, i, 0, 0))
    
    print(current_month_check)
    for i in month_sent:
        dates.append(i['Date'])
       

    print(dates)

    for i in current_month_check:
        if i not in dates:
            dates.append(i)
    
    print(dates)

    final_list = []

    for i in month_sent:
        if i['Date'] in dates:
            interlist = []
            interlist.append(i['Date'])
            interlist.append(round(i['Average']*100,1))
            final_list.append(interlist)
    
    print(final_list)

    for i in range(len(final_list), len(dates)):
        interlist = []
        interlist.append(dates[i])
        interlist.append('')
        
        final_list.append(interlist)
    
    print(final_list)


    
    final_list.sort(key = lambda x: x[0])

    print(final_list)

    for i in final_list:
        number_date = i[0].strftime("%d")
        print(number_date)
        i.append(int(number_date))
    
    print(final_list)

    from datetime import date
    import calendar
    my_date = final_list[0][0]
    day_of_week = calendar.day_name[my_date.weekday()]
    this_month = calendar.month_name[my_date.month]

    for i in final_list:
        i.append("{:02d}".format(i[0].month))
        i.append("{:02d}".format(i[0].day))
        i.append(i[0].year)

    if day_of_week == "Monday":
        final_list.insert(0,[' ',' ',' ', '#', '', ''])
    elif day_of_week == "Wednesday":
        final_list.insert(0,[' ',' ',' ', '#', '',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])
    
    print(final_list)


    pos_by_month = Headline.objects.filter(day_order__lte=25).filter(sentiment__gt=0).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id'))

    neg_by_month = Headline.objects.filter(day_order__lte=25).filter(sentiment__lt=0).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id'))
    
    month_list = []

    for i in pos_by_month:
        month_list.append(i['Date'])
    
    pos_values = []

    for i in pos_by_month:
        pos_values.append(i['Count'])
    
    neg_values = []

    for i in neg_by_month:
        neg_values.append(i['Count'])
    
    print(neg_values)
    
    fig_pn = go.Figure(data=[
    go.Bar(name='Positive Sentiment', x=month_list, y=pos_values, marker_color="rgb(33,102,172)"),
    go.Bar(name='Negative Sentiment', x=month_list, y=neg_values, marker_color="rgb(178,24,43)"),])

    fig_pn.update_layout( legend={'traceorder':'normal'}, height=250)
    fig_pn.update_layout( font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, margin=dict(l=5, r=5, t=5, b=5, pad=10),xaxis_tickformat = '%b',
    yaxis=dict(dtick=300), )
    
    
    

    html_div_fig_pn = str(plotly.offline.plot(fig_pn, output_type='div', config = {'displayModeBar': False}))   



    month_sent_overall = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('-Average')

   
    
    month_sent_overall = month_sent_overall[:10]
    
  

    top10list = []

    for i in month_sent_overall:
        interlist = []
        interlist.append(i['Date'].date())
        interlist.append(round(i['Average']*100,1))
        interlist.append("{:02d}".format(i['Date'].month))
        interlist.append("{:02d}".format(i['Date'].day))
        interlist.append(i['Date'].year)
        top10list.append(interlist)
    
    
    month_sent_overall_neg = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('Average')

    
    
    month_sent_overall_neg = month_sent_overall_neg[:10]

    bottom10list = []

    for i in month_sent_overall_neg:
        interlist = []
        interlist.append(i['Date'].date())
        interlist.append(round(i['Average']*100,1))
        interlist.append("{:02d}".format(i['Date'].month))
        interlist.append("{:02d}".format(i['Date'].day))
        interlist.append(i['Date'].year)

        bottom10list.append(interlist)
    
    
  

    

   
    
    most_positive_hls = Headline.objects.filter(sentiment=1).values('date', 'newspaper', 'headline', 'sentiment','link').order_by('date')

    

  

    most_negative_hls = Headline.objects.filter(sentiment=-1).values('date', 'newspaper', 'headline', 'sentiment','link').order_by('date')

    

 
    
    positive = []
    for i in most_positive_hls:
        interlist = []
        interlist.append(i['date'].strftime("%m/%d/%y"))
        if i['newspaper'] == 1:
            interlist.append("NYT")
            interlist.append("https://www.nytimes.com/")
        elif i['newspaper'] == 2:
            interlist.append("BBC")
            interlist.append("https://www.bbc.com/news")
        elif i['newspaper'] == 3:
            interlist.append("FN")
            interlist.append("https://www.foxnews.com/")  
        interlist.append(i['headline'])
        interlist.append(round(i['sentiment'] * 100, 1))
        interlist.append(i['link'])
        positive.append(interlist)
    
    
    negative = []
    for i in most_negative_hls:
        interlist = []
        interlist.append(i['date'].strftime("%m/%d/%y"))
        if i['newspaper'] == 1:
            interlist.append("NYT")
            interlist.append("https://www.nytimes.com/")
        elif i['newspaper'] == 2:
            interlist.append("BBC")
            interlist.append("https://www.bbc.com/news")
        elif i['newspaper'] == 3:
            interlist.append("FN")
            interlist.append("https://www.foxnews.com/")
        interlist.append(i['headline'])
        interlist.append(round(i['sentiment'] * 100, 1))
        interlist.append(i['link'])
        negative.append(interlist)

   

    average_sentiment_by_day = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Sentiment=Avg('sentiment')).order_by('Date')
    
    



    dfosd = pd.DataFrame(list(average_sentiment_by_day))
    dfosd['Sentiment'] = dfosd['Sentiment'] * 100
   


    figosd = px.line(dfosd, x="Date", y="Sentiment",color_discrete_sequence=['black'] )

    figosd.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',xaxis_title='', yaxis_title ='', margin=dict(l=5, r=5, t=5, b=5, pad=10))

    
    figosd.update_layout(
    
    xaxis_tickformat = '%B',
    yaxis=dict(dtick=2),
    
    )

    html_divosd = str(plotly.offline.plot(figosd, output_type='div', config = {'displayModeBar': False}))


    
    average_by_day_of_week = []
    for i in range(1,8):
        average_by_named_day = Headline.objects.filter(day_order__lte=25).filter(date__week_day=i).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
        summed = 0
        for i in average_by_named_day:
            summed += i['Average'] 
        averaged = summed/len(average_by_named_day)
        averaged = round(averaged *100,1)
        average_by_day_of_week.append(averaged)
    
    
    days_of_the_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']

    figdow = go.Figure([go.Bar(x=days_of_the_week,  y=average_by_day_of_week, marker_color="rgb(33,102,172)")])

    figdow.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',orientation=90, margin=dict(l=5, r=5, t=5, b=5, pad=10),showlegend=False)


    html_div_figdow = str(plotly.offline.plot(figdow, output_type='div', config = {'displayModeBar': False}))
    
    html_divos_jason = JsonResponse({'task':html_divos}, status=200)


    all_headlines = Headline.objects.filter(day_order__lte=25).values('headline')

   

    all_headline_string = ""

    for i in all_headlines: 
        all_headline_string += " " + i['headline']
    
    
    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(500)

    list_of_top_words = []

    for i in most_common: 
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)
    
    

    exceptions = [',',':',"'",'.','?', "'s", '‘', "n't", '’']

    top_words = []

    for i in list_of_top_words:
        if i[0] not in exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_words.append(interlist)
    
    

    total_exceptions = []

    for i in top_words:
        total_exceptions.append(i[0])
    


    overall_words = []
    for i in top_words: 
        overall_words.append(i)
    
    #top people who show up in the top 500 most common words

    for i in overall_words:
        sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__contains=i[0]).values('sentiment')
        total_for_average = 0
    
        for y in sent_average:
            total_for_average += y['sentiment']
    
        total_for_average = total_for_average * 100

        average_key = total_for_average/len(sent_average)

        average_key = round(average_key, 2)

        i.append(average_key)

    
    
    #final places lists
    worst_overall = sorted(overall_words, key = lambda x: x[2])
    top_overall = sorted(overall_words, key = lambda x: x[2], reverse=True)

    worst_overall = worst_overall[:20]
    top_overall = top_overall[:20]

    people_exceptions = ['better', 'mike', 'hospitals', 'andrew', 'event', 'orders', 'tech', 'past','coronavirus', 'us', 'new', 'virus', 'says', 'george',  'china', 'police', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.', 'president', 'amid', 'york', 'death', 'america', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'state', 'man', 'news', '$', 'black', 'outbreak', 'people', 'city', 'back', 'one', 'joe', 'health', 'may', 'first', 'democrats', 'americans', 'white', 'media', '2020', 'take', 'life', 'time', 'updates', 'protests', 'report', 'get', 'calls', 'fight', 'help', '-', 'dr.', 'states', 'global', 'dies', 'response', 'day', 'say', 'case', 'american', 'week', 'bill', ';', 'deaths', 'workers', 'face', 'like', 'dems', 'top', 'see', 'campaign', 'claims', 'economy', 'race', 'court', 'super', 'judge', 'big', 'bbc', 'dead', 'test', 'protesters', 'show', 'india', 'iowa', 'make', 'want', 'reopen', 'still', 'live', 'found', 'go', 'would', 'quarantine', 'masks', 'south', 'work', 'election', 'need', 'democratic', 'vote', 'rep.', 'gov', 'sen.', 'california', 'rally', 'trial', 'plan', 'reopening', 'best', 'toll', 'law', 'vaccine', 'deal', 'travel', 'italy', 'spread', 'impeachment', 'woman', 'women', 'killed', 'end', 'mayor', 'warns', 'last', 'years', 'behind', 'care', 'debate', 'country', 'protest', 'russia', 'know', 'video', 'family', 'attack', 'war', 'quiz', 'senate', 'officials', 'going', 'fears', 'star', 'two', 'inside', 'pictures', 'next', 'former', 'service', 'covid', 'follow', 'voters', 'business', 'children', "'we", 'murder', 'stop', 'chief', 'national', 'testing', 'set', 'hospital', 'ahead', 'primary', 'tells', 'party', 'justice', 'shooting', 'europe', 'briefing', 'much', '2', 'economic', '3', 'tv', 'days', 'korea', 'iran', 'dem', 'win', 'mass', 'free', 'bowl', 'call', 'history', 'million', 'social', 'aid', 'lives', 'order', 'hits', 'five', 'many', 'michael', 'faces', 'rise', 'weekend', 'times', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'hong', 'kong', 'florida', 'supreme', 'chinese', 'doctor', 'charged', 'force', 'governor', 'takes', 'change', 'record', 'exclusive', 'stimulus', 'public', 'facebook', 'listen', 'twitter', 'hit', 'open', 'story', 'official', 'good', 'despite', 'leader', 'mother', 'tuesday', 'year', 'never', 'gives', 'gop', 'john', 'military', 'way', 'arrested', 'spreads', 'online', 'radio', 'got', 'reveals', 'save', 'stay', 'slams', 'africa', 'job', 'wants', 'texas', 'away', 'oil', 'ny', 'relief', 'markets', 'return', 'must', 'making', 'gets', 'long', 'start', 'rules', 'even', 'fall', 'fire', 'makes', 'look', 'latest', 'ban', 'risk', 'doctors', 'surge', 'use', 'food', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'russian', '11', 'federal', 'restrictions', 'cut', 'headlines', 'team', 'key', 'missing', 'kobe', 'probe', 'guide', 'mask', "'the", 'amazon', 'another', 'presidential', 'system', 'think', 'blasts', 'political', 'minneapolis', 'wuhan', 'reports', 'wins', 'lost', 'students', 'mark', 'move', 'kids', 'countries', 'changed', 'close', 'pm', 'shot', 'cities', 'safe', 'medical', 'study', 'seattle', 'made', 'ever', 'ship', 'threat', 'analysis', 'young', 'find', 'france',  'across', 'racism', 'die', 'patients', 'around', 'spain', 'goes', 'everything', 'wrong', 'real', 'washington', 'matter', 'government', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'died', 'deadly', 'left', 'experts', 'come', 'market', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'second', 'mr.', 'chris', 'administration', 'cops', 'wall', 'really', 'might', 'hampshire', 'jobs', 'de', 'germany', 'night', 'memorial', 'stocks', 'cathedral', 'businesses', 'nation', 'small', 'months', 'son', 'near', 'major', 'tom', 'trying', 'problem', 'coming', 'let', 'sign', 'turn', 'give', 'elizabeth', '4', 'seen', 'action', 'plans', 'west', 'father', 'secret', 'candidate', 'sick', 'prison', 'carolina', 'doj', 'message', 'reads', 'patrick', 'secretary', 'union', '!', 'canada', 'tweet', 'caucuses', 'meghan', 'crash', 'taking', 'things', 'stars', 'couple', 'needs', 'congress', 'school', 'power', 'staff', 'hope', 'violence', 'access', 'unrest',  'clash', '“', '”', 'far', 'girl', 'leaves', 'questions', 'six', 'today', 'pay', 'support', 'book', 'leaders', 'fighting', "'re", 'money', '1', 'officer', 'claim', 'release', 'without', 'church', 'concerns']

    top_people = []
    for i in top_words:
        if i[0] not in people_exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_people.append(interlist)
    
    #top people who show up in the top 500 most common words

    for i in top_people:
        sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__contains=i[0]).values('sentiment')
        total_for_average = 0
    
        for y in sent_average:
            total_for_average += y['sentiment']
    
        total_for_average = total_for_average * 100

        average_key = total_for_average/len(sent_average)

        average_key = round(average_key, 2)

        i.append(average_key)

    
    
    #final people list
    worst_people = sorted(top_people, key = lambda x: x[2])
    best_people = sorted(top_people, key = lambda x: x[2], reverse=True)
    

    
    place_exceptions = ['better', 'mike', 'hospitals', 'andrew', 'event', 'orders', 'tech', 'past','coronavirus', 'trump', 'us', 'new', 'virus', 'says', 'biden', 'police', 'covid-19', 'pandemic', 'lockdown', 'world', 'president', 'amid', 'death', 'sanders', 'could', 'crisis', 'cases', 'home', 'house', 'state', 'man', 'news', '$', 'black', 'outbreak', 'people', 'city', 'back', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'democrats', 'white', 'floyd', 'media', '2020', 'take', 'life', 'time', 'updates', 'protests', 'report', 'get', 'calls', 'fight', 'help', '-', 'dr.', 'states', 'dies', 'response', 'day', 'say', 'george', 'case',  'week', 'bill', ';', 'deaths', 'workers', 'face', 'like', 'dems', 'top', 'bloomberg', 'see', 'campaign', 'claims', 'economy', 'race', 'court', 'super', 'judge', 'big', 'bbc', 'dead', 'test', 'protesters', 'show', 'make', 'want', 'reopen', 'still', 'live', 'obama', 'found', 'go', 'flynn', 'would', 'quarantine', 'masks', 'south', 'work', 'election', 'need', 'democratic', 'vote', 'rep.', 'gov', 'sen.', 'rally', 'trial', 'plan', 'reopening', 'best', 'toll', 'law', 'vaccine', 'deal', 'travel', 'spread', 'impeachment', 'woman', 'women', 'killed', 'end', 'mayor', 'warns', 'last', 'years', 'behind', 'care', 'debate', 'country', 'protest', 'know', 'video', 'family', 'attack', 'war', 'quiz', 'senate', 'officials', 'going', 'fears', 'star', 'two', 'inside', 'pictures', 'next', 'former', 'service', 'pelosi', 'covid', 'follow', 'voters', 'business', 'children', "'we", 'murder', 'stop', 'chief', 'national', 'testing', 'set', 'warren', 'hospital', 'ahead', 'primary', 'tells', 'party', 'justice', 'shooting', 'briefing', 'much', '2', 'economic', '3', 'tv', 'days', 'dem', 'win', 'mass', 'free', 'bowl', 'call', 'history', 'million', 'social', 'aid', 'lives', 'order', 'hits', 'five', 'many', 'michael', 'tucker', 'hannity', 'faces', 'cuomo', 'rise', 'weekend', 'times', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'kong', 'supreme', 'doctor', 'charged', 'force', 'governor', 'takes', 'change', 'record', 'exclusive', 'buttigieg', 'stimulus', 'public', 'facebook', 'bolton', 'listen', 'twitter', 'hit', 'open', 'story', 'official', 'good', 'despite', 'leader', 'mother', 'tuesday', 'year', 'never', 'gives', 'gop', 'john', 'military', 'way', 'arrested', 'spreads', 'online', 'radio', 'got', 'reveals', 'save', 'stay', 'slams', 'job', 'wants', 'away', 'oil', 'barr', 'relief', 'markets', 'return', 'must', 'making', 'gets', 'long', 'start', 'rules', 'even', 'fall', 'fire', 'bryant', 'makes', 'look', 'latest', 'ban', 'risk', 'doctors', 'surge', 'use', 'food', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', '11', 'federal', 'restrictions', 'cut', 'headlines', 'team', 'key', 'missing', 'kobe', 'probe', 'guide', 'mask', "'the", 'amazon', 'another', 'presidential', 'system', 'think', 'blasts', 'political', 'minneapolis', 'reports', 'wins', 'lost', 'students', 'mark', 'move', 'kids', 'countries', 'changed', 'close', 'pm', 'shot', 'cities', 'safe', 'medical', 'study', 'made', 'ever', 'ship', 'threat', 'analysis', 'young', 'find', 'france', 'weinstein', 'across', 'racism', 'die', 'patients', 'around',  'goes', 'everything', 'wrong', 'aoc', 'real', 'matter', 'government', 'reform', 'said', 'attacks', 'kill', 'tests', 'bad',  'died', 'deadly', 'left', 'experts', 'come', 'market', 'possible', 'point', 'johnson', 'mean', 'worst', 'results', 'drug', 'north', 'sex', 'positive', 'daily', 'shows', 'cruise', 'great', 'college', 'second', 'mr.', 'chris', 'administration', 'cops', 'wall', 'really', 'might',  'jobs', 'de', 'night', 'memorial', 'stocks', 'cathedral', 'businesses', 'nation', 'small', 'months', 'son', 'near', 'major', 'tom', 'trying', 'problem', 'coming', 'let', 'newt', 'blasio', 'sign', 'turn', 'give', 'elizabeth', '4', 'seen', 'action', 'plans', 'father', 'secret', 'candidate', 'sick', 'prison', 'doj', 'message', 'reads', 'patrick', 'secretary', 'union', '!', 'tweet', 'caucuses', 'meghan', 'crash', 'taking', 'things', 'stars', 'couple', 'needs', 'congress', 'school', 'power', 'staff', 'hope', 'violence', 'access', 'fauci', 'unrest', 'pompeo', 'clash', '“', '”', 'far', 'girl', 'leaves', 'questions', 'six', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'fighting', "'re", 'money', '1', 'officer', 'claim', 'release', 'without', 'siegel', 'church', 'concerns']

    top_places = []
    for i in top_words:
        if i[0] not in place_exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_places.append(interlist)
    
    #top people who show up in the top 500 most common words

    for i in top_places:
        sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__contains=i[0]).values('sentiment')
        total_for_average = 0
    
        for y in sent_average:
            total_for_average += y['sentiment']
    
        total_for_average = total_for_average * 100

        average_key = total_for_average/len(sent_average)

        average_key = round(average_key, 2)

        i.append(average_key)

    
    
    #final places lists
    worst_places = sorted(top_places, key = lambda x: x[2])
    top_places = sorted(top_places, key = lambda x: x[2], reverse=True)


    political_exceptions = ['better', 'mike','coronavirus', 'trump', 'us', 'new', 'virus', 'says', 'biden', 'china', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.',  'amid', 'york', 'death', 'america', 'sanders', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'state', 'man', 'news', '$', 'black', 'outbreak', 'people', 'city', 'back', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'americans', 'white', 'floyd', '2020', 'take', 'life', 'time', 'updates', 'report', 'get', 'calls', 'fight', 'help', '-', 'dr.', 'states', 'global', 'dies', 'response', 'day', 'say', 'george', 'case', 'american', 'week', 'bill', ';', 'deaths', 'face', 'like',  'top', 'bloomberg', 'see', 'claims', 'race', 'court', 'super', 'big', 'bbc', 'dead', 'test', 'show', 'india', 'iowa', 'make', 'want', 'reopen', 'still', 'live', 'obama', 'found', 'go', 'flynn', 'would', 'quarantine', 'masks', 'south', 'work', 'need', 'california', 'plan', 'reopening', 'best', 'toll', 'vaccine', 'deal', 'travel', 'italy', 'spread', 'woman', 'women', 'killed', 'end', 'warns', 'last', 'years', 'behind', 'care', 'country', 'protest', 'russia', 'know', 'video', 'family', 'attack', 'quiz',  'going', 'fears', 'star', 'two', 'inside', 'pictures', 'next', 'former', 'service', 'pelosi', 'covid', 'follow', 'business', 'children', "'we", 'murder', 'stop', 'chief', 'national', 'testing', 'set', 'warren', 'hospital', 'ahead', 'primary', 'tells', 'party', 'justice', 'shooting', 'europe', 'briefing', 'much', '2', '3', 'tv', 'days', 'korea', 'iran', 'win', 'mass', 'free', 'bowl', 'call', 'history', 'million', 'social', 'aid', 'lives', 'order', 'hits', 'five', 'many', 'michael', 'tucker', 'hannity', 'faces', 'cuomo', 'rise', 'weekend', 'times', 'watch', 'fox', 'fear', 'three', 'right', 'hong', 'kong', 'florida', 'supreme', 'chinese', 'doctor', 'charged', 'force', 'governor', 'takes', 'change', 'record', 'exclusive', 'buttigieg', 'stimulus', 'public', 'facebook', 'bolton', 'listen', 'twitter', 'hit', 'open', 'story', 'official', 'good', 'despite', 'leader', 'mother', 'tuesday', 'year', 'never', 'gives',  'john', 'military', 'way', 'arrested', 'spreads', 'online', 'radio', 'got', 'reveals', 'save', 'stay', 'slams', 'africa', 'job', 'wants', 'texas', 'away', 'oil', 'ny', 'barr', 'relief', 'markets', 'return', 'must', 'making', 'gets', 'long', 'start', 'rules', 'even', 'fall', 'fire', 'bryant', 'makes', 'look', 'latest', 'ban', 'risk', 'doctors', 'surge', 'use', 'food', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'russian', '11', 'federal', 'restrictions', 'cut', 'headlines', 'team', 'key', 'missing', 'kobe', 'probe', 'guide', 'mask', "'the", 'amazon', 'another', 'presidential', 'system', 'think', 'blasts', 'political', 'minneapolis', 'wuhan', 'reports', 'wins', 'lost', 'students', 'mark', 'move', 'kids', 'countries', 'changed', 'close', 'pm', 'shot', 'cities', 'safe', 'medical', 'study', 'seattle', 'made', 'ever', 'ship', 'threat', 'analysis', 'young', 'find', 'france', 'weinstein', 'across', 'racism', 'die', 'patients', 'around', 'spain', 'goes', 'everything', 'wrong', 'aoc', 'real', 'washington', 'matter', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'died', 'deadly', 'left', 'experts', 'come', 'market', 'possible', 'point', 'johnson', 'mean', 'worst', 'results', 'drug', 'north', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'second', 'mr.', 'chris', 'administration', 'cops', 'wall', 'really', 'might', 'hampshire', 'jobs', 'de', 'germany', 'night', 'memorial', 'stocks', 'cathedral', 'businesses', 'nation', 'small', 'months', 'son', 'near', 'major', 'tom', 'trying', 'problem', 'coming', 'let', 'newt', 'blasio', 'sign', 'turn', 'give', 'elizabeth', '4', 'seen', 'action', 'plans', 'west', 'father', 'secret', 'candidate', 'sick', 'prison', 'carolina', 'message', 'reads', 'patrick', 'secretary', 'union', '!', 'canada', 'tweet', 'caucuses', 'meghan', 'crash', 'taking', 'things', 'stars', 'couple', 'needs', 'school', 'power', 'staff', 'hope', 'violence', 'access', 'fauci', 'unrest', 'pompeo', 'clash', '“', '”', 'far', 'girl', 'leaves', 'questions', 'six', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'fighting', "'re", 'money', '1', 'officer', 'claim', 'release', 'without', 'siegel', 'church', 'concerns']
  
    top_political = []
    for i in top_words:
        if i[0] not in political_exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_political.append(interlist)
    
    #top people who show up in the top 500 most common words

    for i in top_political:
        sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__contains=i[0]).values('sentiment')
        total_for_average = 0
    
        for y in sent_average:
            total_for_average += y['sentiment']
    
        total_for_average = total_for_average * 100

        average_key = total_for_average/len(sent_average)

        average_key = round(average_key, 2)

        i.append(average_key)

    
    
    #final places lists
    worst_political = sorted(top_political, key = lambda x: x[2])
    top_political = sorted(top_political, key = lambda x: x[2], reverse=True)
   

    
    
    economic_exceptions = ['coronavirus', 'trump', 'us', 'new', 'virus', 'says', 'biden', 'china', 'police', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.', 'president', 'amid', 'death', 'york', 'america', 'sanders', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'man', 'state', 'black', 'news', 'outbreak', 'people', 'back', 'city', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'democrats', 'white', 'americans', 'floyd', '2020', 'media', 'take', 'life', 'updates', 'time', 'protests', 'report', 'get', 'calls', 'fight', 'help', 'day', 'dies', 'american', '-', 'dr.', 'say', 'global', 'states', 'response', 'case', 'george', 'week', ';', 'bill', 'like', 'face', 'deaths', 'campaign', 'dems', 'see', 'top', 'bloomberg', 'court', 'race', 'claims', 'dead', 'super', 'big', 'judge', 'bbc', 'test', 'protesters', 'show', 'make', 'india', 'iowa', 'want', 'reopen', 'still', 'live', 'masks', 'found', 'go', 'obama', 'would', 'south', 'flynn', 'election', 'quarantine', 'work', 'need', 'democratic', 'vote', 'rep.', 'california', 'gov', 'best', 'sen.', 'rally', 'reopening', 'trial', 'killed', 'plan', 'toll', 'mayor', 'woman', 'women', 'law', 'vaccine', 'deal', 'years', 'travel', 'end', 'care', 'italy', 'spread', 'impeachment', 'warns', 'last', 'behind', 'debate', 'country', 'protest', 'quiz', 'know', 'attack', 'russia', 'video', 'family', 'star', 'war', 'senate', 'service', 'two', 'officials', 'going', 'pictures', 'next', 'covid', 'follow', 'fears', 'former', 'inside', 'voters', 'pelosi', 'national', 'children', 'chief', 'ahead', "'we", 'murder', 'stop', 'justice', 'testing', 'set', 'warren', 'tells', 'hospital', 'primary', 'win', 'party', 'shooting', '2', '3', 'tv', 'europe', 'briefing', 'much', 'history', 'days', 'korea', 'weekend', 'iran', 'dem', 'many', 'mass', 'free', 'lives', 'order', 'bowl', 'hits', 'call', 'supreme', 'million', 'social', 'michael', 'aid', 'five', 'tucker', 'rise', 'times', 'hong', 'kong', 'florida', 'chinese', 'hannity', 'faces', 'cuomo', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'record', 'doctor', 'charged', 'force', 'governor', 'story', 'takes', 'change', 'exclusive', 'buttigieg', 'public', 'gives', 'facebook', 'gop', 'bolton', 'listen', 'military', 'official', 'away', 'twitter', 'hit', 'open', 'year', 'never', 'way', 'good', 'despite', 'leader', 'mother', 'tuesday', 'john', 'arrested', 'spreads', 'online', 'radio', 'texas', 'got', 'reveals', 'save', 'start', 'stay', 'return', 'slams', 'africa', 'wants', 'ny', '11', 'barr', 'relief', 'must', 'making', 'makes', 'gets', 'long', 'rules', 'even', 'food', 'headlines', 'fall', 'fire', 'bryant', 'look', 'latest', 'ban', 'mask', 'risk', 'russian', 'doctors', 'presidential', 'surge', 'system', 'use', 'security', 'battle', 'killing', 'push', 'emergency', 'another', 'cities', 'think', 'safe', 'blasts', 'federal', 'restrictions', 'cut', 'seattle', 'made', 'team', 'reports', 'key', 'missing', 'lost', 'kobe', '4', 'move', 'probe', 'guide', 'countries', "'the", 'amazon', 'shot', 'racism', 'political', 'minneapolis', 'wuhan', 'wins', 'students', 'threat', 'left', 'mark', 'kids', 'changed', 'close', 'pm', 'medical', 'study', 'around', 'spain', 'ever', 'ship', 'wrong', 'analysis', 'young', 'find', 'washington', 'france', 'government', 'weinstein', 'across', 'die', 'patients', 'goes', 'everything', 'deadly', 'aoc', 'real', 'west', 'experts', 'matter', 'johnson', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'nation', 'died', 'son', 'come', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'night', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'months', 'second', 'mr.', 'chris', 'administration', 'father', 'needs', 'cops', 'major', 'wall', 'problem', 'really', 'might', 'hampshire', 'newt', 'jobs', 'de', 'germany', 'turn', 'message', 'memorial', 'cathedral', 'reads', 'businesses', 'give', '!', 'small', 'plans', 'event', 'near', 'secret', 'tom', 'trying', 'staff', 'coming', 'let', 'carolina', 'blasio', 'sign', 'unrest', 'secretary', 'elizabeth', 'union', 'seen', 'action', 'candidate', 'sick', 'church', 'prison', 'doj', 'patrick', '“', '”', 'canada', 'past', 'girl', 'leaves', 'tweet', 'caucuses', 'questions', 'meghan', 'crash', 'six', 'taking', 'things', 'stars', 'couple', 'congress', 'school', 'orders', '1', 'power', 'hospitals', 'hope', 'violence', 'access', 'fauci', 'mike', 'pompeo', 'clash', 'far', 'better', 'andrew', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'tech', 'fighting']

    top_economic = []
    for i in top_words:
        if i[0] not in economic_exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_economic.append(interlist)
    
    #top people who show up in the top 500 most common words

    for i in top_economic:
        sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__contains=i[0]).values('sentiment')
        total_for_average = 0
    
        for y in sent_average:
            total_for_average += y['sentiment']
    
        total_for_average = total_for_average * 100

        average_key = total_for_average/len(sent_average)

        average_key = round(average_key, 2)

        i.append(average_key)

    
    
    #final places lists
    worst_economic = sorted(top_economic, key = lambda x: x[2])
    top_economic = sorted(top_economic, key = lambda x: x[2], reverse=True)
   
    corona_exceptions = ['trump', 'us', 'new', 'says', 'biden', 'china', 'police', 'world', 'u.s.', 'president', 'amid', 'death', 'york', 'america', 'sanders', 'could', 'crisis', 'uk', 'home', 'house', 'man', 'state', 'black', 'news', 'people', '$', 'back', 'city', 'one', 'joe',  'may', 'first', 'bernie', 'democrats', 'white', 'americans', 'floyd', '2020', 'media', 'take', 'life', 'updates', 'time', 'protests', 'report', 'get', 'calls', 'fight', 'help', 'day', 'dies', 'american', '-', 'dr.', 'say', 'global', 'states', 'response', 'case', 'george', 'week', ';', 'bill', 'like', 'face', 'deaths', 'workers', 'campaign', 'dems', 'see', 'top', 'bloomberg', 'court', 'race', 'claims', 'economy', 'dead', 'super', 'big', 'judge', 'bbc', 'test', 'protesters', 'show', 'make', 'india', 'iowa', 'want', 'still', 'live', 'found', 'go', 'obama', 'would', 'south', 'flynn', 'election', 'work', 'need', 'democratic', 'vote', 'rep.', 'california', 'gov', 'best', 'sen.', 'rally', 'trial', 'killed', 'plan', 'toll', 'mayor', 'woman', 'women', 'law',  'deal', 'years', 'travel', 'end', 'care', 'italy', 'impeachment', 'warns', 'last', 'behind', 'debate', 'country', 'protest', 'quiz', 'know', 'attack', 'russia', 'video', 'family', 'star', 'war', 'senate', 'service', 'two', 'officials', 'going', 'pictures', 'next', 'follow', 'fears', 'former', 'inside', 'voters', 'pelosi', 'national', 'children', 'chief', 'ahead', 'business', "'we", 'murder', 'stop', 'justice', 'set', 'warren', 'tells', 'primary', 'win', 'party', 'shooting', '2', '3', 'tv', 'europe', 'briefing', 'much', 'economic', 'history', 'days', 'korea', 'weekend', 'iran', 'dem', 'many', 'mass', 'free', 'lives', 'order', 'bowl', 'hits', 'call', 'supreme', 'million', 'social', 'michael', 'aid', 'five', 'tucker', 'rise', 'times', 'hong', 'kong', 'florida', 'chinese', 'hannity', 'faces', 'cuomo', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'record', 'doctor', 'charged', 'force', 'governor', 'story', 'takes', 'change', 'exclusive', 'buttigieg', 'stimulus', 'public', 'gives', 'facebook', 'gop', 'bolton', 'listen', 'military', 'official', 'away', 'twitter', 'hit', 'open', 'year', 'never', 'way', 'good', 'despite', 'leader', 'mother', 'tuesday', 'john', 'arrested', 'online', 'radio', 'texas', 'got', 'reveals', 'save', 'start', 'stay', 'return', 'slams', 'africa', 'job', 'wants', 'oil', 'ny', '11', 'barr', 'relief', 'markets', 'must', 'making', 'makes', 'gets', 'long', 'rules', 'even', 'food', 'headlines', 'fall', 'fire', 'bryant', 'look', 'latest', 'ban', 'risk', 'russian', 'doctors', 'presidential', 'surge', 'system', 'use', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'another', 'cities', 'think', 'safe', 'blasts', 'federal', 'restrictions', 'cut', 'seattle', 'made', 'team', 'reports', 'key', 'missing', 'lost', 'kobe', '4', 'move', 'probe', 'guide', 'countries', "'the", 'amazon', 'shot', 'racism', 'political', 'minneapolis', 'wins', 'students', 'threat', 'left', 'mark', 'kids', 'changed', 'close', 'pm', 'medical', 'study', 'around', 'spain', 'ever', 'ship', 'wrong', 'analysis', 'young', 'find', 'washington', 'france', 'government', 'weinstein', 'across', 'die', 'goes', 'everything', 'deadly', 'aoc', 'real', 'west', 'experts', 'matter', 'johnson', 'reform', 'said', 'nevada', 'attacks', 'kill',  'bad', 'nyc', 'nation', 'died', 'son', 'come', 'market', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'night', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'months', 'second', 'mr.', 'chris', 'administration', 'father', 'needs', 'cops', 'major', 'wall', 'problem', 'really', 'might', 'hampshire', 'newt', 'jobs', 'de', 'germany', 'turn', 'message', 'memorial', 'stocks', 'cathedral', 'reads', 'businesses', 'give', '!', 'small', 'plans', 'event', 'near', 'secret', 'tom', 'trying', 'staff', 'coming', 'let', 'carolina', 'blasio', 'sign', 'unrest', 'secretary', 'elizabeth', 'union', 'seen', 'action', 'candidate', 'sick', 'church', 'prison', 'doj', 'patrick', '“', '”', 'canada', 'past', 'girl', 'leaves', 'tweet', 'caucuses', 'questions', 'meghan', 'crash', 'six', 'taking', 'things', 'stars', 'couple', 'congress', 'school', 'orders', '1', 'power', 'hope', 'violence', 'access', 'mike', 'pompeo', 'clash', 'far', 'better', 'andrew', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'tech', 'fighting']

    top_corona = []
    for i in top_words:
        if i[0] not in corona_exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_corona.append(interlist)
    
    #top people who show up in the top 500 most common words

    for i in top_corona:
        sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__contains=i[0]).values('sentiment')
        total_for_average = 0
    
        for y in sent_average:
            total_for_average += y['sentiment']
    
        total_for_average = total_for_average * 100

        average_key = total_for_average/len(sent_average)

        average_key = round(average_key, 2)

        i.append(average_key)

    
    
    #final places lists
    worst_corona = sorted(top_corona, key = lambda x: x[2])
    top_corona = sorted(top_corona, key = lambda x: x[2], reverse=True)

    rp_exceptions = ['coronavirus', 'us', 'new', 'virus', 'says', 'biden', 'china', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.', 'president', 'amid', 'death', 'york', 'america', 'sanders', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'man', 'state', 'news', 'outbreak', 'people', '$', 'back', 'city', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'democrats', 'americans', '2020', 'media', 'take', 'life', 'updates', 'time', 'report', 'get', 'calls', 'fight', 'help', 'day', 'dies', 'american', '-', 'dr.', 'say', 'global', 'states', 'response', 'case', 'george', 'week', ';', 'bill', 'like', 'face', 'deaths', 'workers', 'campaign', 'dems', 'see', 'top', 'bloomberg', 'court', 'race', 'claims', 'economy', 'dead', 'super', 'big', 'judge', 'bbc', 'test', 'show', 'make', 'india', 'iowa', 'want', 'reopen', 'still', 'live', 'masks', 'found', 'go', 'obama', 'would', 'south', 'flynn', 'election', 'quarantine', 'work', 'need', 'democratic', 'vote', 'rep.', 'california', 'gov', 'best', 'sen.', 'reopening', 'trial', 'killed', 'plan', 'toll', 'mayor', 'woman', 'women', 'law', 'vaccine', 'deal', 'years', 'travel', 'end', 'care', 'italy', 'spread', 'impeachment', 'warns', 'last', 'behind', 'debate', 'country', 'protest', 'quiz', 'know', 'attack', 'russia', 'video', 'family', 'star', 'war', 'senate', 'service', 'two', 'officials', 'going', 'pictures', 'next', 'covid', 'follow', 'fears', 'former', 'inside', 'voters', 'pelosi', 'national', 'children', 'chief', 'ahead', 'business', "'we", 'murder', 'stop', 'testing', 'set', 'warren', 'tells', 'hospital', 'primary', 'win', 'party', 'shooting', '2', '3', 'tv', 'europe', 'briefing', 'much', 'economic', 'history', 'days', 'korea', 'weekend', 'iran', 'dem', 'many', 'mass', 'free', 'lives', 'order', 'bowl', 'hits', 'call', 'supreme', 'million', 'social', 'michael', 'aid', 'five', 'tucker', 'rise', 'times', 'hong', 'kong', 'florida', 'chinese', 'hannity', 'faces', 'cuomo', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'record', 'doctor', 'charged', 'force', 'governor', 'story', 'takes', 'change', 'exclusive', 'buttigieg', 'stimulus', 'public', 'gives', 'facebook', 'gop', 'bolton', 'listen', 'military', 'official', 'away', 'twitter', 'hit', 'open', 'year', 'never', 'way', 'good', 'despite', 'leader', 'mother', 'tuesday', 'john', 'arrested', 'spreads', 'online', 'radio', 'texas', 'got', 'reveals', 'save', 'start', 'stay', 'return', 'slams', 'africa', 'job', 'wants', 'oil', 'ny', '11', 'barr', 'relief', 'markets', 'must', 'making', 'makes', 'gets', 'long', 'rules', 'even', 'food', 'headlines', 'fall', 'fire', 'bryant', 'look', 'latest', 'ban', 'mask', 'risk', 'russian', 'doctors', 'presidential', 'surge', 'system', 'use', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'another', 'cities', 'think', 'safe', 'blasts', 'federal', 'restrictions', 'cut', 'seattle', 'made', 'team', 'reports', 'key', 'missing', 'lost', 'kobe', '4', 'move', 'probe', 'guide', 'countries', "'the", 'amazon', 'shot', 'political', 'minneapolis', 'wuhan', 'wins', 'students', 'threat', 'left', 'mark', 'kids', 'changed', 'close', 'pm', 'medical', 'study', 'around', 'spain', 'ever', 'ship', 'wrong', 'analysis', 'young', 'find', 'washington', 'france', 'government', 'weinstein', 'across', 'die', 'patients', 'goes', 'everything', 'deadly', 'aoc', 'real', 'west', 'experts', 'matter', 'johnson', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'nation', 'died', 'son', 'come', 'market', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'night', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'months', 'second', 'mr.', 'chris', 'administration', 'father', 'needs',  'major', 'wall', 'problem', 'really', 'might', 'hampshire', 'newt', 'jobs', 'de', 'germany', 'turn', 'message', 'memorial', 'stocks', 'cathedral', 'reads', 'businesses', 'give', '!', 'small', 'plans', 'event', 'near', 'secret', 'tom', 'trying', 'staff', 'coming', 'let', 'carolina', 'blasio', 'sign', 'unrest', 'secretary', 'elizabeth', 'union', 'seen', 'action', 'candidate', 'sick', 'church', 'prison', 'doj', 'patrick', '“', '”', 'canada', 'past', 'girl', 'leaves', 'tweet', 'caucuses', 'questions', 'meghan', 'crash', 'six', 'taking', 'things', 'stars', 'couple', 'congress', 'school', 'orders', '1', 'power', 'hospitals', 'hope', 'violence', 'access', 'fauci', 'mike', 'pompeo', 'clash', 'far', 'better', 'andrew', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'tech', 'fighting']
    
    top_rp = []
    for i in top_words:
        if i[0] not in rp_exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            top_rp.append(interlist)
    
    #top people who show up in the top 500 most common words

    for i in top_rp:
        sent_average = Headline.objects.filter(day_order__lte=25).filter(headline__contains=i[0]).values('sentiment')
        total_for_average = 0
    
        for y in sent_average:
            total_for_average += y['sentiment']
    
        total_for_average = total_for_average * 100

        average_key = total_for_average/len(sent_average)

        average_key = round(average_key, 2)

        i.append(average_key)

    
    
    #final places lists
    worst_rp = sorted(top_rp, key = lambda x: x[2])
    top_rp = sorted(top_rp, key = lambda x: x[2], reverse=True)

    

    return render(request, 'custom_scraper/sentiment_overall_ajax.html', {'html_divos':html_divos, "average_sent":average_sent, "html_div_sent_hr": html_div_sent_hr, "html_div_pie": html_div_pie, "fig_sent_hist_div": fig_sent_hist_div, 'final_list': final_list, 'html_div_fig_pn': html_div_fig_pn, "top10list":top10list, "bottom10list":bottom10list, "positive":positive, "negative":negative, 'html_divosd':html_divosd, 'html_div_figdow': html_div_figdow, "html_divos_jason": html_divos_jason, 'this_month':this_month, 'top_overall':top_overall, 'worst_overall': worst_overall, 'best_people': best_people, 'top_places': top_places, 'top_political': top_political, 'top_rp': top_rp, 'top_economic': top_economic, 'top_corona': top_corona})


def sentiment_compare(request):
    from datetime import datetime
    from calendar import monthrange
    from django.db.models.functions import TruncYear


    average_sentiment_by_date_compare = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by("Date",)
    

    comparesent = pd.DataFrame(list(average_sentiment_by_date_compare))
    comparesent['Average'] = comparesent['Average'] * 100
    comparesent['newspaper'] = comparesent['newspaper'].replace(1, 'The New York Times')
    comparesent['newspaper'] = comparesent['newspaper'].replace(2, 'BBC News')
    comparesent['newspaper'] = comparesent['newspaper'].replace(3, 'Fox News')
    comparesent.rename(columns={'newspaper':'Newspaper'}, inplace= True)


    figcompare = px.line(comparesent, x="Date", y="Average", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )
   

    figcompare.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))

    figcompare.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                
                
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True,
            thickness=.05
        ),
        type="date"
    )
)
    
    
    html_div_compare = str(plotly.offline.plot(figcompare, output_type='div', config = {'displayModeBar': False}))
    
    average_sentiment_by_date_compare_month = Headline.objects.annotate(Date=TruncMonth('date')).values('Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by("Date",)
    

    comparesent_month = pd.DataFrame(list(average_sentiment_by_date_compare_month))
    comparesent_month['Average'] = comparesent_month['Average'] * 100
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(1, 'The New York Times')
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(2, 'BBC News')
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(3, 'Fox News')
    comparesent_month.rename(columns={'newspaper':'Newspaper'}, inplace= True)


    figcompare_month = px.line(comparesent_month, x="Date", y="Average", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )
   

    figcompare_month.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0))

    
    
    html_div_compare_month = str(plotly.offline.plot(figcompare_month, output_type='div', config = {'displayModeBar': False}))
   
    today = datetime.today()

    

    def get_calendar(np_code):
        selected_month = today.month

        month_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=np_code).filter(date__month=selected_month).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
        
        
        dates = []
        sentiments = []

        current_month_days = monthrange(today.year, selected_month)

        

        current_month_check = [] 
        for i in range(1,current_month_days[1]+1):
            current_month_check.append(datetime(today.year, selected_month, i, 0, 0))
        
        
        for i in month_sent:
            dates.append(i['Date'])
        

        

        for i in current_month_check:
            if i not in dates:
                dates.append(i)
        
       

        final_list = []

        for i in month_sent:
            if i['Date'] in dates:
                interlist = []
                interlist.append(i['Date'])
                interlist.append(round(i['Average']*100,1))
                final_list.append(interlist)
        
        

        for i in range(len(final_list), len(dates)):
            interlist = []
            interlist.append(dates[i])
            interlist.append('')
            
            final_list.append(interlist)
        
        


        
        final_list.sort(key = lambda x: x[0])

        

        for i in final_list:
            number_date = i[0].strftime("%d")
            
            i.append(int(number_date))
        
        

        from datetime import date
        import calendar
        my_date = final_list[0][0]
        day_of_week = calendar.day_name[my_date.weekday()]
        this_month = calendar.month_name[my_date.month]

        for i in final_list:
            i.append("{:02d}".format(i[0].month))
            i.append("{:02d}".format(i[0].day))
            i.append(i[0].year)

        if day_of_week == "Monday":
            final_list.insert(0,[' ',' ',' ', '#', '', ''])
        elif day_of_week == "Wednesday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
        
        
        return(final_list)
    
    nytimes_cal = get_calendar(1)
    bbc_cal = get_calendar(2)
    fn_cal = get_calendar(3)

    

    from datetime import date
    import calendar
    my_date = nytimes_cal[8][0]
    
    this_month = calendar.month_name[my_date.month]
    

    

    def get_calendar_last(np_code):
        selected_month = today.month - 1

        month_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=np_code).filter(date__month=selected_month).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
        
        
        dates = []
        sentiments = []

        current_month_days = monthrange(today.year, selected_month)

        

        current_month_check = [] 
        for i in range(1,current_month_days[1]+1):
            current_month_check.append(datetime(today.year, selected_month, i, 0, 0))
        
        
        for i in month_sent:
            dates.append(i['Date'])
        

        

        for i in current_month_check:
            if i not in dates:
                dates.append(i)
        
        

        final_list = []

        for i in month_sent:
            if i['Date'] in dates:
                interlist = []
                interlist.append(i['Date'])
                interlist.append(round(i['Average']*100,1))
                final_list.append(interlist)
        
        

        for i in range(len(final_list), len(dates)):
            interlist = []
            interlist.append(dates[i])
            interlist.append('')
            
            final_list.append(interlist)
        
        


        
        final_list.sort(key = lambda x: x[0])

        

        for i in final_list:
            number_date = i[0].strftime("%d")
            
            i.append(int(number_date))
        
       

        from datetime import date
        import calendar
        my_date = final_list[0][0]
        day_of_week = calendar.day_name[my_date.weekday()]
        this_month = calendar.month_name[my_date.month]

        for i in final_list:
            i.append("{:02d}".format(i[0].month))
            i.append("{:02d}".format(i[0].day))
            i.append(i[0].year)

        if day_of_week == "Monday":
            final_list.insert(0,[' ',' ',' ', '#', '', ''])
        elif day_of_week == "Wednesday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
        
        
        return(final_list)
    
    nytimes_cal_last = get_calendar_last(1)
    bbc_cal_last = get_calendar_last(2)
    fn_cal_last = get_calendar_last(3)

    

    from datetime import date
    import calendar
    last_date = nytimes_cal_last[8][0]
    
    last_month = calendar.month_name[last_date.month]
    
    

    import plotly.graph_objects as go

    def pie_for_paper(paper_num):
        overall_pos = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(sentiment__gt=0).values('sentiment')

        overall_neg = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(sentiment__lt=0).values('sentiment')

        overall_zero = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(sentiment=0).values('sentiment')

        pie_labels = ['Positive', 'Negative', 'Neutral']

        pie_values = []

        pie_values.append(len(overall_pos))
        pie_values.append(len(overall_neg))
        pie_values.append(len(overall_zero))


        pie_fig = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values), ])

        pie_fig.update_layout(
        font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', margin=dict(l=5, r=5, t=5, b=5, pad=10),showlegend=False )

        pie_fig.update_traces(marker=dict(colors=["rgb(33,102,172)",'rgb(178,24,43)', 'whitesmoke']))

        


        html_div_pie = str(plotly.offline.plot(pie_fig, output_type='div',config = {'displayModeBar': False},))

        return html_div_pie
    
    nyt_pie = pie_for_paper(1)
    bbc_pie = pie_for_paper(2)
    fn_pie = pie_for_paper(3)

    def year_average_paper(paper_num):

        average_sentiment_by_month_one = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).annotate(Date=TruncYear('date')).values('newspaper','Date').annotate(Average=Avg('sentiment')).order_by("Date")

        
        for i in average_sentiment_by_month_one:
           
            average_sent = i['Average']
        
        average_sent = average_sent * 100
        average_sent = round(average_sent, 1)
       
        return average_sent

    nyt_average_ytd = year_average_paper(1)
    bbc_average_ytd = year_average_paper(2)
    fn_average_ytd = year_average_paper(3)


    from django.db.models import Count

    average_sentiment_by_month_compare_pos = Headline.objects.filter(day_order__lte=25).filter(sentiment__gt=0).annotate(Date=TruncMonth('date')).values('Date', 'newspaper').annotate(Count=Count('id')).order_by("Date",)
    

    comparesent_month = pd.DataFrame(list(average_sentiment_by_month_compare_pos))
    comparesent_month['Count'] = comparesent_month['Count'] 
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(1, 'The New York Times')
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(2, 'BBC News')
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(3, 'Fox News')
    comparesent_month.rename(columns={'newspaper':'Newspaper'}, inplace= True)

   


    figcompare_month_pos = px.line(comparesent_month, x="Date", y="Count", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )
   

    figcompare_month_pos.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')

   
    html_div_compare_month_pos = str(plotly.offline.plot(figcompare_month_pos, output_type='div', config = {'displayModeBar': False}))

    average_sentiment_by_month_compare_neg = Headline.objects.filter(day_order__lte=25).filter(sentiment__lt=0).annotate(Date=TruncMonth('date')).values('Date', 'newspaper').annotate(Count=Count('id')).order_by("Date",)
    

    comparesent_month_neg = pd.DataFrame(list(average_sentiment_by_month_compare_neg))
    comparesent_month_neg['Count'] = comparesent_month_neg['Count'] 
    comparesent_month_neg['newspaper'] = comparesent_month_neg['newspaper'].replace(1, 'The New York Times')
    comparesent_month_neg['newspaper'] = comparesent_month_neg['newspaper'].replace(2, 'BBC News')
    comparesent_month_neg['newspaper'] = comparesent_month_neg['newspaper'].replace(3, 'Fox News')
    comparesent_month_neg.rename(columns={'newspaper':'Newspaper'}, inplace= True)

    


    figcompare_month_neg = px.line(comparesent_month_neg, x="Date", y="Count", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )
   

    figcompare_month_neg.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')
    
    html_div_compare_month_neg = str(plotly.offline.plot(figcompare_month_neg, output_type='div', config = {'displayModeBar': False}))
    

    average_sentiment_by_month_compare_neu = Headline.objects.filter(day_order__lte=25).filter(sentiment=0).annotate(Date=TruncMonth('date')).values('Date', 'newspaper').annotate(Count=Count('id')).order_by("Date",)
    

    comparesent_month_neu = pd.DataFrame(list(average_sentiment_by_month_compare_neu))
    comparesent_month_neu['Count'] = comparesent_month_neu['Count'] 
    comparesent_month_neu['newspaper'] = comparesent_month_neu['newspaper'].replace(1, 'The New York Times')
    comparesent_month_neu['newspaper'] = comparesent_month_neu['newspaper'].replace(2, 'BBC News')
    comparesent_month_neu['newspaper'] = comparesent_month_neu['newspaper'].replace(3, 'Fox News')
    comparesent_month_neu.rename(columns={'newspaper':'Newspaper'}, inplace= True)

    


    figcompare_month_neu = px.line(comparesent_month_neu, x="Date", y="Count", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )
   

    figcompare_month_neu.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')
    
    html_div_compare_month_neu = str(plotly.offline.plot(figcompare_month_neu, output_type='div', config = {'displayModeBar': False}))

  
    from django.db.models.functions import ExtractWeekDay

    dow_test = Headline.objects.filter(day_order__lte=25).annotate(weekday=ExtractWeekDay('date')).values('weekday', 'newspaper').annotate(Average=Avg('sentiment'))


    
       
    
    dow_sent = pd.DataFrame(list(dow_test))
    
    dow_sent['Average'] = dow_sent['Average'] * 100
    dow_sent['weekday'] = dow_sent['weekday'].replace(1, 'Sunday')
    dow_sent['weekday'] = dow_sent['weekday'].replace(2, 'Monday')
    dow_sent['weekday'] = dow_sent['weekday'].replace(3, 'Tuesday')
    dow_sent['weekday'] = dow_sent['weekday'].replace(4, 'Wednesday')
    dow_sent['weekday'] = dow_sent['weekday'].replace(5, 'Thursday')
    dow_sent['weekday'] = dow_sent['weekday'].replace(6, 'Friday')
    dow_sent['weekday'] = dow_sent['weekday'].replace(7, 'Saturday')
    
    dow_sent['newspaper'] = dow_sent['newspaper'].replace(1, 'The New York Times')
    dow_sent['newspaper'] = dow_sent['newspaper'].replace(2, 'BBC News')
    dow_sent['newspaper'] = dow_sent['newspaper'].replace(3, 'Fox News')
    dow_sent.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    

    
    


    figcompare_dow_sent = px.line(dow_sent, x="weekday", y="Average", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )
   

    figcompare_dow_sent.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')
    
    html_div_compare_dow_sent = str(plotly.offline.plot(figcompare_dow_sent, output_type='div', config = {'displayModeBar': False}))
    
    from django.db.models import F
    from django.db.models.functions import Ceil

    hist_sent = Headline.objects.filter(day_order__lte=25).exclude(sentiment=0).annotate(Sentiment=F('sentiment') * 10).annotate(Sent=Ceil('Sentiment')).values('newspaper','Sent').annotate(Count=Count('id'))
   
    hist_sentdf = pd.DataFrame(list(hist_sent))
    
    
    hist_sentdf['newspaper'] = hist_sentdf['newspaper'].replace(1, 'The New York Times')
    hist_sentdf['newspaper'] = hist_sentdf['newspaper'].replace(2, 'BBC News')
    hist_sentdf['newspaper'] = hist_sentdf['newspaper'].replace(3, 'Fox News')
    hist_sentdf.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    

    
    


    figcompare_hist_sent = px.line(hist_sentdf, x="Sent", y="Count", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )
   

    figcompare_hist_sent.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), )
    
    html_div_compare_hist_sent = str(plotly.offline.plot(figcompare_hist_sent, output_type='div', config = {'displayModeBar': False}))

    sent_hr = Headline.objects.filter(day_order__lte=25).values('newspaper', 'day_order').annotate(Average=Avg('sentiment'))

    sent_hr_df = pd.DataFrame(list(sent_hr))
    
    
    sent_hr_df['Average'] = sent_hr_df['Average'] * 100
    sent_hr_df['newspaper'] = sent_hr_df['newspaper'].replace(1, 'The New York Times')
    sent_hr_df['newspaper'] = sent_hr_df['newspaper'].replace(2, 'BBC News')
    sent_hr_df['newspaper'] = sent_hr_df['newspaper'].replace(3, 'Fox News')
    sent_hr_df.rename(columns={'newspaper':'Newspaper'}, inplace= True)
    sent_hr_df.rename(columns={'day_order':'Rank'}, inplace= True)
    

    
    


    figcompare_sent_hr = px.line(sent_hr_df, x="Rank", y="Average", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )
   

    figcompare_sent_hr.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), )
    
    html_div_compare_sent_hr = str(plotly.offline.plot(figcompare_sent_hr, output_type='div', config = {'displayModeBar': False}))

    
   
    
    
    def find_positive(paper_num):
        all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

        all_headline_string = ""

        for i in all_headlines: 
            all_headline_string += " " + i['headline']
    
    
        import nltk
        from nltk import FreqDist
        from nltk.corpus import stopwords
        stopword = stopwords.words('english')
        text = all_headline_string
        word_tokens = nltk.word_tokenize(text.lower())
        removing_stopwords = [word for word in word_tokens if word not in stopword]
        freq = FreqDist(removing_stopwords)
        most_common = freq.most_common(500)

        list_of_top_words = []

        for i in most_common: 
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            list_of_top_words.append(interlist)
    
    

        exceptions = [',',':',"'",'.','?', "'s", '‘', "n't", '’']

        top_words = []

        for i in list_of_top_words:
            if i[0] not in exceptions:
                interlist = []
                interlist.append(i[0])
                interlist.append(i[1])
                top_words.append(interlist)





        overall_words = []
        for i in top_words: 
            overall_words.append(i)

        

        for i in overall_words:
            paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
            i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))

     
        
    

        best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
        worst_words = sorted(overall_words, key = lambda x: x[2],)

        best_and_worst = []
        best_and_worst.append(best_words[:100])
        best_and_worst.append(worst_words[:100])

        return best_and_worst
        


    nyt_words = find_positive(1)
    nyt_best_words = nyt_words[0]
    nyt_worst_words = nyt_words[1]

    bbc_words = find_positive(2)
    bbc_best_words = bbc_words[0]
    bbc_worst_words = bbc_words[1]

    fn_words = find_positive(3)
    fn_best_words = fn_words[0]
    fn_worst_words = fn_words[1]

    
   

    def find_people(paper_num):
        all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

        all_headline_string = ""

        for i in all_headlines: 
            all_headline_string += " " + i['headline']
    
    
        import nltk
        from nltk import FreqDist
        from nltk.corpus import stopwords
        stopword = stopwords.words('english')
        text = all_headline_string
        word_tokens = nltk.word_tokenize(text.lower())
        removing_stopwords = [word for word in word_tokens if word not in stopword]
        freq = FreqDist(removing_stopwords)
        most_common = freq.most_common(300)

        list_of_top_words = []

        for i in most_common: 
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            list_of_top_words.append(interlist)
    
    

        exceptions = ['georgia', 'worse', 'democrat', 'run', 'warning', 'crime',  'fbi', 'due', 'game', 'explains', 'reacts', 'daughter', 'responds', 'jail', 'nypd',  'baby', 'boy', 'symptoms', 'afghan', 'eu', 'visual', 'isolation', 'italian', 'tracking', 'denies', 'israel', 'french', 'australian', 'abuse', 'theme', 'suspect', 'turkey', 'brazil', 'arrest', 'aged', 'london', 'harry', 'since', 'mental' , 'delhi', '-', 'speech', '&', 'impact', 'vp', "–",   'cnn', 'calling',      'distancing', 'saved', 'german', 'boss', 'australia', 'four', 'ca', 'huge', 'largest', 'england', 'photo', 'sea', 'passes', 'row', 'indian', 'ways',   'cdc', 'announces', 'issues', 'nfl', 'massive', 'comments', 'owner', 'dc', '-',       '...', 'begins', 'jailed', "'my", 'minister', 'queen', "'ve", 'reopens', 'largest'   'huge', 'shots', 'tips', 'rare', 'birthday', 'app', 'storm', 'returns',     'politics', 'c.d.c', 'finally', 'street', 'g.o.p', 'outbreaks', 'shots',         'hot', 'defense', 'control', 'facing', 'billion', 'schools', 'summer',    'w.h.o',          'coverage', 'providing', 'love', 'read', 'everyone', 'trillion', 'rich', 'region', 'rights', 'region', 'rights','threatens', '5', 'japan', 'moves', '(', ')', 'happened', 'already', 'became', 'nearly',      ',',':',"'",'.','?', "'s", '‘', "n't", '’', 'better', 'mike', 'hospitals', 'andrew', 'event', 'orders', 'tech', 'past','coronavirus', 'us', 'new', 'virus', 'says', 'george',  'china', 'police', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.', 'president', 'amid', 'york', 'death', 'america', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'state', 'man', 'news', '$', 'black', 'outbreak', 'people', 'city', 'back', 'one', 'joe', 'health', 'may', 'first', 'democrats', 'americans', 'white', 'media', '2020', 'take', 'life', 'time', 'updates', 'protests', 'report', 'get', 'calls', 'fight', 'help', '-', 'dr.', 'states', 'global', 'dies', 'response', 'day', 'say', 'case', 'american', 'week', 'bill', ';', 'deaths', 'workers', 'face', 'like', 'dems', 'top', 'see', 'campaign', 'claims', 'economy', 'race', 'court', 'super', 'judge', 'big', 'bbc', 'dead', 'test', 'protesters', 'show', 'india', 'iowa', 'make', 'want', 'reopen', 'still', 'live', 'found', 'go', 'would', 'quarantine', 'masks', 'south', 'work', 'election', 'need', 'democratic', 'vote', 'rep.', 'gov', 'sen.', 'california', 'rally', 'trial', 'plan', 'reopening', 'best', 'toll', 'law', 'vaccine', 'deal', 'travel', 'italy', 'spread', 'impeachment', 'woman', 'women', 'killed', 'end', 'mayor', 'warns', 'last', 'years', 'behind', 'care', 'debate', 'country', 'protest', 'russia', 'know', 'video', 'family', 'attack', 'war', 'quiz', 'senate', 'officials', 'going', 'fears', 'star', 'two', 'inside', 'pictures', 'next', 'former', 'service', 'covid', 'follow', 'voters', 'business', 'children', "'we", 'murder', 'stop', 'chief', 'national', 'testing', 'set', 'hospital', 'ahead', 'primary', 'tells', 'party', 'justice', 'shooting', 'europe', 'briefing', 'much', '2', 'economic', '3', 'tv', 'days', 'korea', 'iran', 'dem', 'win', 'mass', 'free', 'bowl', 'call', 'history', 'million', 'social', 'aid', 'lives', 'order', 'hits', 'five', 'many', 'michael', 'faces', 'rise', 'weekend', 'times', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'hong', 'kong', 'florida', 'supreme', 'chinese', 'doctor', 'charged', 'force', 'governor', 'takes', 'change', 'record', 'exclusive', 'stimulus', 'public', 'facebook', 'listen', 'twitter', 'hit', 'open', 'story', 'official', 'good', 'despite', 'leader', 'mother', 'tuesday', 'year', 'never', 'gives', 'gop', 'john', 'military', 'way', 'arrested', 'spreads', 'online', 'radio', 'got', 'reveals', 'save', 'stay', 'slams', 'africa', 'job', 'wants', 'texas', 'away', 'oil', 'ny', 'relief', 'markets', 'return', 'must', 'making', 'gets', 'long', 'start', 'rules', 'even', 'fall', 'fire', 'makes', 'look', 'latest', 'ban', 'risk', 'doctors', 'surge', 'use', 'food', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'russian', '11', 'federal', 'restrictions', 'cut', 'headlines', 'team', 'key', 'missing', 'kobe', 'probe', 'guide', 'mask', "'the", 'amazon', 'another', 'presidential', 'system', 'think', 'blasts', 'political', 'minneapolis', 'wuhan', 'reports', 'wins', 'lost', 'students', 'mark', 'move', 'kids', 'countries', 'changed', 'close', 'pm', 'shot', 'cities', 'safe', 'medical', 'study', 'seattle', 'made', 'ever', 'ship', 'threat', 'analysis', 'young', 'find', 'france',  'across', 'racism', 'die', 'patients', 'around', 'spain', 'goes', 'everything', 'wrong', 'real', 'washington', 'matter', 'government', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'died', 'deadly', 'left', 'experts', 'come', 'market', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'second', 'mr.', 'chris', 'administration', 'cops', 'wall', 'really', 'might', 'hampshire', 'jobs', 'de', 'germany', 'night', 'memorial', 'stocks', 'cathedral', 'businesses', 'nation', 'small', 'months', 'son', 'near', 'major', 'tom', 'trying', 'problem', 'coming', 'let', 'sign', 'turn', 'give', 'elizabeth', '4', 'seen', 'action', 'plans', 'west', 'father', 'secret', 'candidate', 'sick', 'prison', 'carolina', 'doj', 'message', 'reads', 'patrick', 'secretary', 'union', '!', 'canada', 'tweet', 'caucuses', 'meghan', 'crash', 'taking', 'things', 'stars', 'couple', 'needs', 'congress', 'school', 'power', 'staff', 'hope', 'violence', 'access', 'unrest',  'clash', '“', '”', 'far', 'girl', 'leaves', 'questions', 'six', 'today', 'pay', 'support', 'book', 'leaders', 'fighting', "'re", 'money', '1', 'officer', 'claim', 'release', 'without', 'church', 'concerns' ]

        top_words = []

        

        for i in list_of_top_words:
            if i[0] not in exceptions:
                interlist = []
                interlist.append(i[0])
                interlist.append(i[1])
                top_words.append(interlist)





        overall_words = []
        for i in top_words: 
            overall_words.append(i)

        

        for i in overall_words:
            paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
            i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))

     
        
    

        best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
        worst_words = sorted(overall_words, key = lambda x: x[2],)

        best_and_worst = []
        best_and_worst.append(best_words)
        best_and_worst.append(worst_words[:20])
        best_and_worst.append(exceptions)

        return best_and_worst

    nyt_people = find_people(1)
    nyt_best_people = nyt_people[0]
    nyt_worst_people = nyt_people[1]
    bbc_people = find_people(2)
    bbc_best_people = bbc_people[0]
    bbc_worst_people = bbc_people[1]
    fn_people = find_people(3)
    fn_best_people = fn_people[0]
    fn_worst_people = fn_people[1]
    people_exceptions = nyt_people[2]


    def find_places(paper_num):
        all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

        all_headline_string = ""

        for i in all_headlines: 
            all_headline_string += " " + i['headline']


        import nltk
        from nltk import FreqDist
        from nltk.corpus import stopwords
        stopword = stopwords.words('english')
        text = all_headline_string
        word_tokens = nltk.word_tokenize(text.lower())
        removing_stopwords = [word for word in word_tokens if word not in stopword]
        freq = FreqDist(removing_stopwords)
        most_common = freq.most_common(300)

        list_of_top_words = []

        for i in most_common: 
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            list_of_top_words.append(interlist)



        exceptions = [ 'crime', 'stone', 'democrat', 'run', 'worse' , 'warning',  'mental', 'theme', 'suspect', 'arrest', 'aged', 'harry', 'since',   'visual', 'isolation', 'tracking', 'denies', 'abuse',  'due', 'schumer', 'game', 'jail', 'gutfeld', 'nypd', 'fbi', 'mom',  'clinton', 'graham', 'texas', 'responds', 'wife', 'calling', 'explains', 'reacts', 'daughter',  "&", 'impact', 'vp', 'gingrich', 'cnn', 'mccarthy', 'mcenany',  'owner', "n't", "–", 'speech',    'pence', 'cdc', 'announces', 'issues', 'nfl', 'massive', 'comments', "'s", "'",'boss', 'boy', 'symptoms', 'boss', 'four', 'ca', 'baby', 'ways', 'distancing', 'saved',   "'ve", 'reopens', 'largest', 'photo', 'sea', 'passes', 'row', 'minister', 'queen', 'storm', 'returns', '...', 'begins', 'jailed', "'my" ,  'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app',    'donald','outbreaks', 'w.h.o', 'c.d.c', 'finally', 'street', 'g.o.p',        '.',':', 'schools', '?' , "’", ",", "summer", "‘",      'politics', 'hot', 'defense', 'control', 'facing', 'billion',      'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became',            'better', 'mike', 'hospitals', 'andrew', 'event', 'orders', 'tech', 'past','coronavirus', 'trump', 'us', 'new', 'virus', 'says', 'biden', 'police', 'covid-19', 'pandemic', 'lockdown', 'world', 'president', 'amid', 'death', 'sanders', 'could', 'crisis', 'cases', 'home', 'house', 'state', 'man', 'news', '$', 'black', 'outbreak', 'people', 'city', 'back', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'democrats', 'white', 'floyd', 'media', '2020', 'take', 'life', 'time', 'updates', 'protests', 'report', 'get', 'calls', 'fight', 'help', '-', 'dr.', 'states', 'dies', 'response', 'day', 'say', 'george', 'case',  'week', 'bill', ';', 'deaths', 'workers', 'face', 'like', 'dems', 'top', 'bloomberg', 'see', 'campaign', 'claims', 'economy', 'race', 'court', 'super', 'judge', 'big', 'bbc', 'dead', 'test', 'protesters', 'show', 'make', 'want', 'reopen', 'still', 'live', 'obama', 'found', 'go', 'flynn', 'would', 'quarantine', 'masks', 'south', 'work', 'election', 'need', 'democratic', 'vote', 'rep.', 'gov', 'sen.', 'rally', 'trial', 'plan', 'reopening', 'best', 'toll', 'law', 'vaccine', 'deal', 'travel', 'spread', 'impeachment', 'woman', 'women', 'killed', 'end', 'mayor', 'warns', 'last', 'years', 'behind', 'care', 'debate', 'country', 'protest', 'know', 'video', 'family', 'attack', 'war', 'quiz', 'senate', 'officials', 'going', 'fears', 'star', 'two', 'inside', 'pictures', 'next', 'former', 'service', 'pelosi', 'covid', 'follow', 'voters', 'business', 'children', "'we", 'murder', 'stop', 'chief', 'national', 'testing', 'set', 'warren', 'hospital', 'ahead', 'primary', 'tells', 'party', 'justice', 'shooting', 'briefing', 'much', '2', 'economic', '3', 'tv', 'days', 'dem', 'win', 'mass', 'free', 'bowl', 'call', 'history', 'million', 'social', 'aid', 'lives', 'order', 'hits', 'five', 'many', 'michael', 'tucker', 'hannity', 'faces', 'cuomo', 'rise', 'weekend', 'times', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'kong', 'supreme', 'doctor', 'charged', 'force', 'governor', 'takes', 'change', 'record', 'exclusive', 'buttigieg', 'stimulus', 'public', 'facebook', 'bolton', 'listen', 'twitter', 'hit', 'open', 'story', 'official', 'good', 'despite', 'leader', 'mother', 'tuesday', 'year', 'never', 'gives', 'gop', 'john', 'military', 'way', 'arrested', 'spreads', 'online', 'radio', 'got', 'reveals', 'save', 'stay', 'slams', 'job', 'wants', 'away', 'oil', 'barr', 'relief', 'markets', 'return', 'must', 'making', 'gets', 'long', 'start', 'rules', 'even', 'fall', 'fire', 'bryant', 'makes', 'look', 'latest', 'ban', 'risk', 'doctors', 'surge', 'use', 'food', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', '11', 'federal', 'restrictions', 'cut', 'headlines', 'team', 'key', 'missing', 'kobe', 'probe', 'guide', 'mask', "'the", 'amazon', 'another', 'presidential', 'system', 'think', 'blasts', 'political', 'minneapolis', 'reports', 'wins', 'lost', 'students', 'mark', 'move', 'kids', 'countries', 'changed', 'close', 'pm', 'shot', 'cities', 'safe', 'medical', 'study', 'made', 'ever', 'ship', 'threat', 'analysis', 'young', 'find', 'france', 'weinstein', 'across', 'racism', 'die', 'patients', 'around',  'goes', 'everything', 'wrong', 'aoc', 'real', 'matter', 'government', 'reform', 'said', 'attacks', 'kill', 'tests', 'bad',  'died', 'deadly', 'left', 'experts', 'come', 'market', 'possible', 'point', 'johnson', 'mean', 'worst', 'results', 'drug', 'north', 'sex', 'positive', 'daily', 'shows', 'cruise', 'great', 'college', 'second', 'mr.', 'chris', 'administration', 'cops', 'wall', 'really', 'might',  'jobs', 'de', 'night', 'memorial', 'stocks', 'cathedral', 'businesses', 'nation', 'small', 'months', 'son', 'near', 'major', 'tom', 'trying', 'problem', 'coming', 'let', 'newt', 'blasio', 'sign', 'turn', 'give', 'elizabeth', '4', 'seen', 'action', 'plans', 'father', 'secret', 'candidate', 'sick', 'prison', 'doj', 'message', 'reads', 'patrick', 'secretary', 'union', '!', 'tweet', 'caucuses', 'meghan', 'crash', 'taking', 'things', 'stars', 'couple', 'needs', 'congress', 'school', 'power', 'staff', 'hope', 'violence', 'access', 'fauci', 'unrest', 'pompeo', 'clash', '“', '”', 'far', 'girl', 'leaves', 'questions', 'six', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'fighting', "'re", 'money', '1', 'officer', 'claim', 'release', 'without', 'siegel', 'church', 'concerns']

        top_words = []



        for i in list_of_top_words:
            if i[0] not in exceptions:
                interlist = []
                interlist.append(i[0])
                interlist.append(i[1])
                top_words.append(interlist)





        overall_words = []
        for i in top_words: 
            overall_words.append(i)



        for i in overall_words:
            paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
            i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





        best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
        worst_words = sorted(overall_words, key = lambda x: x[2],)

        best_and_worst = []
        best_and_worst.append(best_words)
        best_and_worst.append(worst_words[:20])
        best_and_worst.append(exceptions)

        return best_and_worst

    nyt_places = find_places(1)
    bbc_places = find_places(2)
    fn_places = find_places(3)

    nyt_best_places = nyt_places[0]
    nyt_worst_places = nyt_places[1]

    bbc_best_places = bbc_places[0]
    bbc_worst_places = bbc_places[1]

    fn_best_places = fn_places[0]
    fn_worst_places = fn_places[1]
    place_exceptions = nyt_places[2]


    def find_politics(paper_num):
        all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

        all_headline_string = ""

        for i in all_headlines: 
            all_headline_string += " " + i['headline']


        import nltk
        from nltk import FreqDist
        from nltk.corpus import stopwords
        stopword = stopwords.words('english')
        text = all_headline_string
        word_tokens = nltk.word_tokenize(text.lower())
        removing_stopwords = [word for word in word_tokens if word not in stopword]
        freq = FreqDist(removing_stopwords)
        most_common = freq.most_common(300)

        list_of_top_words = []

        for i in most_common: 
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            list_of_top_words.append(interlist)


        exceptions = [ 'worse', 'warning',  'stone', 'georgia', 'worse', 'run', 'past',    'wife', 'jail', 'gutfeld', 'fbi', 'mom', 'due', 'schumer', 'game',  'street', 'outbreaks',   'reacts', 'daughter', 'graham', 'responds',  'cnn', 'doj', 'mccarthy', 'calling', 'explains',   'dc',  'gingrich', 'vp', 'impact', '&', 'speech', 'mcenany', 'law', "–",   'pence', 'clinton', 'cdc', 'announces', 'issues', 'nfl', 'massive', 'comments', 'owner', 'event',    'since','japan', 'harry', 'mental', 'delhi',  'aged', 'judge', 'london',  'australian', 'abuse', 'theme', 'suspect', 'media', 'turkey', 'brazil', 'arrest',  'italian', 'tracking', 'denies', 'israel', 'french',  'boy', 'symptoms', "'" , "'s", "afghan", 'eu', "n't", "visual", 'isolation',    'distancing', 'saved', 'german', 'boss', 'australia', 'four', 'ca', 'baby',   'england', 'photo', 'sea', 'passes', 'row', 'indian', 'orders', 'ways',  '...', 'begins', 'vote', 'jailed', "'my", 'minister', "'ve", 'reopens', 'largest',     'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app', 'storm', 'returns',     'finally', 'c.d.c',  'donald',  'tech', "‘", 'debate', 'w.h.o',   ".", ":", "schools", "?", "’", "," , 'summer',   'billion', 'trial',  'hot', 'defense', 'hospitals', 'control', 'facing',  'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became',  'better', 'mike','coronavirus', 'trump', 'us', 'new', 'virus', 'says', 'biden', 'china', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.',  'amid', 'york', 'death', 'america', 'sanders', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'state', 'man', 'news', '$', 'black', 'outbreak', 'people', 'city', 'back', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'americans', 'white', 'floyd', '2020', 'take', 'life', 'time', 'updates', 'report', 'get', 'calls', 'fight', 'help', '-', 'dr.', 'states', 'global', 'dies', 'response', 'day', 'say', 'george', 'case', 'american', 'week', 'bill', ';', 'deaths', 'face', 'like',  'top', 'bloomberg', 'see', 'claims', 'race', 'court', 'super', 'big', 'bbc', 'dead', 'test', 'show', 'india', 'iowa', 'make', 'want', 'reopen', 'still', 'live', 'obama', 'found', 'go', 'flynn', 'would', 'quarantine', 'masks', 'south', 'work', 'need', 'california', 'plan', 'reopening', 'best', 'toll', 'vaccine', 'deal', 'travel', 'italy', 'spread', 'woman', 'women', 'killed', 'end', 'warns', 'last', 'years', 'behind', 'care', 'country', 'protest', 'russia', 'know', 'video', 'family', 'attack', 'quiz',  'going', 'fears', 'star', 'two', 'inside', 'pictures', 'next', 'former', 'service', 'pelosi', 'covid', 'follow', 'business', 'children', "'we", 'murder', 'stop', 'chief', 'national', 'testing', 'set', 'warren', 'hospital', 'ahead', 'primary', 'tells', 'party', 'justice', 'shooting', 'europe', 'briefing', 'much', '2', '3', 'tv', 'days', 'korea', 'iran', 'win', 'mass', 'free', 'bowl', 'call', 'history', 'million', 'social', 'aid', 'lives', 'order', 'hits', 'five', 'many', 'michael', 'tucker', 'hannity', 'faces', 'cuomo', 'rise', 'weekend', 'times', 'watch', 'fox', 'fear', 'three', 'right', 'hong', 'kong', 'florida', 'supreme', 'chinese', 'doctor', 'charged', 'force', 'governor', 'takes', 'change', 'record', 'exclusive', 'buttigieg', 'stimulus', 'public', 'facebook', 'bolton', 'listen', 'twitter', 'hit', 'open', 'story', 'official', 'good', 'despite', 'leader', 'mother', 'tuesday', 'year', 'never', 'gives',  'john', 'military', 'way', 'arrested', 'spreads', 'online', 'radio', 'got', 'reveals', 'save', 'stay', 'slams', 'africa', 'job', 'wants', 'texas', 'away', 'oil', 'ny', 'barr', 'relief', 'markets', 'return', 'must', 'making', 'gets', 'long', 'start', 'rules', 'even', 'fall', 'fire', 'bryant', 'makes', 'look', 'latest', 'ban', 'risk', 'doctors', 'surge', 'use', 'food', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'russian', '11', 'federal', 'restrictions', 'cut', 'headlines', 'team', 'key', 'missing', 'kobe', 'probe', 'guide', 'mask', "'the", 'amazon', 'another', 'presidential', 'system', 'think', 'blasts', 'political', 'minneapolis', 'wuhan', 'reports', 'wins', 'lost', 'students', 'mark', 'move', 'kids', 'countries', 'changed', 'close', 'pm', 'shot', 'cities', 'safe', 'medical', 'study', 'seattle', 'made', 'ever', 'ship', 'threat', 'analysis', 'young', 'find', 'france', 'weinstein', 'across', 'racism', 'die', 'patients', 'around', 'spain', 'goes', 'everything', 'wrong', 'aoc', 'real', 'washington', 'matter', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'died', 'deadly', 'left', 'experts', 'come', 'market', 'possible', 'point', 'johnson', 'mean', 'worst', 'results', 'drug', 'north', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'second', 'mr.', 'chris', 'administration', 'cops', 'wall', 'really', 'might', 'hampshire', 'jobs', 'de', 'germany', 'night', 'memorial', 'stocks', 'cathedral', 'businesses', 'nation', 'small', 'months', 'son', 'near', 'major', 'tom', 'trying', 'problem', 'coming', 'let', 'newt', 'blasio', 'sign', 'turn', 'give', 'elizabeth', '4', 'seen', 'action', 'plans', 'west', 'father', 'secret', 'candidate', 'sick', 'prison', 'carolina', 'message', 'reads', 'patrick', 'secretary', 'union', '!', 'canada', 'tweet', 'caucuses', 'meghan', 'crash', 'taking', 'things', 'stars', 'couple', 'needs', 'school', 'power', 'staff', 'hope', 'violence', 'access', 'fauci', 'unrest', 'pompeo', 'clash', '“', '”', 'far', 'girl', 'leaves', 'questions', 'six', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'fighting', "'re", 'money', '1', 'officer', 'claim', 'release', 'without', 'siegel', 'church', 'concerns']


        top_words = []



        for i in list_of_top_words:
            if i[0] not in exceptions:
                interlist = []
                interlist.append(i[0])
                interlist.append(i[1])
                top_words.append(interlist)





        overall_words = []
        for i in top_words: 
            overall_words.append(i)



        for i in overall_words:
            paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
            i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





        best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
        worst_words = sorted(overall_words, key = lambda x: x[2],)

        best_and_worst = []
        best_and_worst.append(best_words)
        best_and_worst.append(worst_words[:20])
        best_and_worst.append(exceptions)

        return best_and_worst

    nyt_politics = find_politics(1)
    bbc_politics = find_politics(2)
    fn_politics = find_politics(3)

    nyt_politics_words = nyt_politics[0]
    bbc_politics_words = bbc_politics[0]
    fn_politics_words = fn_politics[0]
    politics_exceptions = nyt_politics[2]

    def find_economic(paper_num):
        all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

        all_headline_string = ""

        for i in all_headlines: 
            all_headline_string += " " + i['headline']


        import nltk
        from nltk import FreqDist
        from nltk.corpus import stopwords
        stopword = stopwords.words('english')
        text = all_headline_string
        word_tokens = nltk.word_tokenize(text.lower())
        removing_stopwords = [word for word in word_tokens if word not in stopword]
        freq = FreqDist(removing_stopwords)
        most_common = freq.most_common(300)

        list_of_top_words = []

        for i in most_common: 
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            list_of_top_words.append(interlist)


        exceptions = [ 'warning', 'crime', 'georgia', 'stone', 'worse', 'democrat', 'run', 'jail', 'gutfeld', 'nypd', 'fbi', 'mom', 'due', 'schumer', 'game',  'calling', 'explains', 'reacts', 'daughter', 'graham', 'responds', 'wife',   'speech', '&', 'impact', 'vp', 'claim', 'gingrich', 'cnn', 'mccarthy',  'massive', 'comments', 'owner', 'siegel', 'dc', "–", 'mcenany',    'pence', 'concerns', 'clinton', 'cdc', 'announces', 'issues', 'nfl',  'since', 'mental', 'delhi',  'suspect', 'turkey', 'brazil', 'arrest', 'aged', 'london', 'japan', 'harry',  'tracking', 'denies', 'israel', 'french', 'australian', 'abuse', 'theme',  'italian', 'tracking', 'denies',   'boy', 'symptoms', "'",  "'s", 'afghan', 'eu', "n't", 'visual', 'isolation',   'ways', 'distancing', 'saved', 'german', 'boss', 'australia', 'four', 'ca', 'baby',   'reopens', 'largest', 'england', 'photo', 'sea', 'passes', 'row', 'indian',   '...', 'begins', 'jailed', "'my", 'minister', 'queen', "'ve", 'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app', 'storm', 'returns',   'g.o.p', 'street', 'outbreaks',   'schools', '?', 'job', "’",",", 'summer',"‘", 'w.h.o', 'donald', 'c.d.c', 'finally',     'politics', 'hot', 'defense', 'control', 'facing', '.', 'without', ':',   'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became',    'coronavirus', 'trump', 'us', 'new', 'virus', 'says', 'biden', 'china', 'police', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.', 'president', 'amid', 'death', 'york', 'america', 'sanders', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'man', 'state', 'black', 'news', 'outbreak', 'people', 'back', 'city', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'democrats', 'white', 'americans', 'floyd', '2020', 'media', 'take', 'life', 'updates', 'time', 'protests', 'report', 'get', 'calls', 'fight', 'help', 'day', 'dies', 'american', '-', 'dr.', 'say', 'global', 'states', 'response', 'case', 'george', 'week', ';', 'bill', 'like', 'face', 'deaths', 'campaign', 'dems', 'see', 'top', 'bloomberg', 'court', 'race', 'claims', 'dead', 'super', 'big', 'judge', 'bbc', 'test', 'protesters', 'show', 'make', 'india', 'iowa', 'want', 'reopen', 'still', 'live', 'masks', 'found', 'go', 'obama', 'would', 'south', 'flynn', 'election', 'quarantine', 'work', 'need', 'democratic', 'vote', 'rep.', 'california', 'gov', 'best', 'sen.', 'rally', 'reopening', 'trial', 'killed', 'plan', 'toll', 'mayor', 'woman', 'women', 'law', 'vaccine', 'deal', 'years', 'travel', 'end', 'care', 'italy', 'spread', 'impeachment', 'warns', 'last', 'behind', 'debate', 'country', 'protest', 'quiz', 'know', 'attack', 'russia', 'video', 'family', 'star', 'war', 'senate', 'service', 'two', 'officials', 'going', 'pictures', 'next', 'covid', 'follow', 'fears', 'former', 'inside', 'voters', 'pelosi', 'national', 'children', 'chief', 'ahead', "'we", 'murder', 'stop', 'justice', 'testing', 'set', 'warren', 'tells', 'hospital', 'primary', 'win', 'party', 'shooting', '2', '3', 'tv', 'europe', 'briefing', 'much', 'history', 'days', 'korea', 'weekend', 'iran', 'dem', 'many', 'mass', 'free', 'lives', 'order', 'bowl', 'hits', 'call', 'supreme', 'million', 'social', 'michael', 'aid', 'five', 'tucker', 'rise', 'times', 'hong', 'kong', 'florida', 'chinese', 'hannity', 'faces', 'cuomo', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'record', 'doctor', 'charged', 'force', 'governor', 'story', 'takes', 'change', 'exclusive', 'buttigieg', 'public', 'gives', 'facebook', 'gop', 'bolton', 'listen', 'military', 'official', 'away', 'twitter', 'hit', 'open', 'year', 'never', 'way', 'good', 'despite', 'leader', 'mother', 'tuesday', 'john', 'arrested', 'spreads', 'online', 'radio', 'texas', 'got', 'reveals', 'save', 'start', 'stay', 'return', 'slams', 'africa', 'wants', 'ny', '11', 'barr', 'relief', 'must', 'making', 'makes', 'gets', 'long', 'rules', 'even', 'food', 'headlines', 'fall', 'fire', 'bryant', 'look', 'latest', 'ban', 'mask', 'risk', 'russian', 'doctors', 'presidential', 'surge', 'system', 'use', 'security', 'battle', 'killing', 'push', 'emergency', 'another', 'cities', 'think', 'safe', 'blasts', 'federal', 'restrictions', 'cut', 'seattle', 'made', 'team', 'reports', 'key', 'missing', 'lost', 'kobe', '4', 'move', 'probe', 'guide', 'countries', "'the", 'amazon', 'shot', 'racism', 'political', 'minneapolis', 'wuhan', 'wins', 'students', 'threat', 'left', 'mark', 'kids', 'changed', 'close', 'pm', 'medical', 'study', 'around', 'spain', 'ever', 'ship', 'wrong', 'analysis', 'young', 'find', 'washington', 'france', 'government', 'weinstein', 'across', 'die', 'patients', 'goes', 'everything', 'deadly', 'aoc', 'real', 'west', 'experts', 'matter', 'johnson', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'nation', 'died', 'son', 'come', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'night', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'months', 'second', 'mr.', 'chris', 'administration', 'father', 'needs', 'cops', 'major', 'wall', 'problem', 'really', 'might', 'hampshire', 'newt', 'jobs', 'de', 'germany', 'turn', 'message', 'memorial', 'cathedral', 'reads', 'businesses', 'give', '!', 'small', 'plans', 'event', 'near', 'secret', 'tom', 'trying', 'staff', 'coming', 'let', 'carolina', 'blasio', 'sign', 'unrest', 'secretary', 'elizabeth', 'union', 'seen', 'action', 'candidate', 'sick', 'church', 'prison', 'doj', 'patrick', '“', '”', 'canada', 'past', 'girl', 'leaves', 'tweet', 'caucuses', 'questions', 'meghan', 'crash', 'six', 'taking', 'things', 'stars', 'couple', 'congress', 'school', 'orders', '1', 'power', 'hospitals', 'hope', 'violence', 'access', 'fauci', 'mike', 'pompeo', 'clash', 'far', 'better', 'andrew', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'tech', 'fighting']


        top_words = []



        for i in list_of_top_words:
            if i[0] not in exceptions:
                interlist = []
                interlist.append(i[0])
                interlist.append(i[1])
                top_words.append(interlist)





        overall_words = []
        for i in top_words: 
            overall_words.append(i)



        for i in overall_words:
            paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
            i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





        best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
        worst_words = sorted(overall_words, key = lambda x: x[2],)

        best_and_worst = []
        best_and_worst.append(best_words)
        best_and_worst.append(worst_words[:20])
        best_and_worst.append(exceptions)

        return best_and_worst

    nyt_economic = find_economic(1)
    bbc_economic = find_economic(2)
    fn_economic = find_economic(3)

    nyt_economic_words = nyt_economic[0]
    bbc_economic_words = bbc_economic[0]
    fn_economic_words = fn_economic[0]
    economics_exceptions = nyt_economic[2] 
   
    def find_corona(paper_num):
        all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

        all_headline_string = ""

        for i in all_headlines: 
            all_headline_string += " " + i['headline']


        import nltk
        from nltk import FreqDist
        from nltk.corpus import stopwords
        stopword = stopwords.words('english')
        text = all_headline_string
        word_tokens = nltk.word_tokenize(text.lower())
        removing_stopwords = [word for word in word_tokens if word not in stopword]
        freq = FreqDist(removing_stopwords)
        most_common = freq.most_common(300)

        list_of_top_words = []

        for i in most_common: 
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            list_of_top_words.append(interlist)


        exceptions = [ 'warning',  'crime', 'georgia', 'worse', 'run', 'democrat',   'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app', 'storm', 'returns', '', '...', 'begins', 'jailed', "", "'my", 'queen', "'ve", 'largest', 'england', 'photo', 'sea', 'passes', 'row', 'indian', 'ways', 'saved', 'german', 'boss', 'minister', 'australia', 'four', 'ca', 'baby', 'boy', "'", "'s", 'afghan', 'eu', "n't", 'visual', 'denies', 'music', 'israel', 'french', 'australian', 'abuse', 'theme', 'suspect', 'turkey', 'brazil', 'arrest', 'aged', 'london', 'japan', 'harry', 'since', 'mental', 'delhi', 'concerns', 'clinton', 'announces', 'issues', 'nfl', 'comments', 'owner', 'siegel', 'dc',  '–', 'mcenany', 'speech', '&', 'impact', 'vp', 'claim', 'gingrich', 'accused', 'cnn', 'mccarthy', 'calling', 'explains', 'reacts', 'daughter', 'graham', 'officer', 'responds', 'wife', 'jail', 'gutfeld', 'nypd', 'fbi', 'mom', 'due', 'schumer', 'game',    'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became', 'money', 'politics', 'hot', 'defense', 'control', 'without', 'facing', 'billion', '.', ':', '’', '?', ",", 'summer', "‘", 'schools', 'finally', 'street', 'g.o.p', 'stone',   'us', 'new', 'says', 'biden', 'china', 'police', 'world', 'u.s.', 'president', 'amid', 'death', 'york', 'america', 'sanders', 'could', 'crisis', 'uk', 'home', 'house', 'man', 'state', 'black', 'news', 'people', '$', 'back', 'city', 'one', 'joe',  'may', 'first', 'bernie', 'democrats', 'white', 'americans', 'floyd', '2020', 'media', 'take', 'life', 'updates', 'time', 'protests', 'report', 'get', 'calls', 'fight', 'help', 'day', 'dies', 'american', '-', 'dr.', 'say', 'global', 'states', 'response', 'case', 'george', 'week', ';', 'bill', 'like', 'face', 'deaths', 'workers', 'campaign', 'dems', 'see', 'top', 'bloomberg', 'court', 'race', 'claims', 'economy', 'dead', 'super', 'big', 'judge', 'bbc', 'test', 'protesters', 'show', 'make', 'india', 'iowa', 'want', 'still', 'live', 'found', 'go', 'obama', 'would', 'south', 'flynn', 'election', 'work', 'need', 'democratic', 'vote', 'rep.', 'california', 'gov', 'best', 'sen.', 'rally', 'trial', 'killed', 'plan', 'toll', 'mayor', 'woman', 'women', 'law',  'deal', 'years', 'travel', 'end', 'care', 'italy', 'impeachment', 'warns', 'last', 'behind', 'debate', 'country', 'protest', 'quiz', 'know', 'attack', 'russia', 'video', 'family', 'star', 'war', 'senate', 'service', 'two', 'officials', 'going', 'pictures', 'next', 'follow', 'fears', 'former', 'inside', 'voters', 'pelosi', 'national', 'children', 'chief', 'ahead', 'business', "'we", 'murder', 'stop', 'justice', 'set', 'warren', 'tells', 'primary', 'win', 'party', 'shooting', '2', '3', 'tv', 'europe', 'briefing', 'much', 'economic', 'history', 'days', 'korea', 'weekend', 'iran', 'dem', 'many', 'mass', 'free', 'lives', 'order', 'bowl', 'hits', 'call', 'supreme', 'million', 'social', 'michael', 'aid', 'five', 'tucker', 'rise', 'times', 'hong', 'kong', 'florida', 'chinese', 'hannity', 'faces', 'cuomo', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'record', 'doctor', 'charged', 'force', 'governor', 'story', 'takes', 'change', 'exclusive', 'buttigieg', 'stimulus', 'public', 'gives', 'facebook', 'gop', 'bolton', 'listen', 'military', 'official', 'away', 'twitter', 'hit', 'open', 'year', 'never', 'way', 'good', 'despite', 'leader', 'mother', 'tuesday', 'john', 'arrested', 'online', 'radio', 'texas', 'got', 'reveals', 'save', 'start', 'stay', 'return', 'slams', 'africa', 'job', 'wants', 'oil', 'ny', '11', 'barr', 'relief', 'markets', 'must', 'making', 'makes', 'gets', 'long', 'rules', 'even', 'food', 'headlines', 'fall', 'fire', 'bryant', 'look', 'latest', 'ban', 'risk', 'russian', 'doctors', 'presidential', 'surge', 'system', 'use', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'another', 'cities', 'think', 'safe', 'blasts', 'federal', 'restrictions', 'cut', 'seattle', 'made', 'team', 'reports', 'key', 'missing', 'lost', 'kobe', '4', 'move', 'probe', 'guide', 'countries', "'the", 'amazon', 'shot', 'racism', 'political', 'minneapolis', 'wins', 'students', 'threat', 'left', 'mark', 'kids', 'changed', 'close', 'pm', 'medical', 'study', 'around', 'spain', 'ever', 'ship', 'wrong', 'analysis', 'young', 'find', 'washington', 'france', 'government', 'weinstein', 'across', 'die', 'goes', 'everything', 'deadly', 'aoc', 'real', 'west', 'experts', 'matter', 'johnson', 'reform', 'said', 'nevada', 'attacks', 'kill',  'bad', 'nyc', 'nation', 'died', 'son', 'come', 'market', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'night', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'months', 'second', 'mr.', 'chris', 'administration', 'father', 'needs', 'cops', 'major', 'wall', 'problem', 'really', 'might', 'hampshire', 'newt', 'jobs', 'de', 'germany', 'turn', 'message', 'memorial', 'stocks', 'cathedral', 'reads', 'businesses', 'give', '!', 'small', 'plans', 'event', 'near', 'secret', 'tom', 'trying', 'staff', 'coming', 'let', 'carolina', 'blasio', 'sign', 'unrest', 'secretary', 'elizabeth', 'union', 'seen', 'action', 'candidate', 'sick', 'church', 'prison', 'doj', 'patrick', '“', '”', 'canada', 'past', 'girl', 'leaves', 'tweet', 'caucuses', 'questions', 'meghan', 'crash', 'six', 'taking', 'things', 'stars', 'couple', 'congress', 'school', 'orders', '1', 'power', 'hope', 'violence', 'access', 'mike', 'pompeo', 'clash', 'far', 'better', 'andrew', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'tech', 'fighting']


        top_words = []



        for i in list_of_top_words:
            if i[0] not in exceptions:
                interlist = []
                interlist.append(i[0])
                interlist.append(i[1])
                top_words.append(interlist)





        overall_words = []
        for i in top_words: 
            overall_words.append(i)



        for i in overall_words:
            paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
            i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





        best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
        worst_words = sorted(overall_words, key = lambda x: x[2],)

        best_and_worst = []
        best_and_worst.append(best_words)
        best_and_worst.append(worst_words[:20])
        best_and_worst.append(exceptions)

        return best_and_worst

    nyt_corona = find_corona(1)
    bbc_corona = find_corona(2)
    fn_corona = find_corona(3)

    nyt_corona_words = nyt_corona[0]
    bbc_corona_words = bbc_corona[0]
    fn_corona_words = fn_corona[0]
    corona_exceptions = nyt_corona[2]


    def find_rp(paper_num):
        all_headlines = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).values('headline')

        all_headline_string = ""

        for i in all_headlines: 
            all_headline_string += " " + i['headline']


        import nltk
        from nltk import FreqDist
        from nltk.corpus import stopwords
        stopword = stopwords.words('english')
        text = all_headline_string
        word_tokens = nltk.word_tokenize(text.lower())
        removing_stopwords = [word for word in word_tokens if word not in stopword]
        freq = FreqDist(removing_stopwords)
        most_common = freq.most_common(300)

        list_of_top_words = []

        for i in most_common: 
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            list_of_top_words.append(interlist)


        exceptions = [  'democrat', 'run', 'warning',  'georgia', 'distancing', 'worse',   'announces', 'issues', 'nfl', 'comments', 'owner',  'siegel', 'dc', "–", 'mcenany', 'speech', '&', 'impact', 'vp', 'claim', 'gingrich', 'accused', 'cnn', 'mccarthy', 'calling', 'explains', 'reacts', 'daughter', 'graham', 'responds', 'wife', 'gutfeld', 'mom', 'due', 'schumer', 'game', 'pence', 'concerns', 'clinton', 'cdc',  'shots', 'huge', 'tips', 'rare', 'birthday', 'putin', 'app', 'storm', 'returns', '...', 'begins', 'jailed', "'my", 'queen', "'ve", 'largest', 'england', 'photo', 'sea', 'passes', 'row', 'indian', 'ways', 'saved', 'german', 'boss', 'minister', 'australia', 'four', 'ca', 'baby', 'boy', 'symptoms', "'" , "'s", 'afghan', 'eu', "n't", 'visual', 'isolation', 'italian', 'tracking', 'denies', 'music', 'israel', 'french', 'australian', 'abuse', 'theme', 'suspect', 'turkey', 'brazil', 'aged', 'london', 'japan', 'harry', 'since', 'mental', 'delhi',  'coverage', 'providing', 'love', 'read', '(', ')', 'already', 'became', 'money', 'politics', 'hot', 'defense', 'control', 'without', 'facing', 'billion', '.', ':', "’", '?', ",", 'summer' , "‘", 'schools', 'w.h.o', 'c.d.c', 'finally', 'street', 'g.o.p', 'outbreaks', 'stone',    'coronavirus', 'us', 'new', 'virus', 'says', 'biden', 'china', 'covid-19', 'pandemic', 'lockdown', 'world', 'u.s.', 'president', 'amid', 'death', 'york', 'america', 'sanders', 'could', 'crisis', 'cases', 'uk', 'home', 'house', 'man', 'state', 'news', 'outbreak', 'people', '$', 'back', 'city', 'one', 'joe', 'health', 'may', 'first', 'bernie', 'democrats', 'americans', '2020', 'media', 'take', 'life', 'updates', 'time', 'report', 'get', 'calls', 'fight', 'help', 'day', 'dies', 'american', '-', 'dr.', 'say', 'global', 'states', 'response', 'case', 'george', 'week', ';', 'bill', 'like', 'face', 'deaths', 'workers', 'campaign', 'dems', 'see', 'top', 'bloomberg', 'court', 'race', 'claims', 'economy', 'dead', 'super', 'big', 'judge', 'bbc', 'test', 'show', 'make', 'india', 'iowa', 'want', 'reopen', 'still', 'live', 'masks', 'found', 'go', 'obama', 'would', 'south', 'flynn', 'election', 'quarantine', 'work', 'need', 'democratic', 'vote', 'rep.', 'california', 'gov', 'best', 'sen.', 'reopening', 'trial', 'killed', 'plan', 'toll', 'mayor', 'woman', 'women', 'law', 'vaccine', 'deal', 'years', 'travel', 'end', 'care', 'italy', 'spread', 'impeachment', 'warns', 'last', 'behind', 'debate', 'country', 'protest', 'quiz', 'know', 'attack', 'russia', 'video', 'family', 'star', 'war', 'senate', 'service', 'two', 'officials', 'going', 'pictures', 'next', 'covid', 'follow', 'fears', 'former', 'inside', 'voters', 'pelosi', 'national', 'children', 'chief', 'ahead', 'business', "'we", 'murder', 'stop', 'testing', 'set', 'warren', 'tells', 'hospital', 'primary', 'win', 'party', 'shooting', '2', '3', 'tv', 'europe', 'briefing', 'much', 'economic', 'history', 'days', 'korea', 'weekend', 'iran', 'dem', 'many', 'mass', 'free', 'lives', 'order', 'bowl', 'hits', 'call', 'supreme', 'million', 'social', 'michael', 'aid', 'five', 'tucker', 'rise', 'times', 'hong', 'kong', 'florida', 'chinese', 'hannity', 'faces', 'cuomo', 'republicans', 'watch', 'fox', 'fear', 'three', 'right', 'record', 'doctor', 'charged', 'force', 'governor', 'story', 'takes', 'change', 'exclusive', 'buttigieg', 'stimulus', 'public', 'gives', 'facebook', 'gop', 'bolton', 'listen', 'military', 'official', 'away', 'twitter', 'hit', 'open', 'year', 'never', 'way', 'good', 'despite', 'leader', 'mother', 'tuesday', 'john', 'arrested', 'spreads', 'online', 'radio', 'texas', 'got', 'reveals', 'save', 'start', 'stay', 'return', 'slams', 'africa', 'job', 'wants', 'oil', 'ny', '11', 'barr', 'relief', 'markets', 'must', 'making', 'makes', 'gets', 'long', 'rules', 'even', 'food', 'headlines', 'fall', 'fire', 'bryant', 'look', 'latest', 'ban', 'mask', 'risk', 'russian', 'doctors', 'presidential', 'surge', 'system', 'use', 'security', 'battle', 'killing', 'push', 'stock', 'emergency', 'another', 'cities', 'think', 'safe', 'blasts', 'federal', 'restrictions', 'cut', 'seattle', 'made', 'team', 'reports', 'key', 'missing', 'lost', 'kobe', '4', 'move', 'probe', 'guide', 'countries', "'the", 'amazon', 'shot', 'political', 'minneapolis', 'wuhan', 'wins', 'students', 'threat', 'left', 'mark', 'kids', 'changed', 'close', 'pm', 'medical', 'study', 'around', 'spain', 'ever', 'ship', 'wrong', 'analysis', 'young', 'find', 'washington', 'france', 'government', 'weinstein', 'across', 'die', 'patients', 'goes', 'everything', 'deadly', 'aoc', 'real', 'west', 'experts', 'matter', 'johnson', 'reform', 'said', 'nevada', 'attacks', 'kill', 'tests', 'bad', 'nyc', 'nation', 'died', 'son', 'come', 'market', 'possible', 'point', 'mean', 'worst', 'results', 'drug', 'north', 'night', 'sex', 'positive', 'daily', 'michigan', 'shows', 'cruise', 'great', 'college', 'months', 'second', 'mr.', 'chris', 'administration', 'father', 'needs',  'major', 'wall', 'problem', 'really', 'might', 'hampshire', 'newt', 'jobs', 'de', 'germany', 'turn', 'message', 'memorial', 'stocks', 'cathedral', 'reads', 'businesses', 'give', '!', 'small', 'plans', 'event', 'near', 'secret', 'tom', 'trying', 'staff', 'coming', 'let', 'carolina', 'blasio', 'sign', 'unrest', 'secretary', 'elizabeth', 'union', 'seen', 'action', 'candidate', 'sick', 'church', 'prison', 'doj', 'patrick', '“', '”', 'canada', 'past', 'girl', 'leaves', 'tweet', 'caucuses', 'questions', 'meghan', 'crash', 'six', 'taking', 'things', 'stars', 'couple', 'congress', 'school', 'orders', '1', 'power', 'hospitals', 'hope', 'violence', 'access', 'fauci', 'mike', 'pompeo', 'clash', 'far', 'better', 'andrew', 'today', 'wallace', 'pay', 'support', 'book', 'leaders', 'tech', 'fighting']


        top_words = []



        for i in list_of_top_words:
            if i[0] not in exceptions:
                interlist = []
                interlist.append(i[0])
                interlist.append(i[1])
                top_words.append(interlist)





        overall_words = []
        for i in top_words: 
            overall_words.append(i)



        for i in overall_words:
            paper_avg_sentiment_for_i = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
            i.append(round(paper_avg_sentiment_for_i[0]['Average']*100,2))





        best_words = sorted(overall_words, key = lambda x: x[2], reverse=True)
        worst_words = sorted(overall_words, key = lambda x: x[2],)

        best_and_worst = []
        best_and_worst.append(best_words)
        best_and_worst.append(worst_words[:20])
        best_and_worst.append(exceptions)

        return best_and_worst

    nyt_rp = find_rp(1)
    bbc_rp = find_rp(2)
    fn_rp = find_rp(3)

    nyt_rp_words = nyt_rp[0]
    bbc_rp_words = bbc_rp[0]
    fn_rp_words = fn_rp[0]
    rp_exceptions = nyt_rp[2]

    def variance_variables(papernum1, papernum2):

        def total_variance_avg_sentiment_day(newspaper):
            newspaper1data = Headline.objects.filter(day_order__lte=25).filter(newspaper=newspaper).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
            
            newspaper1x = []
            for i in newspaper1data:
                newspaper1x.append(i['Date'])
            
            newspaper1y = []
            for i in newspaper1data:
                newspaper1y.append(round(i['Average']*100,2))
            
            newspaperxy = []

            newspaperxy.append(newspaper1x)
            newspaperxy.append(newspaper1y)
        
            return newspaperxy

        nyt_avg_sent = total_variance_avg_sentiment_day(papernum1)
        fn_avg_sent = total_variance_avg_sentiment_day(papernum2)

        start_index = len(nyt_avg_sent[0]) - 30
        end_index = len(nyt_avg_sent[0])

        paper_color1 = ''
        paper_color2 = ''

        if papernum1 == 1:
            paper_color1 = '#8e949e'
        elif papernum1 == 2:
            paper_color1 = '#bb1919'
        elif papernum1 == 3:
            paper_color1 = '#006edb'
        
        if papernum2 == 1:
            paper_color2 = '#8e949e'
        elif papernum2 == 2:
            paper_color2 ='#bb1919'
        elif papernum2 == 3:
            paper_color2 =  '#006edb'




        fig_var_sent_nyt_fn =  go.Figure()
        fig_var_sent_nyt_fn.add_trace(go.Scatter(x=nyt_avg_sent[0][start_index:end_index], y=nyt_avg_sent[1][start_index:end_index], 
            fill=None,
            mode='lines',
            line_color=paper_color1
            ))
        fig_var_sent_nyt_fn.add_trace(go.Scatter(
            x=fn_avg_sent[0][start_index:end_index],
            y=fn_avg_sent[1][start_index:end_index],
            fill='tonexty',
            mode='lines', line_color=paper_color2,
        ))

        fig_var_sent_nyt_fn.update_layout(
            font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0),showlegend=False, height=300 )


        html_div_fig_nyt_fn = str(plotly.offline.plot(fig_var_sent_nyt_fn, output_type='div',config = {'displayModeBar': False},))

        
        variance_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum1).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Average=Avg('sentiment'))

        variance_fn = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum2).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Average=Avg('sentiment'))


        
        
        
        nyt_sentiment_by_day = []

        for i in variance_nyt:
            nyt_sentiment_by_day.append(i['Average']*100)
        
        fn_sentiment_by_day = []

        for i in variance_fn:
            fn_sentiment_by_day.append(i['Average']*100)
        
        fn_nyt_variance_by_day = []

        for i in range(0, len(nyt_sentiment_by_day)):
            day_variance = abs(nyt_sentiment_by_day[i] - fn_sentiment_by_day[i])
            fn_nyt_variance_by_day.append(day_variance)
        
        
        
        fn_nyt_sum_variance = 0

        for i in fn_nyt_variance_by_day:
            fn_nyt_sum_variance += i 
        
        fn_nyt_average_variance = round(fn_nyt_sum_variance/len(nyt_sentiment_by_day),1)

        return_variables = []

        return_variables.append(html_div_fig_nyt_fn)
        return_variables.append(fn_nyt_average_variance)
        return_variables.append(fn_nyt_sum_variance)

        return return_variables
    

    variance_variables_output_nyt_fn = variance_variables(1,3)
    variance_variables_output_nyt_bbc = variance_variables(1,2)
    variance_variables_output_fn_bbc = variance_variables(3,2)



    html_div_fig_nyt_fn = variance_variables_output_nyt_fn[0]
    fn_nyt_average_variance = variance_variables_output_nyt_fn[1]
    fn_nyt_sum_variance = variance_variables_output_nyt_fn[2]

    html_div_fig_nyt_bbc = variance_variables_output_nyt_bbc[0]
    bbc_nyt_average_variance = variance_variables_output_nyt_bbc[1]
    bbc_nyt_sum_variance = variance_variables_output_nyt_bbc[2]

    html_div_fig_fn_bbc = variance_variables_output_fn_bbc[0]
    fn_bbc_average_variance = variance_variables_output_fn_bbc[1]
    fn_bbc_sum_variance = variance_variables_output_fn_bbc[2]


    all_headlines = Headline.objects.filter(day_order__lte=25).values('headline')

    all_headline_string = ""

    for i in all_headlines: 
        all_headline_string += " " + i['headline']


    import nltk
    from nltk import FreqDist
    from nltk.corpus import stopwords
    stopword = stopwords.words('english')
    text = all_headline_string
    word_tokens = nltk.word_tokenize(text.lower())
    removing_stopwords = [word for word in word_tokens if word not in stopword]
    freq = FreqDist(removing_stopwords)
    most_common = freq.most_common(500)

    list_of_top_words = []

    for i in most_common: 
        interlist = []
        interlist.append(i[0])
        interlist.append(i[1])
        list_of_top_words.append(interlist)

   

    top_exceptions = [',', '’', ':', "'", '.', "'s", '?', '‘'  ]

    scrubbed_list = []

    for i in list_of_top_words:
        if i[0] not in top_exceptions:
            interlist = []
            interlist.append(i[0])
            interlist.append(i[1])
            scrubbed_list.append(interlist)
    
  

    for i in scrubbed_list:
        nyt_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
        if not nyt_sent:
            nyt_sent = [{'newspaper': 1, 'Average': 0}]


        bbc_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
        if not bbc_sent:
            bbc_sent = [{'newspaper': 2, 'Average': 0}]

        fn_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=i[0]).values('newspaper').annotate(Average=Avg('sentiment'))
        if not fn_sent:
            fn_sent = [{'newspaper': 3, 'Average': 0}]

        i.append(nyt_sent[0]['Average'] * 100)
        i.append(bbc_sent[0]['Average']* 100)
        i.append(fn_sent[0]['Average']*100)

        
  

    scrubbed_list_with_variances = []
    for i in scrubbed_list:
        nyt_fn_variance = round(i[2] - i[4],2)
        nyt_bbc_variance = round(i[2]- i[3],2)
        fn_bbc_variance = round(i[4] - i[3],2)
        
        nyt_check = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=i[0])
        bbc_check = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=i[0])
        fn_check = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=i[0])

        if nyt_check and fn_check: 
            i.append(nyt_fn_variance)
        else:
            i.append(0)

        if nyt_check and bbc_check:
            i.append(nyt_bbc_variance)
        else:
            i.append(0)
        
        if fn_check and bbc_check:
            i.append(fn_bbc_variance)
        else:
            i.append(0)
    
    

    master_word_variance = []


    for i in scrubbed_list:
        nyt_fn = []
        nyt_fn.append(i[0])
        nyt_fn.append(i[1])
        nyt_fn.append('NYT')
        nyt_fn.append('FN')
        nyt_fn.append(i[5])
        master_word_variance.append(nyt_fn)
        nyt_bbc = []
        nyt_bbc.append(i[0])
        nyt_bbc.append(i[1])
        nyt_bbc.append('NYT')
        nyt_bbc.append('BBC')
        nyt_bbc.append(i[6])
        master_word_variance.append(nyt_bbc)
        fn_bbc = []
        fn_bbc.append(i[0])
        fn_bbc.append(i[1])
        fn_bbc.append('FN')
        fn_bbc.append('BBC')
        fn_bbc.append(i[7])
        master_word_variance.append(fn_bbc)

  

    most_variance = sorted(master_word_variance, key = lambda x: abs(x[4]), reverse=True)
    

    most_variance_words = most_variance[:300]

    


    #do not rerun queries. filter most_variance with exception lists to find people, places, political, etc. 

    most_variance_people = []

    for i in most_variance_words:
        if i[0] not in people_exceptions:
            most_variance_people.append(i)
    
    most_variance_places = []

    for i in most_variance_words:
        if i[0] not in place_exceptions:
            most_variance_places.append(i)

    most_variance_politics = []

    for i in most_variance_words:
        if i[0] not in politics_exceptions:
            most_variance_politics.append(i)
    
    most_variance_economics = []

    for i in most_variance_words:
        if i[0] not in economics_exceptions:
            most_variance_economics.append(i)
    

    most_variance_corona = []
    for i in most_variance_words:
        if i[0] not in corona_exceptions:
            most_variance_corona.append(i)
    
    most_variance_rp = []
    for i in most_variance_words:
        if i[0] not in rp_exceptions:
            most_variance_rp.append(i)

    
    daily_sent_var_query_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
    daily_sent_var_query_bbc = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
    daily_sent_var_query_fn = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))

    
    all_sents_by_day = []
    
    for i in range(0,len(daily_sent_var_query_nyt)):
        interlist = []
        interlist.append(daily_sent_var_query_nyt[i]['Date'])
        interlist.append(round(daily_sent_var_query_nyt[i]['Average']*100,2))
        interlist.append(round(daily_sent_var_query_bbc[i]['Average']*100,2))
        interlist.append(round(daily_sent_var_query_fn[i]['Average']*100,2))
        all_sents_by_day.append(interlist)
    
    

    daily_variances = []

    for i in all_sents_by_day:
        interlist = []
        interlist.append(i[0])
        interlist.append('NYT')
        interlist.append('BBC')
        interlist.append(i[1] - i[2])
        interlist2 = []
        interlist2.append(i[0])
        interlist2.append('NYT')
        interlist2.append('FN')
        interlist2.append(i[1]-i[3])
        interlist3 = []
        interlist3.append(i[0])
        interlist3.append('FN')
        interlist3.append('BBC')
        interlist3.append(i[3]-i[2])
        daily_variances.append(interlist)
        daily_variances.append(interlist2)
        daily_variances.append(interlist3)

         

    most_variance_dates = sorted(daily_variances, key = lambda x: abs(x[3]), reverse=True)
    

        

    












    

    

    
    

   




    return render(request, 'custom_scraper/sentiment_compare.html', {'html_div_compare': html_div_compare, 'html_div_compare_month': html_div_compare_month, 'nytimes_cal': nytimes_cal, 'bbc_cal': bbc_cal, 'fn_cal': fn_cal, 'this_month':this_month, 'last_month': last_month, 'nytimes_cal_last': nytimes_cal_last, 'bbc_cal_last': bbc_cal_last, 'fn_cal_last': fn_cal_last, 'nyt_pie': nyt_pie, 'bbc_pie': bbc_pie, 'fn_pie': fn_pie, 'nyt_average_ytd': nyt_average_ytd, 'bbc_average_ytd': bbc_average_ytd, 'fn_average_ytd': fn_average_ytd, 'html_div_compare_month_pos': html_div_compare_month_pos, 'html_div_compare_month_neg': html_div_compare_month_neg, 'html_div_compare_month_neu': html_div_compare_month_neu, 'html_div_compare_dow_sent': html_div_compare_dow_sent, 'html_div_compare_hist_sent': html_div_compare_hist_sent, 'html_div_compare_sent_hr': html_div_compare_sent_hr, 'nyt_best_words': nyt_best_words, 'bbc_best_words': bbc_best_words, 'fn_best_words': fn_best_words, 'nyt_worst_words': nyt_worst_words, 'bbc_worst_words': bbc_worst_words, 'fn_worst_words': fn_worst_words, 'nyt_best_people': nyt_best_people, 'bbc_best_people': bbc_best_people, 'fn_best_people': fn_best_people, 'nyt_worst_people': nyt_worst_people, 'bbc_worst_people': bbc_worst_people, 'fn_worst_people': fn_worst_people, 'nyt_best_places': nyt_best_places, 'bbc_best_places': bbc_best_places, 'fn_best_places': fn_best_places, 'nyt_worst_places': nyt_worst_places, 'bbc_worst_places': bbc_worst_places, 'fn_worst_places': fn_worst_places, 'nyt_politics_words': nyt_politics_words, 'bbc_politics_words': bbc_politics_words, 'fn_politics_words': fn_politics_words, 'nyt_economic_words': nyt_economic_words, 'bbc_economic_words': bbc_economic_words, 'fn_economic_words': fn_economic_words, 'nyt_corona_words': nyt_corona_words, 'bbc_corona_words': bbc_corona_words, 'fn_corona_words': fn_corona_words, 'nyt_rp_words': nyt_rp_words, 'bbc_rp_words': bbc_rp_words, 'fn_rp_words': fn_rp_words, 'html_div_fig_nyt_fn': html_div_fig_nyt_fn, 'fn_nyt_average_variance': fn_nyt_average_variance,     'html_div_fig_nyt_bbc': html_div_fig_nyt_bbc, 'bbc_nyt_average_variance': bbc_nyt_average_variance, 'html_div_fig_fn_bbc': html_div_fig_fn_bbc, 'fn_bbc_average_variance': fn_bbc_average_variance, 'most_variance_words': most_variance_words, 'most_variance_people': most_variance_people, 'most_variance_places':most_variance_places, 'most_variance_politics': most_variance_politics, 'most_variance_economics': most_variance_economics, 'most_variance_corona': most_variance_corona, 'most_variance_rp': most_variance_rp, 'most_variance_dates': most_variance_dates })