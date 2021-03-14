from django.shortcuts import render
from django.utils import timezone
from .models import Headline
from .models import Headlinewrl
from .models import Headlinewc
from .models import Headline_emotion
from .models import top_words_emotions_tally
from .models import top_words_emotions_percent
from .models import hl_tokens_emotions
from custom_scraper.models import total_word_count
from custom_scraper.models import cooc
from .models import word_count_general
from .models import style_wc
from .models import cooc_wc
from .models import Headline_emotion
from .models import html_cache
# Create your views here.
from datetime import date, timedelta
from textblob import TextBlob
from .models import Photos
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import WordCountSearch
from .forms import SentimentWordSearch
from .forms import SentimentDateSearch
from .forms import DateForm
from .forms import CompareSearch1
from .forms import CompareSearch2
from .forms import CompareSearchSingle



from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models.functions import TruncDay
from django.db.models import Avg
import pandas as pd
import plotly.express as px
import plotly
from django.db.models.functions import TruncMonth
from django.db.models import CharField, Value
from django.http import HttpResponse








today = date.today()
yesterday = date.today() - timedelta(days=1)

def mainpage(request):

    today1 = today
    print(today)
    nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
    if not nytheadlines:
        print("not nyt")
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
        if keyword_counter < 6:
            all_wf_values.append(v[0])
            all_wf_keys.append(v[1])
        keyword_counter += 1

    key1 = all_wf_keys[0]
    freq1 = all_wf_values[0]
    key2 = all_wf_keys[1]
    freq2 = all_wf_values[1]
    key3 = all_wf_keys[2]
    freq3 = all_wf_values[2]
    key4 = all_wf_keys[3]
    freq4 = all_wf_values[3]
    key5 = all_wf_keys[4]
    freq5 = all_wf_values[4]
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




    form = DateForm()

    print(all_wf_keys)
    print(all_wf_values)


    from django.db.models import Sum

    daily_emotion = Headline_emotion.objects.filter(day_order__lte=25).filter(date__contains=today).values('anger', 'fear', 'anticip', 'trust', 'surprise', 'sadness', 'disgust', 'joy' )
    for i in daily_emotion:
        print(i)

    emotion_count_dict = {}
    emotion_count_dict['anger'] = 0
    emotion_count_dict['fear'] = 0
    emotion_count_dict['anticip'] = 0
    emotion_count_dict['trust'] = 0
    emotion_count_dict['surprise'] = 0
    emotion_count_dict['sadness'] = 0
    emotion_count_dict['disgust'] = 0
    emotion_count_dict['joy'] = 0

    for record in daily_emotion:
        if record['anger'] > 0:
            emotion_count_dict['anger'] += record['anger']
        if record['fear'] > 0:
            emotion_count_dict['fear'] += record['fear']
        if record['anticip'] > 0:
            emotion_count_dict['anticip'] += record['anticip']
        if record['trust'] > 0:
            emotion_count_dict['trust'] += record['trust']

        if record['surprise'] > 0:
            emotion_count_dict['surprise'] += record['surprise']
        if record['sadness'] > 0:
            emotion_count_dict['sadness'] += record['sadness']
        if record['disgust'] > 0:
            emotion_count_dict['disgust'] += record['disgust']
        if record['joy'] > 0:
            emotion_count_dict['joy'] += record['joy']


    list_of_emotions = []
    for key, value in emotion_count_dict.items():
        interlist = [key, value]
        list_of_emotions.append(interlist)

    print(list_of_emotions)

    sorted_list_of_emotions = sorted(list_of_emotions, key=lambda x: x[1],reverse=True)

    emotion_display = sorted_list_of_emotions[:3]

    print(sorted_list_of_emotions)

    return render(request, 'custom_scraper/mainpage.html', {'emotion_display':emotion_display, "nytheadlines":nytheadlines,"bbcheadlines":bbcheadlines,"fnheadlines":fnheadlines,"ny_score":ny_score, "bbc_score":bbc_score, "fn_score":fn_score, "overall_score":overall_score, "today1":today1,"allkeywords":allkeywords,"key1":key1,"key2":key2,"key3":key3, "key4":key4,"freq4":freq4, "key5":key5,"freq5":freq5, "freq1":freq1,"freq2":freq2,"freq3":freq3,  "nytheadlines":nytheadlines, "bbcheadlines":bbcheadlines, "fnheadlines":fnheadlines, "form":form,})

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
    if not search:
        current_time = datetime.datetime.now()

        today = current_time.strftime('%Y/%m/%d')
    else:
        today = search
    today_year = today[:4]
    today_date = today[8:]
    today_month = today[5:7]
    today = today_year + "-" + today_month + "-" + today_date
    header_date = datetime.datetime.strptime(today, '%Y-%m-%d').date()

    scraped = True
    nytheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=1).filter(day_order__lte=25)
    if not nytheadlines:
        scraped = False
        nytheadlines = ["No headlines for this date. Headlines record start Jan 25, 2020"]

    bbcheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=2).filter(day_order__lte=25)
    if not bbcheadlines:
        bbcheadlines = ["No headlines for this date. Headlines record start Jan 25, 2020"]

    fnheadlines = Headline.objects.filter(date__contains=today).filter(newspaper=3).filter(day_order__lte=25)
    if not fnheadlines:
        fnheadlines = ["No headlines for this date. Headlines record start Jan 25, 2020"]

    nyt_sentiment_score = Headline.objects.filter(date__contains=today).filter(newspaper=1)
    if not nyt_sentiment_score:
        nyt_sentiment_score = [{'sentiment':0}]

    bbc_sentiment_score = Headline.objects.filter(date__contains=today).filter(newspaper=2)
    if not bbc_sentiment_score:
        bbc_sentiment_score = [{'sentiment':0}]

    fn_sentiment_score = Headline.objects.filter(date__contains=today).filter(newspaper=3)
    if not fn_sentiment_score:
        fn_sentiment_score = [{'sentiment':0}]
        today1=yesterday

    ny_score = 0

    if nyt_sentiment_score == [{'sentiment':0}]:
        ny_score = 0
    else:


        for i in nyt_sentiment_score:
            ny_score += i.sentiment
        ny_score = ny_score/len(nyt_sentiment_score)
        ny_score = round(ny_score*100,1)

    if bbc_sentiment_score == [{'sentiment':0}]:
        bbc_score = 0
    else:

        bbc_score = 0
        for i in bbc_sentiment_score:
            bbc_score += i.sentiment
        bbc_score = bbc_score/len(bbc_sentiment_score)
        bbc_score = round(bbc_score*100,1)

    if fn_sentiment_score == [{'sentiment':0}]:
        fn_score = 0

    else:
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

    if nytheadlines == ["No headlines for this date. Headlines record start Jan 25, 2020"]:
        if bbcheadlines == ["No headlines for this date. Headlines record start Jan 25, 2020"]:
            if fnheadlines == ["No headlines for this date. Headlines record start Jan 25, 2020"]:
                    key1 = ''
                    freq1 = ''
                    key2 = ''
                    freq2 = ''
                    key3 = ''
                    freq3 = ''
    else:

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





    key1_photo_link = Photos.objects.filter(keyword=key1).filter(date__contains=today).first()



    form = DateForm()






    from django.db.models import Sum

    daily_emotion = Headline_emotion.objects.filter(day_order__lte=25).filter(date__contains=today).values('anger', 'fear', 'anticip', 'trust', 'surprise', 'sadness', 'disgust', 'joy' )


    emotion_count_dict = {}
    emotion_count_dict['anger'] = 0
    emotion_count_dict['fear'] = 0
    emotion_count_dict['anticip'] = 0
    emotion_count_dict['trust'] = 0
    emotion_count_dict['surprise'] = 0
    emotion_count_dict['sadness'] = 0
    emotion_count_dict['disgust'] = 0
    emotion_count_dict['joy'] = 0

    for record in daily_emotion:
        if record['anger'] > 0:
            emotion_count_dict['anger'] += record['anger']
        if record['fear'] > 0:
            emotion_count_dict['fear'] += record['fear']
        if record['anticip'] > 0:
            emotion_count_dict['anticip'] += record['anticip']
        if record['trust'] > 0:
            emotion_count_dict['trust'] += record['trust']

        if record['surprise'] > 0:
            emotion_count_dict['surprise'] += record['surprise']
        if record['sadness'] > 0:
            emotion_count_dict['sadness'] += record['sadness']
        if record['disgust'] > 0:
            emotion_count_dict['disgust'] += record['disgust']
        if record['joy'] > 0:
            emotion_count_dict['joy'] += record['joy']


    list_of_emotions = []
    for key, value in emotion_count_dict.items():
        interlist = [key, value]
        list_of_emotions.append(interlist)



    sorted_list_of_emotions = sorted(list_of_emotions, key=lambda x: x[1],reverse=True)

    emotion_display = sorted_list_of_emotions[:3]

    if not daily_emotion:
        emotion_display = [['',''], ['','']]






    return render(request, 'custom_scraper/date_search.html', {'emotion_display':emotion_display,"search":search, "nytheadlines":nytheadlines,"bbcheadlines":bbcheadlines,"fnheadlines":fnheadlines,"ny_score":ny_score, "bbc_score":bbc_score, "fn_score":fn_score, "overall_score":overall_score,"key1":key1,"key2":key2,"key3":key3,"freq1":freq1,"freq2":freq2,"freq3":freq3,  "nytheadlines":nytheadlines, "bbcheadlines":bbcheadlines, "fnheadlines":fnheadlines, "key1_photo_link":key1_photo_link, "form":form,"header_date":header_date, "scraped":scraped})


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
       font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', margin=dict(pad=50),showlegend=True )

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
    selected_year = today.year

    month_sent = Headline.objects.filter(day_order__lte=25).filter(date__month=selected_month).filter(date__year=selected).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
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








    print(final_list)






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

    print(top_overall)

    return render(request, 'custom_scraper/sentiment_overall_ajax.html', {'html_divos':html_divos, "average_sent":average_sent, "html_div_sent_hr": html_div_sent_hr, "html_div_pie": html_div_pie, "fig_sent_hist_div": fig_sent_hist_div, 'final_list': final_list, 'html_div_fig_pn': html_div_fig_pn, "top10list":top10list, "bottom10list":bottom10list, "positive":positive, "negative":negative, 'html_divosd':html_divosd, 'html_div_figdow': html_div_figdow, "html_divos_jason": html_divos_jason, 'this_month':this_month, 'top_overall':top_overall, 'worst_overall': worst_overall, 'best_people': best_people, 'top_places': top_places, 'top_political': top_political, 'top_rp': top_rp, 'top_economic': top_economic, 'top_corona': top_corona})


def sentiment_compare(request):
    from datetime import datetime
    from calendar import monthrange
    from django.db.models.functions import TruncYear


    today = datetime.today()
    yesterday = today - timedelta(1)
    today = str(today)[:10]

    yesterday = str(yesterday)[:10]
    cached = False

    if html_cache.objects.filter(date__contains=today).filter(page_num=3):
        html_record = html_cache.objects.filter(date__contains=today).filter(page_num=3).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/sentiment_compare.html',{'html':html, 'cached':cached},)

    if html_cache.objects.filter(date__contains=yesterday).filter(page_num=3):
        html_record = html_cache.objects.filter(date__contains=yesterday).filter(page_num=3).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/sentiment_compare.html',{'html':html, 'cached':cached},)












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
        selected_year = today.year
        month_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=np_code).filter(date__year=selected_year).filter(date__month=selected_month).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))


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
        elif day_of_week == "Saturday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
        elif day_of_week == "Tuesday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])

        elif day_of_week == "Thursday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])


        elif day_of_week == "Friday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
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
        selected_year = today.year

        if selected_month == 0:
            selected_month = 12

        if selected_month == 12:
            selected_year -= 1

        month_sent = Headline.objects.filter(day_order__lte=25).filter(newspaper=np_code).filter(date__year=selected_year).filter(date__month=selected_month).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))


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

        elif day_of_week == "Saturday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
        elif day_of_week == "Tuesday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])

        elif day_of_week == "Thursday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])


        elif day_of_week == "Friday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
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
    def css_to_calendars(calendar_data):
        for record in calendar_data:

            if record[1] == '':
                record.append('gray')
                record.append('')
            elif record[1] == ' ':
                record.append(' ')
                record.append(' ')
            elif record[1] > 4 and record[1] <=5:
                record.append('seven')
                record.append('seven7')

            elif record[1] > 5 and record[1] <= 6:
                record.append('eight')
                record.append('eight8')
            elif record[1] > 3 and record[1] <=4:
                record.append('six')
                record.append('six6')
            elif record[1] > 2 and record[1] <= 3:
                record.append('five')
                record.append('five5')
            elif record[1] > 1 and record[1] <= 2:
                record.append('four')
                record.append('four4')
            elif record[1] > 0 and record[1] <= 1:
                record.append('three')
                record.append('three3')
            elif record[1] > -1 and record[1] < 0:
                record.append('two')
                record.append('two2')
            elif record[1] > -2 and record[1] <= -1:
                record.append('one')
                record.append('one1')
            elif record[1] <= -2:
                record.append('zero')
                record.append('zero0')
            elif record[1] > 6:
                record.append('nine')
                record.append('nine9')

        return calendar_data

    nytimes_cal_last = css_to_calendars(nytimes_cal_last)
    bbc_cal_last = css_to_calendars(bbc_cal_last)
    fn_cal_last = css_to_calendars(fn_cal_last)

    nytimes_cal = css_to_calendars(nytimes_cal)
    bbc_cal = css_to_calendars(bbc_cal)
    fn_cal = css_to_calendars(fn_cal)



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
        font=dict(family="Roboto",size=13,color="black"), height=250, width=250, plot_bgcolor='white', margin=dict(l=5, r=5, t=5, b=5, pad=10),showlegend=True )

        pie_fig.update_traces(marker=dict(colors=["rgb(33,102,172)",'rgb(178,24,43)', 'whitesmoke']), textposition='inside')




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

    dow_test = Headline.objects.filter(day_order__lte=25).annotate(weekday=ExtractWeekDay('date')).values('weekday', 'newspaper').annotate(Average=Avg('sentiment')).order_by('weekday')





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

    hist_sent = Headline.objects.filter(day_order__lte=25).exclude(sentiment=0).annotate(Sentiment=F('sentiment') * 10).annotate(Sent=Ceil('Sentiment')).values('newspaper','Sent').annotate(Count=Count('id')).order_by('Sent')

    hist_sentdf = pd.DataFrame(list(hist_sent))


    hist_sentdf['newspaper'] = hist_sentdf['newspaper'].replace(1, 'The New York Times')
    hist_sentdf['newspaper'] = hist_sentdf['newspaper'].replace(2, 'BBC News')
    hist_sentdf['newspaper'] = hist_sentdf['newspaper'].replace(3, 'Fox News')
    hist_sentdf.rename(columns={'newspaper':'Newspaper'}, inplace= True)






    figcompare_hist_sent = px.line(hist_sentdf, x="Sent", y="Count", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )


    figcompare_hist_sent.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), )

    html_div_compare_hist_sent = str(plotly.offline.plot(figcompare_hist_sent, output_type='div', config = {'displayModeBar': False}))

    sent_hr = Headline.objects.filter(day_order__lte=25).values('newspaper', 'day_order').annotate(Average=Avg('sentiment')).order_by('day_order')

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

    from custom_scraper.models import superlative_table
    from custom_scraper.models import variance_table





    def superlatives_function(graph_num):
        today_super = date.today()
        nyt_best_words = []
        bbc_best_words = []
        fn_best_words = []

        nyt_best_words_raw = superlative_table.objects.filter(graphid=graph_num).filter(newspaper=1).filter(date__contains=today_super).values('word', 'count', 'sentiment').order_by('-sentiment')
        bbc_best_words_raw = superlative_table.objects.filter(graphid=graph_num).filter(newspaper=2).filter(date__contains=today_super).values('word', 'count', 'sentiment').order_by('-sentiment')
        fn_best_words_raw = superlative_table.objects.filter(graphid=graph_num).filter(newspaper=3).filter(date__contains=today_super).values('word', 'count', 'sentiment').order_by('-sentiment')




        for i in nyt_best_words_raw:
            interlist = []
            interlist.append(i['word'])
            interlist.append(i['count'])
            interlist.append(round(i['sentiment'],2))
            nyt_best_words.append(interlist)

        for i in bbc_best_words_raw:
            interlist = []
            interlist.append(i['word'])
            interlist.append(i['count'])
            interlist.append(round(i['sentiment'],2))
            bbc_best_words.append(interlist)

        for i in fn_best_words_raw:
            interlist = []
            interlist.append(i['word'])
            interlist.append(i['count'])
            interlist.append(round(i['sentiment'],2))
            fn_best_words.append(interlist)

        superlatives_output = []
        superlatives_output.append(nyt_best_words)
        superlatives_output.append(bbc_best_words)
        superlatives_output.append(fn_best_words)

        return superlatives_output

    graph1_superlative = superlatives_function(1)
    nyt_best_words = graph1_superlative[0]
    bbc_best_words = graph1_superlative[1]
    fn_best_words = graph1_superlative[2]

    graph2_superlative = superlatives_function(2)
    nyt_worst_words = sorted(graph2_superlative[0], reverse=False, key=lambda item:item[2])
    bbc_worst_words = sorted(graph2_superlative[1], reverse=False, key=lambda item:item[2])
    fn_worst_words = sorted(graph2_superlative[2], reverse=False, key=lambda item:item[2])


    graph3_superlative = superlatives_function(3)
    nyt_best_people = graph3_superlative[0]
    bbc_best_people = graph3_superlative[1]
    fn_best_people = graph3_superlative[2]

    graph4_superlative = superlatives_function(4)
    nyt_best_places = graph4_superlative[0]
    bbc_best_places = graph4_superlative[1]
    fn_best_places = graph4_superlative[2]

    graph5_superlative = superlatives_function(5)
    nyt_politics_words = graph5_superlative[0]
    bbc_politics_words = graph5_superlative[1]
    fn_politics_words = graph5_superlative[2]

    graph6_superlative = superlatives_function(6)
    nyt_economic_words = graph6_superlative[0]
    bbc_economic_words = graph6_superlative[1]
    fn_economic_words = graph6_superlative[2]

    graph7_superlative = superlatives_function(7)
    nyt_corona_words = graph7_superlative[0]
    bbc_corona_words = graph7_superlative[1]
    fn_corona_words = graph7_superlative[2]

    graph8_superlative = superlatives_function(8)
    nyt_rp_words = graph8_superlative[0]
    bbc_rp_words = graph8_superlative[1]
    fn_rp_words = graph8_superlative[2]

    today_var = date.today()

    variance_dates = variance_table.objects.filter(graphid=9).filter(date__contains=today_var).values('variance_date', 'news1', 'news2', 'sentiment').order_by('id')[:100]

    most_variance_dates = []
    for i in variance_dates:
        interlist = []
        interlist.append(i['variance_date'].date())
        interlist.append(i['news1'])
        interlist.append(i['news2'])
        interlist.append(round(i['sentiment'],2))
        most_variance_dates.append(interlist)




    for i in most_variance_dates:
        date_var = i[0]
        i.append('{:02d}'.format(date_var.month))
        i.append('{:02d}'.format(date_var.day))
        i.append(date_var.year)













    def variance_variables(papernum1, papernum2):

        def total_variance_avg_sentiment_day(newspaper):
            newspaper1data = Headline.objects.filter(day_order__lte=25).filter(newspaper=newspaper).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('Date')

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
            paper_color1 = '#2d2e30'
            papername1 = "The New York Times"
        elif papernum1 == 2:
            paper_color1 = '#bb1919'
            papername1 = "BBC News"
        elif papernum1 == 3:
            paper_color1 = '#006edb'
            papername1 = "Fox News"

        if papernum2 == 1:
            paper_color2 = '#2d2e30'
            papername2 = "The New York Times"
        elif papernum2 == 2:
            paper_color2 ='#bb1919'
            papername2 = "BBC News"
        elif papernum2 == 3:
            paper_color2 =  '#006edb'
            papername2 = "Fox News"




        fig_var_sent_nyt_fn =  go.Figure()
        fig_var_sent_nyt_fn.add_trace(go.Scatter(x=nyt_avg_sent[0][start_index:end_index], y=nyt_avg_sent[1][start_index:end_index], name=papername1,
            fill=None,
            mode='lines',
            line_color=paper_color1
            ))
        fig_var_sent_nyt_fn.add_trace(go.Scatter(
            x=fn_avg_sent[0][start_index:end_index],
            y=fn_avg_sent[1][start_index:end_index], name=papername2,
            fill='tonexty',
            mode='lines', line_color=paper_color2, line=dict(width=2),
        ))

        fig_var_sent_nyt_fn.update_layout(
            font=dict(family="Roboto",size=13,color="black"),  plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0),showlegend=False, height=300 )


        html_div_fig_nyt_fn = str(plotly.offline.plot(fig_var_sent_nyt_fn, output_type='div',config = {'displayModeBar': False},))


        variance_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum1).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by('Date')

        variance_fn = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum2).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by('Date')





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


    most_variance_words = []

    today_var_word = date.today()
    from custom_scraper.models import variance_table_word

    variance_words = variance_table_word.objects.filter(graphid=10).filter(date__contains=today_var_word).values('word', 'count', 'news1', 'news2', 'sentiment')

    for i in variance_words:
        interlist = []
        interlist.append(i['word'])
        interlist.append(i['count'])
        interlist.append(i['news1'])
        interlist.append(i['news2'])
        interlist.append(round(i['sentiment'],2))
        most_variance_words.append(interlist)




    def variance_graph(graphidnum):
        today_var_word = date.today()
        variance_lister = variance_table_word.objects.filter(graphid=graphidnum).filter(date__contains=today_var_word).values('word', 'count', 'news1', 'news2', 'sentiment')

        output_list = []

        for i in variance_lister:
            interlist = []
            interlist.append(i['word'])
            interlist.append(i['count'])
            interlist.append(i['news1'])
            interlist.append(i['news2'])
            interlist.append(round(i['sentiment'],2))
            output_list.append(interlist)

        return(output_list)

    most_variance_people = variance_graph(11)
    most_variance_places = variance_graph(12)
    most_variance_politics = variance_graph(13)
    most_variance_economics = variance_graph(14)
    most_variance_corona = variance_graph(15)
    most_variance_rp = variance_graph(16)


    #overlapping distribution: daily average sentiment
    nyt_sentiment_daily = Headline.objects.filter(newspaper=1).filter(day_order__lte=25).exclude(sentiment=0).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date",)
    bbc_sentiment_daily = Headline.objects.filter(newspaper=2).filter(day_order__lte=25).exclude(sentiment=0).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date",)
    fn_sentiment_daily = Headline.objects.filter(newspaper=3).filter(day_order__lte=25).exclude(sentiment=0).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date",)


    def get_daily_averaget(queryset):
        output_list = []
        for i in queryset:
            output_list.append(float(round(i['Average'] * 100, 2)))
        return output_list

    nyt_curve = get_daily_averaget(nyt_sentiment_daily)
    bbc_curve = get_daily_averaget(bbc_sentiment_daily)
    fn_curve = get_daily_averaget(fn_sentiment_daily)


    import plotly.figure_factory as ff


    hist_data = [nyt_curve, bbc_curve, fn_curve]

    group_labels = ['The New York Times', 'BBC News', 'Fox News']

    colors = ['#2d2e30', '#bb1919', '#006edb']

    fig_curve = ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)
    fig_curve.update_layout(
            font=dict(family="Roboto",size=13,color="black"),  plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0), height=300 )


    html_div_fig_curve = str(plotly.offline.plot(fig_curve, output_type='div',config = {'displayModeBar': False},))



    #overlapping distribution for all articles by newspaper
    nyt_sentiment_all = Headline.objects.filter(newspaper=1).filter(day_order__lte=25).exclude(sentiment=0).values('sentiment')
    bbc_sentiment_all = Headline.objects.filter(newspaper=2).filter(day_order__lte=25).exclude(sentiment=0).values('sentiment')
    fn_sentiment_all = Headline.objects.filter(newspaper=3).filter(day_order__lte=25).exclude(sentiment=0).values('sentiment')


    def get_daily_average_all(queryset):
        output_list = []
        for i in queryset:
            output_list.append(float(round(i['sentiment'] * 100, 2)))
        return output_list

    nyt_curve_all = get_daily_average_all(nyt_sentiment_all)
    bbc_curve_all = get_daily_average_all(bbc_sentiment_all)
    fn_curve_all = get_daily_average_all(fn_sentiment_all)



    import plotly.figure_factory as ff


    hist_data_all = [nyt_curve_all, bbc_curve_all, fn_curve_all]

    group_labels_all = ['The New York Times', 'BBC News', 'Fox News']

    colors_all = ['#2d2e30', '#bb1919', '#006edb']

    fig_curve_all = ff.create_distplot(hist_data_all, group_labels_all, show_hist=False, colors=colors_all)
    fig_curve_all.update_layout(
            font=dict(family="Roboto",size=13,color="black"),  plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0), height=300 )


    html_div_fig_curve_all = str(plotly.offline.plot(fig_curve_all, output_type='div',config = {'displayModeBar': False},))

    template = loader.get_template('custom_scraper/sentiment_compare.html')


    context = {'html_div_compare': html_div_compare,   'html_div_compare_month': html_div_compare_month, 'nytimes_cal': nytimes_cal, 'bbc_cal': bbc_cal, 'fn_cal': fn_cal, 'this_month':this_month, 'last_month': last_month, 'nytimes_cal_last': nytimes_cal_last, 'bbc_cal_last': bbc_cal_last, 'fn_cal_last': fn_cal_last, 'nyt_pie': nyt_pie, 'bbc_pie': bbc_pie, 'fn_pie': fn_pie, 'nyt_average_ytd': nyt_average_ytd, 'bbc_average_ytd': bbc_average_ytd, 'fn_average_ytd': fn_average_ytd, 'html_div_compare_month_pos': html_div_compare_month_pos, 'html_div_compare_month_neg': html_div_compare_month_neg, 'html_div_compare_month_neu': html_div_compare_month_neu, 'html_div_compare_dow_sent': html_div_compare_dow_sent, 'html_div_compare_hist_sent': html_div_compare_hist_sent, 'html_div_compare_sent_hr': html_div_compare_sent_hr, 'nyt_best_words': nyt_best_words, 'bbc_best_words': bbc_best_words, 'fn_best_words': fn_best_words, 'nyt_best_people': nyt_best_people, 'bbc_best_people': bbc_best_people, 'fn_best_people': fn_best_people, 'nyt_worst_words': nyt_worst_words, 'bbc_worst_words': bbc_worst_words, 'fn_worst_words': fn_worst_words, 'nyt_best_places': nyt_best_places, 'bbc_best_places': bbc_best_places, 'fn_best_places': fn_best_places, 'nyt_politics_words': nyt_politics_words, 'bbc_politics_words': bbc_politics_words, 'fn_politics_words': fn_politics_words, 'nyt_economic_words': nyt_economic_words, 'bbc_economic_words': bbc_economic_words, 'fn_economic_words': fn_economic_words, 'nyt_corona_words': nyt_corona_words, 'bbc_corona_words': bbc_corona_words, 'fn_corona_words': fn_corona_words, 'nyt_rp_words': nyt_rp_words, 'bbc_rp_words': bbc_rp_words, 'fn_rp_words': fn_rp_words, 'html_div_fig_nyt_fn': html_div_fig_nyt_fn, 'html_div_fig_nyt_bbc': html_div_fig_nyt_bbc, 'html_div_fig_fn_bbc': html_div_fig_fn_bbc, 'fn_nyt_average_variance': fn_nyt_average_variance, 'bbc_nyt_average_variance': bbc_nyt_average_variance, 'fn_bbc_average_variance':  fn_bbc_average_variance, 'most_variance_dates': most_variance_dates, 'most_variance_words': most_variance_words , 'most_variance_people': most_variance_people,  'most_variance_politics': most_variance_politics,  'most_variance_economics': most_variance_economics,      'most_variance_corona': most_variance_corona, 'most_variance_rp': most_variance_rp, 'html_div_fig_curve': html_div_fig_curve, 'html_div_fig_curve_all': html_div_fig_curve_all  }
    cache_test = HttpResponse(template.render(context, request),)

    cache_test = cache_test.content.decode("utf-8")
    html_cache_save = html_cache(page_num=3, cache_html=cache_test)
    html_cache_save.save()


























    return render(request, 'custom_scraper/sentiment_compare.html', {'html_div_compare': html_div_compare,   'html_div_compare_month': html_div_compare_month, 'nytimes_cal': nytimes_cal, 'bbc_cal': bbc_cal, 'fn_cal': fn_cal, 'this_month':this_month, 'last_month': last_month, 'nytimes_cal_last': nytimes_cal_last, 'bbc_cal_last': bbc_cal_last, 'fn_cal_last': fn_cal_last, 'nyt_pie': nyt_pie, 'bbc_pie': bbc_pie, 'fn_pie': fn_pie, 'nyt_average_ytd': nyt_average_ytd, 'bbc_average_ytd': bbc_average_ytd, 'fn_average_ytd': fn_average_ytd, 'html_div_compare_month_pos': html_div_compare_month_pos, 'html_div_compare_month_neg': html_div_compare_month_neg, 'html_div_compare_month_neu': html_div_compare_month_neu, 'html_div_compare_dow_sent': html_div_compare_dow_sent, 'html_div_compare_hist_sent': html_div_compare_hist_sent, 'html_div_compare_sent_hr': html_div_compare_sent_hr, 'nyt_best_words': nyt_best_words, 'bbc_best_words': bbc_best_words, 'fn_best_words': fn_best_words, 'nyt_best_people': nyt_best_people, 'bbc_best_people': bbc_best_people, 'fn_best_people': fn_best_people, 'nyt_worst_words': nyt_worst_words, 'bbc_worst_words': bbc_worst_words, 'fn_worst_words': fn_worst_words, 'nyt_best_places': nyt_best_places, 'bbc_best_places': bbc_best_places, 'fn_best_places': fn_best_places, 'nyt_politics_words': nyt_politics_words, 'bbc_politics_words': bbc_politics_words, 'fn_politics_words': fn_politics_words, 'nyt_economic_words': nyt_economic_words, 'bbc_economic_words': bbc_economic_words, 'fn_economic_words': fn_economic_words, 'nyt_corona_words': nyt_corona_words, 'bbc_corona_words': bbc_corona_words, 'fn_corona_words': fn_corona_words, 'nyt_rp_words': nyt_rp_words, 'bbc_rp_words': bbc_rp_words, 'fn_rp_words': fn_rp_words, 'html_div_fig_nyt_fn': html_div_fig_nyt_fn, 'html_div_fig_nyt_bbc': html_div_fig_nyt_bbc, 'html_div_fig_fn_bbc': html_div_fig_fn_bbc, 'fn_nyt_average_variance': fn_nyt_average_variance, 'bbc_nyt_average_variance': bbc_nyt_average_variance, 'fn_bbc_average_variance':  fn_bbc_average_variance, 'most_variance_dates': most_variance_dates, 'most_variance_words': most_variance_words , 'most_variance_people': most_variance_people,  'most_variance_politics': most_variance_politics,  'most_variance_economics': most_variance_economics,      'most_variance_corona': most_variance_corona, 'most_variance_rp': most_variance_rp, 'html_div_fig_curve': html_div_fig_curve, 'html_div_fig_curve_all': html_div_fig_curve_all  })


def sentiment_newspaper(request):
    from datetime import datetime
    from calendar import monthrange
    from django.db.models.functions import TruncYear
    from django.db.models import Count
    import plotly.graph_objects as go


    today = datetime.today()
    yesterday = today - timedelta(1)
    today = str(today)[:10]

    yesterday = str(yesterday)[:10]
    cached = False

    if html_cache.objects.filter(date__contains=today).filter(page_num=2):
        html_record = html_cache.objects.filter(date__contains=today).filter(page_num=2).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/sentiment_newspaper.html',{'html':html, 'cached':cached},)

    if html_cache.objects.filter(date__contains=yesterday).filter(page_num=2):
        html_record = html_cache.objects.filter(date__contains=yesterday).filter(page_num=2).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/sentiment_newspaper.html',{'html':html, 'cached':cached},)

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



    def overall_sent_paper(paper_num):
        average_sentiment_by_day = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).annotate(Date=TruncDay('date')).values('Date').annotate(Sentiment=Avg('sentiment')).order_by('Date')
        dfosd = pd.DataFrame(list(average_sentiment_by_day))
        dfosd['Sentiment'] = dfosd['Sentiment'] * 100
        figosd = px.line(dfosd, x="Date", y="Sentiment",color_discrete_sequence=['black'] )
        figosd.update_layout(
            font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',xaxis_title='', yaxis_title ='', margin=dict(l=5, r=5, t=5, b=5, pad=10))


        figosd.update_layout(

        xaxis_tickformat = '%B',
        yaxis=dict(dtick=6),

        )

        html_divosd = str(plotly.offline.plot(figosd, output_type='div', config = {'displayModeBar': False}))

        return html_divosd

    html_divosd_nyt = overall_sent_paper(1)
    html_divosd_bbc = overall_sent_paper(2)
    html_divosd_fn = overall_sent_paper(3)






    today = datetime.today()




    selected_month = today.month
    selected_year = today.year

    month_sent = Headline.objects.filter(day_order__lte=25).filter(date__month=selected_month).filter(date__year=selected_year).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))


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
    elif day_of_week == "Saturday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
    elif day_of_week == "Tuesday":
        final_list.insert(0,[' ',' ',' ', '#', '',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])

    elif day_of_week == "Thursday":
        final_list.insert(0,[' ',' ',' ', '#', '',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])


    elif day_of_week == "Friday":
        final_list.insert(0,[' ',' ',' ', '#', '',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])
        final_list.insert(0,[' ',' ',' ', '#','',''])




    def get_calendar_heatmap(papernum):
        today = datetime.today()




        selected_month = today.month
        selected_year = today.year

        month_sent = Headline.objects.filter(day_order__lte=25).filter(date__month=selected_month).filter(date__year=selected_year).filter(newspaper=papernum).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))


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
        elif day_of_week == "Saturday":
                final_list.insert(0,[' ',' ',' ', '#', '',''])
                final_list.insert(0,[' ',' ',' ', '#','',''])
                final_list.insert(0,[' ',' ',' ', '#','',''])
                final_list.insert(0,[' ',' ',' ', '#', '',''])
                final_list.insert(0,[' ',' ',' ', '#','',''])
                final_list.insert(0,[' ',' ',' ', '#','',''])
        elif day_of_week == "Tuesday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])

        elif day_of_week == "Thursday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])


        elif day_of_week == "Friday":
            final_list.insert(0,[' ',' ',' ', '#', '',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])
            final_list.insert(0,[' ',' ',' ', '#','',''])

        return final_list


    final_list_nyt = get_calendar_heatmap(1)
    final_list_bbc = get_calendar_heatmap(2)
    final_list_fn = get_calendar_heatmap(3)









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
    go.Bar(name='Positive Sentiment', x=month_list, y=pos_values, marker_color="rgb(33,102,172)"),
    go.Bar(name='Negative Sentiment', x=month_list, y=neg_values, marker_color="rgb(178,24,43)"),])

    fig_pn.update_layout( legend={'traceorder':'normal'}, height=250)
    fig_pn.update_layout( font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, margin=dict(l=5, r=5, t=5, b=5, pad=10),xaxis_tickformat = '%b',
    yaxis=dict(dtick=300), )




    html_div_fig_pn = str(plotly.offline.plot(fig_pn, output_type='div', config = {'displayModeBar': False}))



    def get_sent_breakdown(papernum):

        pos_by_month = Headline.objects.filter(day_order__lte=25).filter(sentiment__gt=0).filter(newspaper=papernum).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id')).order_by('Date')

        neg_by_month = Headline.objects.filter(day_order__lte=25).filter(sentiment__lt=0).filter(newspaper=papernum).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id')).order_by('Date')

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
        go.Bar(name='Positive Sentiment', x=month_list, y=pos_values, marker_color="rgb(33,102,172)"),
        go.Bar(name='Negative Sentiment', x=month_list, y=neg_values, marker_color="rgb(178,24,43)"),])

        fig_pn.update_layout( legend={'traceorder':'normal'}, height=250)
        fig_pn.update_layout( font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, margin=dict(l=5, r=5, t=5, b=5, pad=10),xaxis_tickformat = '%b',
        yaxis=dict(dtick=300), )




        html_div_fig_pn = str(plotly.offline.plot(fig_pn, output_type='div', config = {'displayModeBar': False}))




        return html_div_fig_pn

    html_div_fig_pn_nyt = get_sent_breakdown(1)
    html_div_fig_pn_bbc = get_sent_breakdown(2)
    html_div_fig_pn_fn = get_sent_breakdown(3)



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
       font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', margin=dict(l=0, r=10, t=0, b=0, pad=0),showlegend=False )

    pie_fig.update_traces(marker=dict(colors=["rgb(33,102,172)",'rgb(178,24,43)', 'whitesmoke']))




    html_div_pie = str(plotly.offline.plot(pie_fig, output_type='div',config = {'displayModeBar': False},))



    def get_overall_pie(paper_num):
        overall_pos = Headline.objects.filter(day_order__lte=25).filter(sentiment__gt=0).filter(newspaper=paper_num).values('sentiment')

        overall_neg = Headline.objects.filter(day_order__lte=25).filter(sentiment__lt=0).filter(newspaper=paper_num).values('sentiment')

        overall_zero = Headline.objects.filter(day_order__lte=25).filter(sentiment=0).filter(newspaper=paper_num).values('sentiment')

        pie_labels = ['Positive', 'Negative', 'Neutral']

        pie_values = []

        pie_values.append(len(overall_pos))
        pie_values.append(len(overall_neg))
        pie_values.append(len(overall_zero))


        pie_fig = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values), ])

        pie_fig.update_layout(
        font=dict(family="Roboto",size=13,color="black"), plot_bgcolor='white', margin=dict(l=0, r=10, t=0, b=0, pad=0),showlegend=False )

        pie_fig.update_traces(marker=dict(colors=["rgb(33,102,172)",'rgb(178,24,43)', 'whitesmoke']))




        html_div_pie = str(plotly.offline.plot(pie_fig, output_type='div',config = {'displayModeBar': False},))

        return html_div_pie

    html_div_pie_nyt = get_overall_pie(1)
    html_div_pie_bbc = get_overall_pie(2)
    html_div_pie_fn = get_overall_pie(3)

    average_sentiment_by_month_one = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncYear('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date")


    for i in average_sentiment_by_month_one:
        average_sent = i['Average']

    average_sent = average_sent * 100
    average_sent = round(average_sent, 2)

    def get_average_sent(papernum):
        average_sentiment_by_month_one = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum).annotate(Date=TruncYear('date')).values('Date').annotate(Average=Avg('sentiment')).order_by("Date")


        for i in average_sentiment_by_month_one:
            average_sent = i['Average']

        average_sent = average_sent * 100
        average_sent = round(average_sent, 2)

        return average_sent

    average_sent_nyt = get_average_sent(1)
    average_sent_bbc = get_average_sent(2)
    average_sent_fn = get_average_sent(3)


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



    def get_dow_dist(papernum):

        average_by_day_of_week = []
        for i in range(1,8):
            average_by_named_day = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum).filter(date__week_day=i).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment'))
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

        return html_div_figdow

    html_div_figdow_nyt = get_dow_dist(1)
    html_div_figdow_bbc = get_dow_dist(2)
    html_div_figdow_fn = get_dow_dist(3)

    all_sentiments = Headline.objects.filter(day_order__lte=25).values('sentiment')

    sent_hist = []
    for i in all_sentiments:
        if i['sentiment'] != 0:
            sent_hist.append(round(i['sentiment'] * 100))




    fig_sent_hist = px.histogram( x=sent_hist, nbins=30, color_discrete_sequence=['rgb(33,102,172)'])
    fig_sent_hist.update_layout(font=dict(family="Roboto",size=15,color="black"),plot_bgcolor='white',bargap=0.2, margin=dict(l=5, r=5, t=5, b=5, pad=10),showlegend=False, yaxis=dict(dtick=200), xaxis_title='', yaxis_title='')

    """
    sent_hist = [sent_hist]
    fig_sent_hist = ff.create_distplot(sent_hist, 'Sentiment')
    """

    fig_sent_hist_div = str(plotly.offline.plot(fig_sent_hist, output_type='div',config = {'displayModeBar': False},))


    def get_sent_hist(papernum):

        all_sentiments = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum).values('sentiment')

        sent_hist = []
        for i in all_sentiments:
            if i['sentiment'] != 0:
                sent_hist.append(round(i['sentiment'] * 100))




        fig_sent_hist = px.histogram( x=sent_hist, nbins=30, color_discrete_sequence=['rgb(33,102,172)'])
        fig_sent_hist.update_layout(font=dict(family="Roboto",size=15,color="black"),bargap=0.2, plot_bgcolor='white', margin=dict(l=5, r=5, t=5, b=5, pad=10),showlegend=False, yaxis=dict(dtick=200), xaxis_title='', yaxis_title='')

        """
        sent_hist = [sent_hist]
        fig_sent_hist = ff.create_distplot(sent_hist, 'Sentiment')
        """

        fig_sent_hist_div = str(plotly.offline.plot(fig_sent_hist, output_type='div',config = {'displayModeBar': False},))

        return fig_sent_hist_div

    fig_sent_hist_div_nyt = get_sent_hist(1)
    fig_sent_hist_div_bbc = get_sent_hist(2)
    fig_sent_hist_div_fn = get_sent_hist(3)


    average_sentiment_by_hr = Headline.objects.filter(day_order__lte=25).values('day_order').annotate(Average=Avg('sentiment'))


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




    def get_sent_hr(papernum):
        average_sentiment_by_hr = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum).values('day_order').annotate(Average=Avg('sentiment'))


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

        return html_div_sent_hr

    html_div_sent_hr_nyt = get_sent_hr(1)
    html_div_sent_hr_bbc = get_sent_hr(2)
    html_div_sent_hr_fn = get_sent_hr(3)


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
        interlist.append(round(i['sentiment'] * 100, 0))
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


    def find_most_pos_neg_hls(papernum):

        most_positive_hls = Headline.objects.filter(sentiment=1).filter(newspaper=papernum).values('date', 'newspaper', 'headline', 'sentiment','link').order_by('date')





        most_negative_hls = Headline.objects.filter(sentiment=-1).filter(newspaper=papernum).values('date', 'newspaper', 'headline', 'sentiment','link').order_by('date')





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
            interlist.append(round(i['sentiment'] * 100, 0))
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

        both_return = []

        both_return.append(positive)
        both_return.append(negative)

        return both_return

    positive_nyt = find_most_pos_neg_hls(1)[0]
    negative_nyt = find_most_pos_neg_hls(1)[1]

    positive_bbc = find_most_pos_neg_hls(2)[0]
    negative_bbc = find_most_pos_neg_hls(2)[1]

    positive_fn = find_most_pos_neg_hls(3)[0]
    negative_fn = find_most_pos_neg_hls(3)[1]





    month_sent_overall = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('-Average')



    month_sent_overall = month_sent_overall[:20]



    top10list = []

    for i in month_sent_overall:
        interlist = []
        interlist.append(i['Date'].date())
        interlist.append(round(i['Average']*100,1))
        interlist.append("{:02d}".format(i['Date'].month))
        interlist.append("{:02d}".format(i['Date'].day))
        interlist.append(i['Date'].year)
        top10list.append(interlist)

    def find_best_dates(papernum):

        month_sent_overall = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('-Average')



        month_sent_overall = month_sent_overall[:20]



        top10list = []

        for i in month_sent_overall:
            interlist = []
            interlist.append(i['Date'].date())
            interlist.append(round(i['Average']*100,1))
            interlist.append("{:02d}".format(i['Date'].month))
            interlist.append("{:02d}".format(i['Date'].day))
            interlist.append(i['Date'].year)
            top10list.append(interlist)

        return top10list

    top10list_nyt = find_best_dates(1)
    top10list_bbc = find_best_dates(2)
    top10list_fn = find_best_dates(3)



    month_sent_overall_neg = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('Average')



    month_sent_overall_neg = month_sent_overall_neg[:20]

    bottom10list = []

    for i in month_sent_overall_neg:
        interlist = []
        interlist.append(i['Date'].date())
        interlist.append(round(i['Average']*100,1))
        interlist.append("{:02d}".format(i['Date'].month))
        interlist.append("{:02d}".format(i['Date'].day))
        interlist.append(i['Date'].year)

        bottom10list.append(interlist)






    def find_worst_dates(papernum):

        month_sent_overall_neg = Headline.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Average=Avg('sentiment')).order_by('Average')



        month_sent_overall_neg = month_sent_overall_neg[:20]

        bottom10list = []

        for i in month_sent_overall_neg:
            interlist = []
            interlist.append(i['Date'].date())
            interlist.append(round(i['Average']*100,1))
            interlist.append("{:02d}".format(i['Date'].month))
            interlist.append("{:02d}".format(i['Date'].day))
            interlist.append(i['Date'].year)

            bottom10list.append(interlist)




        return bottom10list

    bottom10list_nyt = find_worst_dates(1)
    bottom10list_bbc = find_worst_dates(2)
    bottom10list_fn = find_worst_dates(3)

    from custom_scraper.models import superlative_table

    today_super = date.today()
    top_overall_query = superlative_table.objects.filter(graphid=21).filter(newspaper=4).filter(date__contains=today_super).values('word', 'count', 'sentiment')

    top_overall_list = []

    for i in top_overall_query:

        interlist = []
        interlist.append(i['word'])
        interlist.append(i['count'])
        interlist.append(round(i['sentiment'],2))
        top_overall_list.append(interlist)

    top_overall = top_overall_list



    worst_overall_query = superlative_table.objects.filter(graphid=20).filter(newspaper=4).filter(date__contains=today_super).values('word', 'count', 'sentiment')

    worst_overall_list = []

    for i in worst_overall_query:

        interlist = []
        interlist.append(i['word'])
        interlist.append(i['count'])
        interlist.append(round(i['sentiment'],2))
        worst_overall_list.append(interlist)

    worst_overall = worst_overall_list

    def superlatives_get(graphid_number):
        def superlatives_get_by_paper(papernumber):
            overall_query = superlative_table.objects.filter(graphid=graphid_number).filter(newspaper=papernumber).filter(date__contains=today_super).values('word', 'count', 'sentiment').order_by('-sentiment')
            end_list = []
            for i in overall_query:
                interlist = []
                interlist.append(i['word'])
                interlist.append(i['count'])
                interlist.append(round(i['sentiment'],2))
                end_list.append(interlist)
            return end_list

        nyt = superlatives_get_by_paper(1)
        bbc = superlatives_get_by_paper(2)
        fn = superlatives_get_by_paper(3)
        all_super = superlatives_get_by_paper(4)

        returning = []
        returning.append(all_super)
        returning.append(nyt)
        returning.append(bbc)
        returning.append(fn)

        return returning



    person_list = superlatives_get(30)
    best_people = person_list[0]
    best_people_nyt = person_list[1]
    best_people_bbc = person_list[2]
    best_people_fn = person_list[3]

    place_list = superlatives_get(31)
    top_places = place_list[0]
    top_places_nyt = place_list[1]
    top_places_bbc = place_list[2]
    top_places_fn = place_list[3]

    political_list = superlatives_get(32)
    top_political = political_list[0]
    top_political_nyt = political_list[1]
    top_political_bbc = political_list[2]
    top_political_fn = political_list[3]

    economics_list = superlatives_get(33)
    top_economic = economics_list[0]
    top_economic_nyt = economics_list[1]
    top_economic_bbc = economics_list[2]
    top_economic_fn = economics_list[3]

    corona_list = superlatives_get(34)
    top_corona = corona_list[0]
    top_corona_nyt = corona_list[1]
    top_corona_bbc = corona_list[2]
    top_corona_fn = corona_list[3]

    rp_list = superlatives_get(35)
    top_rp = rp_list[0]
    top_rp_nyt = rp_list[1]
    top_rp_bbc = rp_list[2]
    top_rp_fn = rp_list[3]

    top_overall_list = superlatives_get(21)
    top_overall_nyt = top_overall_list[1]
    top_overall_bbc = top_overall_list[2]
    top_overall_fn = top_overall_list[3]

    worst_overall_list = superlatives_get(20)
    worst_overall_nyt = sorted(worst_overall_list[1], reverse=False, key=lambda item: item[2])
    worst_overall_bbc = sorted(worst_overall_list[2], reverse=False, key=lambda item: item[2])
    worst_overall_fn = sorted(worst_overall_list[3], reverse=False, key=lambda item: item[2])
    print(worst_overall_nyt)








    #sentiment heat map list: add css class to each date list
    def css_to_calendars(calendar_data):
        for record in calendar_data:

            if record[1] == '':
                record.append('gray')
                record.append('')
            elif record[1] == ' ':
                record.append(' ')
                record.append(' ')
            elif record[1] > 4 and record[1] <=5:
                record.append('seven')
                record.append('seven7')

            elif record[1] > 5 and record[1] <= 6:
                record.append('eight')
                record.append('eight8')
            elif record[1] > 3 and record[1] <=4:
                record.append('six')
                record.append('six6')
            elif record[1] > 2 and record[1] <= 3:
                record.append('five')
                record.append('five5')
            elif record[1] > 1 and record[1] <= 2:
                record.append('four')
                record.append('four4')
            elif record[1] > 0 and record[1] <= 1:
                record.append('three')
                record.append('three3')
            elif record[1] > -1 and record[1] < 0:
                record.append('two')
                record.append('two2')
            elif record[1] > -2 and record[1] <= -1:
                record.append('one')
                record.append('one1')
            elif record[1] <= -2:
                record.append('zero')
                record.append('zero0')
            elif record[1] > 6:
                record.append('nine')
                record.append('nine9')

        return calendar_data

    final_list = css_to_calendars(final_list)
    final_list_nyt = css_to_calendars(final_list_nyt)
    final_list_bbc = css_to_calendars(final_list_bbc)
    final_list_fn = css_to_calendars(final_list_fn)


    #Headlines -> add newspaper icon css class to each record list
    for record in positive_nyt:
        record.append('nyt_small')
    for record in negative_nyt:
        record.append('nyt_small')
    for record in positive_bbc:
        record.append('bbc_small')
    for record in negative_bbc:
        record.append('bbc_small')
    for record in positive_fn:
        record.append('fn_small')
    for record in negative_fn:
        record.append('fn_small')

    for record in positive:
        if record[1] == 'NYT':
            record.append('nyt_small')
        elif record[1] == 'BBC':
            record.append('bbc_small')
        elif record[1] == 'FN':
            record.append('fn_small')

    for record in negative:
        if record[1] == 'NYT':
            record.append('nyt_small')
        elif record[1] == 'BBC':
            record.append('bbc_small')
        elif record[1] == 'FN':
            record.append('fn_small')

    template = loader.get_template('custom_scraper/sentiment_newspaper.html')


    context = {'html_divosd': html_divosd, 'html_divosd_nyt': html_divosd_nyt, 'html_divosd_bbc': html_divosd_bbc, 'html_divosd_fn': html_divosd_fn, 'this_month':this_month, 'final_list':final_list, 'final_list_nyt': final_list_nyt, 'final_list_bbc': final_list_bbc, 'final_list_fn': final_list_fn, 'html_div_fig_pn': html_div_fig_pn, 'html_div_fig_pn_nyt': html_div_fig_pn_nyt, 'html_div_fig_pn_bbc': html_div_fig_pn_bbc, 'html_div_fig_pn_fn': html_div_fig_pn_fn, 'html_div_pie': html_div_pie, 'html_div_pie_nyt': html_div_pie_nyt, 'html_div_pie_bbc': html_div_pie_bbc, 'html_div_pie_fn': html_div_pie_fn, 'average_sent': average_sent, 'average_sent_nyt': average_sent_nyt, 'average_sent_bbc': average_sent_bbc, 'average_sent_fn': average_sent_fn, 'html_div_figdow': html_div_figdow, 'html_div_figdow_nyt': html_div_figdow_nyt, 'html_div_figdow_bbc': html_div_figdow_bbc, 'html_div_figdow_fn': html_div_figdow_fn, 'fig_sent_hist_div': fig_sent_hist_div, 'fig_sent_hist_div_nyt': fig_sent_hist_div_nyt, 'fig_sent_hist_div_bbc': fig_sent_hist_div_bbc, 'fig_sent_hist_div_fn': fig_sent_hist_div_fn, 'html_div_sent_hr': html_div_sent_hr, 'html_div_sent_hr_nyt': html_div_sent_hr_nyt, 'html_div_sent_hr_bbc': html_div_sent_hr_bbc, 'html_div_sent_hr_fn': html_div_sent_hr_fn, 'positive':positive, 'positive_nyt': positive_nyt, 'positive_bbc': positive_bbc, 'positive_fn': positive_fn, 'negative_nyt': negative_nyt, 'negative_bbc': negative_bbc, 'negative_fn': negative_fn, 'top10list': top10list, 'top10list_nyt': top10list_nyt, 'top10list_bbc': top10list_bbc,  'top10list_fn': top10list_fn, 'negative':negative, 'bottom10list':bottom10list, 'bottom10list_nyt':bottom10list_nyt, 'bottom10list_bbc':bottom10list_bbc, 'bottom10list_fn':bottom10list_fn, 'bottom10list': bottom10list, 'top_overall': top_overall, 'worst_overall': worst_overall, 'best_people': best_people, 'best_people_nyt': best_people_nyt, 'best_people_bbc': best_people_bbc, 'best_people_fn': best_people_fn, 'top_places': top_places, 'top_places_nyt': top_places_nyt, 'top_places_bbc': top_places_bbc, 'top_places_fn': top_places_fn, 'top_political': top_political, 'top_political_nyt': top_political_nyt, 'top_political_bbc': top_political_bbc, 'top_political_fn': top_political_fn, 'top_economic': top_economic, 'top_economic_nyt':top_economic_nyt, 'top_economic_bbc':top_economic_bbc, 'top_economic_fn': top_economic_fn,  'top_corona':top_corona, 'top_corona_nyt':top_corona_nyt, 'top_corona_bbc':top_corona_bbc, 'top_corona_fn':top_corona_fn, 'top_rp':top_rp, 'top_rp_nyt':top_rp_nyt, 'top_rp_bbc':top_rp_bbc, 'top_rp_fn':top_rp_fn, 'top_overall_nyt': top_overall_nyt, 'top_overall_fn': top_overall_fn, 'top_overall_bbc': top_overall_bbc, 'worst_overall_nyt': worst_overall_nyt, 'worst_overall_bbc': worst_overall_bbc, 'worst_overall_fn': worst_overall_fn }
    cache_test = HttpResponse(template.render(context, request),)

    cache_test = cache_test.content.decode("utf-8")
    html_cache_save = html_cache(page_num=2, cache_html=cache_test)
    html_cache_save.save()

    return render(request, 'custom_scraper/sentiment_newspaper.html', {'html_divosd': html_divosd, 'html_divosd_nyt': html_divosd_nyt, 'html_divosd_bbc': html_divosd_bbc, 'html_divosd_fn': html_divosd_fn, 'this_month':this_month, 'final_list':final_list, 'final_list_nyt': final_list_nyt, 'final_list_bbc': final_list_bbc, 'final_list_fn': final_list_fn, 'html_div_fig_pn': html_div_fig_pn, 'html_div_fig_pn_nyt': html_div_fig_pn_nyt, 'html_div_fig_pn_bbc': html_div_fig_pn_bbc, 'html_div_fig_pn_fn': html_div_fig_pn_fn, 'html_div_pie': html_div_pie, 'html_div_pie_nyt': html_div_pie_nyt, 'html_div_pie_bbc': html_div_pie_bbc, 'html_div_pie_fn': html_div_pie_fn, 'average_sent': average_sent, 'average_sent_nyt': average_sent_nyt, 'average_sent_bbc': average_sent_bbc, 'average_sent_fn': average_sent_fn, 'html_div_figdow': html_div_figdow, 'html_div_figdow_nyt': html_div_figdow_nyt, 'html_div_figdow_bbc': html_div_figdow_bbc, 'html_div_figdow_fn': html_div_figdow_fn, 'fig_sent_hist_div': fig_sent_hist_div, 'fig_sent_hist_div_nyt': fig_sent_hist_div_nyt, 'fig_sent_hist_div_bbc': fig_sent_hist_div_bbc, 'fig_sent_hist_div_fn': fig_sent_hist_div_fn, 'html_div_sent_hr': html_div_sent_hr, 'html_div_sent_hr_nyt': html_div_sent_hr_nyt, 'html_div_sent_hr_bbc': html_div_sent_hr_bbc, 'html_div_sent_hr_fn': html_div_sent_hr_fn, 'positive':positive, 'positive_nyt': positive_nyt, 'positive_bbc': positive_bbc, 'positive_fn': positive_fn, 'negative_nyt': negative_nyt, 'negative_bbc': negative_bbc, 'negative_fn': negative_fn, 'top10list': top10list, 'top10list_nyt': top10list_nyt, 'top10list_bbc': top10list_bbc,  'top10list_fn': top10list_fn, 'negative':negative, 'bottom10list':bottom10list, 'bottom10list_nyt':bottom10list_nyt, 'bottom10list_bbc':bottom10list_bbc, 'bottom10list_fn':bottom10list_fn, 'bottom10list': bottom10list, 'top_overall': top_overall, 'worst_overall': worst_overall, 'best_people': best_people, 'best_people_nyt': best_people_nyt, 'best_people_bbc': best_people_bbc, 'best_people_fn': best_people_fn, 'top_places': top_places, 'top_places_nyt': top_places_nyt, 'top_places_bbc': top_places_bbc, 'top_places_fn': top_places_fn, 'top_political': top_political, 'top_political_nyt': top_political_nyt, 'top_political_bbc': top_political_bbc, 'top_political_fn': top_political_fn, 'top_economic': top_economic, 'top_economic_nyt':top_economic_nyt, 'top_economic_bbc':top_economic_bbc, 'top_economic_fn': top_economic_fn,  'top_corona':top_corona, 'top_corona_nyt':top_corona_nyt, 'top_corona_bbc':top_corona_bbc, 'top_corona_fn':top_corona_fn, 'top_rp':top_rp, 'top_rp_nyt':top_rp_nyt, 'top_rp_bbc':top_rp_bbc, 'top_rp_fn':top_rp_fn, 'top_overall_nyt': top_overall_nyt, 'top_overall_fn': top_overall_fn, 'top_overall_bbc': top_overall_bbc, 'worst_overall_nyt': worst_overall_nyt, 'worst_overall_bbc': worst_overall_bbc, 'worst_overall_fn': worst_overall_fn })


def sentiment_word_search(request):


    form = WordCountSearch()

    import plotly.graph_objects as go

    from datetime import datetime

    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today = str(today)[:10]
    yesterday = str(yesterday)[:10]


    if not Headline.objects.filter(date__contains=today).values('headline'):
        today = yesterday


    top_10_words_terms = word_count_general.objects.filter(newspaper=4).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:9]
    test_terms = []
    test_overall_values_list = []
    for i in top_10_words_terms:
        test_terms.append(i['word'])
        test_overall_values_list.append(i['word_count'])



    test_values_list = []

    for i in range(1,4):
        newspaper_values = []
        for y in test_terms:
            all_test_values = word_count_general.objects.filter(date__contains=today).filter(newspaper=i).filter(word=y).values('word_count')
            for record in all_test_values:
                newspaper_values.append(record['word_count'])
        test_values_list.append(newspaper_values)






    test_ny_values_list = test_values_list[0]
    test_bbc_values_list = test_values_list[1]
    test_fn_values_list = test_values_list[2]




    values_fig = go.Figure(data=[
        go.Bar(name='New York Times', y=test_terms, x=test_ny_values_list, orientation='h', marker_color="#2d2e30"),
        go.Bar(name='BBC News', y=test_terms, x=test_bbc_values_list, orientation = 'h', marker_color="#bb1919"),
        go.Bar(name='Fox News', y=test_terms, x=test_fn_values_list, orientation = 'h', marker_color="rgba(0,51,102,.99)"),
    ], )
    values_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), height=400, plot_bgcolor='white', orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))








    return render(request, 'custom_scraper/sentiment_word_search.html', { 'form':form, 'html_div_values': html_div_values, } )


def sentiment_word_search_result(request):
    form = WordCountSearch()
    search = request.GET.get('word_count')



    key1data = Headline.objects.filter(headline__icontains=search)


    from django.shortcuts import redirect
    if not key1data or len(key1data) < 3:

        request.session['search'] = search
        return redirect('research')






    average_sentiment_by_date_compare_month = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search).annotate(Date=TruncMonth('date')).values('Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by("Date",)


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


    average_sentiment_by_date_compare = Headline.objects.filter(day_order__lte=25).filter(day_order__lte=25).filter(headline__icontains=search).annotate(Date=TruncDay('date')).values('Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by("Date",)


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

    import plotly.graph_objects as go

    ny_sentiment = Headline.objects.filter(newspaper=1).filter(day_order__lte=25).filter(headline__icontains=search)
    bbc_sentiment = Headline.objects.filter(newspaper=2).filter(day_order__lte=25).filter(headline__icontains=search)
    fn_sentiment = Headline.objects.filter(newspaper=3).filter(day_order__lte=25).filter(headline__icontains=search)

    overall_sentiment_query = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search)

    overall_average = 0
    for i in overall_sentiment_query:
        overall_average += i.sentiment

    if len(overall_sentiment_query) == 0:
        overall_average = 0
    else:
        overall_average = overall_average/len(overall_sentiment_query)
        overall_average = 100 * overall_average
        overall_average = round(overall_average,1)



    nyt_average = 0
    for i in ny_sentiment:
        nyt_average += i.sentiment

    if len(ny_sentiment) == 0:
        nyt_average = 0
    else:
        nyt_average = nyt_average/len(ny_sentiment)
        nyt_average = 100 * nyt_average
        nyt_average = round(nyt_average,1)

    bbc_average = 0
    for i in bbc_sentiment:
        bbc_average += i.sentiment

    if len(bbc_sentiment) == 0:
        bbc_average = 0
    else:
        bbc_average = bbc_average/len(bbc_sentiment)
        bbc_average = 100 * bbc_average
        bbc_average = round(bbc_average,1)

    fn_average = 0
    for i in fn_sentiment:
        fn_average += i.sentiment

    if len(fn_sentiment) == 0:
        fn_average = 0
    else:
        fn_average = fn_average/len(fn_sentiment)
        fn_average = 100 * fn_average
        fn_average = round(fn_average,1)

    averages = []
    averages.append(nyt_average)
    averages.append(bbc_average)
    averages.append(fn_average)

    average_sentiment_title = ["The New York Times", "BBC News", "Fox News"]

    sentiment_fig = go.Figure([go.Bar(x=average_sentiment_title, y=averages, marker_color=["#2d2e30","#bb1919","rgba(0,51,102,.99)" ])])

    sentiment_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), orientation=90, height=300,margin=dict(l=5, r=0, t=5, b=5, pad=10),plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', )


    html_div_sentiment = str(plotly.offline.plot(sentiment_fig, output_type='div', config = {'displayModeBar': False}))
    def find_related_words(papernumber):
        #Find related words

        all_headlines_with_search_word = Headline.objects.filter(newspaper=papernumber).filter(day_order__lte=25).filter(headline__icontains=search).values('headline')

        #make string of all headlines with search word
        all_headlines_with_search_word_list = []
        for i in all_headlines_with_search_word:
            all_headlines_with_search_word_list.append(i['headline'])

        related_words_pool = " ".join(all_headlines_with_search_word_list)


        normalized = related_words_pool.lower()

        normalized = normalized.replace(':', '')
        normalized = normalized.replace(',', '')
        normalized = normalized.replace('.','')

        normalized = normalized.replace('?','')
        normalized = normalized.replace("'",' ')
        normalized = normalized.replace('“','')
        normalized = normalized.replace('”','')
        normalized = normalized.replace("’",' ')
        normalized = normalized.replace("‘",'')
        normalized = normalized.replace("-",' ')

        normalized_list = normalized.split(' ')


        list_of_word_counts = []
        already_listed = [ 'r',  'n', 're', 've', 'ed', 'll', 'm','i', '', 'd','b', 'm'  "i", 'v', "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


        for i in normalized_list:
            if i not in already_listed and len(i) != 1 and i != search.lower():
                interlist = []
                interlist.append(i)
                already_listed.append(i)
                interlist.append(normalized.count(i))
                list_of_word_counts.append(interlist)

        sorted_list = sorted(list_of_word_counts, reverse=True, key=lambda item: item[1])




        return sorted_list

    sorted_list_nyt = find_related_words(1)
    sorted_list_bbc = find_related_words(2)
    sorted_list_fn = find_related_words(3)

    #Find related words

    all_headlines_with_search_word = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search).values('headline')

    #make string of all headlines with search word
    all_headlines_with_search_word_list = []
    for i in all_headlines_with_search_word:
        all_headlines_with_search_word_list.append(i['headline'])

    related_words_pool = " ".join(all_headlines_with_search_word_list)



    normalized = related_words_pool.lower()

    normalized = normalized.replace(':', '')
    normalized = normalized.replace(',', '')
    normalized = normalized.replace('.','')

    normalized = normalized.replace('?','')
    normalized = normalized.replace("'",' ')
    normalized = normalized.replace('“','')
    normalized = normalized.replace('”','')
    normalized = normalized.replace("’",' ')
    normalized = normalized.replace("‘",'')
    normalized = normalized.replace("-",' ')


    normalized_list = normalized.split(' ')




    list_of_word_counts = []
    already_listed = [ 'r',  'n', 're', 've', 'ed', 'll', 'm','i', '', 'd','b', 'm'  "i", 'v', "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


    for i in normalized_list:
        if i not in already_listed:
            interlist = []
            interlist.append(i)
            already_listed.append(i)
            interlist.append(normalized.count(i))
            list_of_word_counts.append(interlist)


    sorted_list = sorted(list_of_word_counts, reverse=True, key=lambda item: item[1])


    headlines_contain_search = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search)



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




    list_of_hl = []

    for i in range(0,len(all_hl_list), 4):
        interlist = []
        interlist.append(all_hl_list[i])
        interlist.append(all_hl_list[i+1])
        interlist.append(all_hl_list[i+2])
        interlist.append(all_hl_list[i + 3])
        list_of_hl.append(interlist)





    overall_search_average_query = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search).aggregate(Avg('sentiment'))
    overall_search_average = round(overall_search_average_query['sentiment__avg'] * 100,2)

    nyt_search_average_query = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search).aggregate(Avg('sentiment'))
    if nyt_search_average_query['sentiment__avg'] == None:
        nyt_search_average_query['sentiment__avg'] = 0
    nyt_search_average = round(nyt_search_average_query['sentiment__avg'] * 100,2)

    bbc_search_average_query = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search).aggregate(Avg('sentiment'))
    if bbc_search_average_query['sentiment__avg'] == None:
        bbc_search_average_query['sentiment__avg'] = 0
    bbc_search_average = round(bbc_search_average_query['sentiment__avg'] * 100,2)

    fn_search_average_query = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search).aggregate(Avg('sentiment'))
    if fn_search_average_query['sentiment__avg'] == None:
        fn_search_average_query['sentiment__avg'] = 0
    fn_search_average = round(fn_search_average_query['sentiment__avg'] * 100,2)








    #overlapping distribution for all articles by newspaper
    nyt_sentiment_all = Headline.objects.filter(newspaper=1).filter(day_order__lte=25).filter(headline__icontains=search).exclude(sentiment=0).values('sentiment')
    bbc_sentiment_all = Headline.objects.filter(newspaper=2).filter(day_order__lte=25).filter(headline__icontains=search).exclude(sentiment=0).values('sentiment')
    fn_sentiment_all = Headline.objects.filter(newspaper=3).filter(day_order__lte=25).filter(headline__icontains=search).exclude(sentiment=0).values('sentiment')


    def get_daily_average_all(queryset):
        output_list = []
        for i in queryset:
            output_list.append(float(round(i['sentiment'] * 100, 2)))
        return output_list

    nyt_curve_all = get_daily_average_all(nyt_sentiment_all)
    bbc_curve_all = get_daily_average_all(bbc_sentiment_all)
    fn_curve_all = get_daily_average_all(fn_sentiment_all)





    import plotly.figure_factory as ff

    #checking to see if search result is not empty, and then adding to list that will be used for graph. graph does not generate if a search result is empty

    hist_data_all = []
    group_labels_all = []
    colors_all = []


    if len(nyt_curve_all) > 3:
        hist_data_all.append(nyt_curve_all)
        group_labels_all.append('The New York Times')
        colors_all.append('#2d2e30')

    if len(bbc_curve_all) > 3:
        hist_data_all.append(bbc_curve_all)
        group_labels_all.append('BBC News')
        colors_all.append('#bb1919')

    if len(fn_curve_all) > 3:
        hist_data_all.append(fn_curve_all)
        group_labels_all.append('Fox News')
        colors_all.append('#006edb')



    if len(hist_data_all) > 1:

        fig_curve_all = ff.create_distplot(hist_data_all, group_labels_all, show_hist=False, colors=colors_all)
        fig_curve_all.update_layout(
                font=dict(family="Roboto",size=13,color="black"),  plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0), height=300 )


        html_div_fig_curve_all = str(plotly.offline.plot(fig_curve_all, output_type='div',config = {'displayModeBar': False},))

    else:
        html_div_fig_curve_all = '<div class="plotly-graph-div js-plotly-plot">Not enough occurrences of "'+ search + '" to plot curve</div>'

    average_sentiment_by_day = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search).annotate(Date=TruncDay('date')).values('Date').annotate(Sentiment=Avg('sentiment')).order_by('Date')
    dfosd = pd.DataFrame(list(average_sentiment_by_day))
    dfosd['Sentiment'] = dfosd['Sentiment'] * 100
    figosd = px.line(dfosd, x="Date", y="Sentiment",color_discrete_sequence=['black'] )
    figosd.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=280, plot_bgcolor='white',xaxis_title='', yaxis_title ='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




    html_divosd = str(plotly.offline.plot(figosd, output_type='div', config = {'displayModeBar': False}))



    def overall_sent_paper(paper_num, search, graph_color):
        average_sentiment_by_day = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=search).annotate(Date=TruncDay('date')).values('Date').annotate(Sentiment=Avg('sentiment')).order_by('Date')
        if len(average_sentiment_by_day) < 1:
            html_divosd = '<div class="plotly-graph-div js-plotly-plot">Not enough occurrences of search terms to plot curve</div>'
        else:
            dfosd = pd.DataFrame(list(average_sentiment_by_day))
            dfosd['Sentiment'] = dfosd['Sentiment'] * 100
            figosd = px.line(dfosd, x="Date", y="Sentiment",color_discrete_sequence=[graph_color] )
            figosd.update_layout(
                font=dict(family="Roboto",size=15,),   height=280, plot_bgcolor='white',xaxis_title='', yaxis_title ='', margin=dict(l=5, r=5, t=5, b=5, pad=10))


            figosd.update_layout(

            xaxis_tickformat = '%B',
            yaxis=dict(tickmode='auto'),

            )

            html_divosd = str(plotly.offline.plot(figosd, output_type='div', config = {'displayModeBar': False}))

        return html_divosd

    html_divosd_nyt = overall_sent_paper(1, search, '#2d2e30')
    html_divosd_bbc = overall_sent_paper(2, search, '#bb1919')
    html_divosd_fn = overall_sent_paper(3, search, '#006edb')

    average_sentiment_by_month = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search).annotate(Date=TruncMonth('date')).values('Date').annotate(Sentiment=Avg('sentiment')).order_by('Date')
    dfosm = pd.DataFrame(list(average_sentiment_by_month))
    dfosm['Sentiment'] = dfosm['Sentiment'] * 100
    figosm = px.line(dfosm, x="Date", y="Sentiment",color_discrete_sequence=['black'] )
    figosm.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=280, plot_bgcolor='white',xaxis_title='', yaxis_title ='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




    html_divosm = str(plotly.offline.plot(figosm, output_type='div', config = {'displayModeBar': False}))



    def overall_sent_paper_month(paper_num, search, graph_color):
        average_sentiment_by_day = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=search).annotate(Date=TruncMonth('date')).values('Date').annotate(Sentiment=Avg('sentiment')).order_by('Date')
        if len(average_sentiment_by_day) < 1:
            html_divosd = '<div class="plotly-graph-div js-plotly-plot">Not enough occurrences of search term to plot curve</div>'
        else:
            dfosd = pd.DataFrame(list(average_sentiment_by_day))
            dfosd['Sentiment'] = dfosd['Sentiment'] * 100
            figosd = px.line(dfosd, x="Date", y="Sentiment",color_discrete_sequence=[graph_color] )
            figosd.update_layout(
                font=dict(family="Roboto",size=15,),  height=280, plot_bgcolor='white',xaxis_title='', yaxis_title ='', margin=dict(l=5, r=5, t=5, b=5, pad=10))


            figosd.update_layout(

            xaxis_tickformat = '%B',
            yaxis=dict(tickmode='auto'),

            )

            html_divosd = str(plotly.offline.plot(figosd, output_type='div', config = {'displayModeBar': False}))

        return html_divosd


    html_divosm_nyt = overall_sent_paper_month(1, search, '#2d2e30')
    html_divosm_bbc = overall_sent_paper_month(2, search, '#bb1919')
    html_divosm_fn = overall_sent_paper_month(3, search, '#006edb')



    overall_curve_data = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search).exclude(sentiment=0).values('sentiment')

    overall_curve = get_daily_average_all(overall_curve_data)

    fig_curve_overall = ff.create_distplot([overall_curve], ['Overall'], show_hist=False, colors=['black'])
    fig_curve_overall.update_layout(
            font=dict(family="Roboto",size=13,color="black"),  plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0), height=300 )


    html_div_fig_curve_overall = str(plotly.offline.plot(fig_curve_overall, output_type='div',config = {'displayModeBar': False},))

    pos_compare_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search).filter(sentiment__gte=0)
    pos_compare_bbc = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search).filter(sentiment__gte=0)
    pos_compare_fn = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search).filter(sentiment__gte=0)

    neg_compare_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search).filter(sentiment__lte=0)
    neg_compare_bbc = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search).filter(sentiment__lte=0)
    neg_compare_fn = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search).filter(sentiment__lte=0)

    pos_y = []
    pos_y.append(len(pos_compare_nyt))
    pos_y.append(len(pos_compare_bbc))
    pos_y.append(len(pos_compare_fn))

    overall_pos_y = 0
    for countpos in pos_y:
        overall_pos_y += countpos









    neg_y = []
    neg_y.append(len(neg_compare_nyt))
    neg_y.append(len(neg_compare_bbc))
    neg_y.append(len(neg_compare_fn))

    overall_neg_y = 0
    for countneg in neg_y:
        overall_neg_y += countneg

    fig_pos_neg_compare = go.Figure(data=[
    go.Bar(name='Positive', x=['The New York Times', 'BBC News', 'Fox News'], y=pos_y, marker_color="rgb(33,102,172)"),
    go.Bar(name='Negative', x=['The New York Times', 'BBC News', 'Fox News'], y=neg_y, marker_color="rgb(178,24,43)")
    ])

    fig_pos_neg_compare.update_layout( legend={'traceorder':'normal'}, )
    fig_pos_neg_compare.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )




    html_div_fig_pos_neg = str(plotly.offline.plot(fig_pos_neg_compare, output_type='div', config = {'displayModeBar': False}))


    fig_pos_neg_overall = go.Figure(data=[
    go.Bar(name='Positive', x=['Overall'], y=[overall_pos_y], marker_color="rgb(33,102,172)"),
    go.Bar(name='Negative', x=['Overall'], y=[overall_neg_y], marker_color="rgb(178,24,43)")
    ])


    fig_pos_neg_overall.update_layout( legend={'traceorder':'normal'}, )
    fig_pos_neg_overall.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(b=0,t=0,pad=0), )




    html_div_fig_pos_neg_overall = str(plotly.offline.plot(fig_pos_neg_overall, output_type='div', config = {'displayModeBar': False}))

    if len(sorted_list_nyt) > 200:
        sorted_list_nyt = sorted_list_nyt[:200]

    if len(sorted_list_bbc) > 200:
        sorted_list_bbc = sorted_list_bbc[:200]

    if len(sorted_list_fn) > 200:
        sorted_list_fn = sorted_list_fn[:200]
    #find most co-occuring words, order those words by total count, but show count for each paper for each word
    # ex. andrew 12, 1, 3


    nyt_dict = {}
    for i in sorted_list_nyt:
        nyt_dict[i[0]] = i[1]


    bbc_dict = {}
    for i in sorted_list_bbc:
        bbc_dict[i[0]] = i[1]

    fn_dict = {}
    for i in sorted_list_fn:
        fn_dict[i[0]] = i[1]

    def dict_converter(nw_dict):
        new_list = []
        for key, value in nw_dict.items():
            new_list.append([key, value])

        new_list = sorted(new_list, key=lambda x:x[1], reverse=True)

        return new_list

    nyt_cooc = dict_converter(nyt_dict)
    bbc_cooc = dict_converter(bbc_dict)
    fn_cooc = dict_converter(fn_dict)

    if len(nyt_cooc) > 200:
        nyt_cooc = nyt_cooc[:200]

    if len(bbc_cooc) > 200:
        bbc_cooc = bbc_cooc[:200]

    if len(fn_cooc) > 200:
        fn_cooc = fn_cooc[:200]

    all_dict = {}

    for i in nyt_dict:
        if i not in all_dict:
            all_dict[i] = nyt_dict[i]
        else:
            all_dict[i] += nyt_dict[i]

    for i in bbc_dict:
        if i not in all_dict:
            all_dict[i] = bbc_dict[i]
        else:
            all_dict[i] += bbc_dict[i]

    for i in fn_dict:
        if i not in all_dict:
            all_dict[i] = fn_dict[i]
        else:
            all_dict[i] += fn_dict[i]

    dictionary_list = []
    for key, value in all_dict.items():
        dictionary_list.append([key, value])

    dictionary_list = sorted(dictionary_list, key=lambda x:x[1], reverse=True)

    final_output = []
    for i in dictionary_list:
        interlist = []
        interlist.append(i[0])
        if i[0] in nyt_dict:
            interlist.append(nyt_dict[i[0]])
        else:
            interlist.append(0)
        if i[0] in bbc_dict:
            interlist.append(bbc_dict[i[0]])
        else:
            interlist.append(0)
        if i[0] in fn_dict:
            interlist.append(fn_dict[i[0]])
        else:
            interlist.append(0)

        final_output.append(interlist)

    if len(final_output) > 200:
        final_output = final_output[:200]

    def get_curve(search, newspapernum, paper_color):

        if newspapernum == 1:
            newspaper_name = 'The New York Times'
        elif newspapernum == 2:
            newspaper_name = 'BBC News'
        elif newspapernum == 3:
            newspaper_name = 'Fox News'

        overall_curve_data_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=newspapernum).filter(headline__icontains=search).exclude(sentiment=0).values('sentiment')

        if len(overall_curve_data_nyt) < 3:
            html_div_fig_curve_nyt = '<div class="plotly-graph-div js-plotly-plot">Not enough occurrences of "'+ search + '" to plot curve</div>'

        else:
            nyt_curve = get_daily_average_all(overall_curve_data_nyt)

            singular_matrix_check = 0
            for x in nyt_curve:
                singular_matrix_check += x
            if singular_matrix_check/len(nyt_curve) == nyt_curve[0] and singular_matrix_check/len(nyt_curve) == nyt_curve[1]:
                html_div_fig_curve_nyt = '<div class="plotly-graph-div js-plotly-plot">Not enough occurrences of "'+ search + '" to plot curve</div>'

            else:


                fig_curve_nyt = ff.create_distplot([nyt_curve], [newspaper_name], show_hist=False, colors=[paper_color])
                fig_curve_nyt.update_layout(
                    font=dict(family="Roboto",size=13,color="black"),  plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0), height=300 )


                html_div_fig_curve_nyt = str(plotly.offline.plot(fig_curve_nyt, output_type='div',config = {'displayModeBar': False},))

        return html_div_fig_curve_nyt

    html_div_fig_curve_nyt = get_curve(search, 1, '#2d2e30')
    html_div_fig_curve_bbc = get_curve(search, 2, '#bb1919')
    html_div_fig_curve_fn = get_curve(search, 3, '#006edb')


    def neg_pos_chart(pos, neg, nw_name):
        pos_y_nw = len(pos)
        neg_y_nw = len(neg)


        fig_pos_neg_overall = go.Figure(data=[
        go.Bar(name='Positive', x=[nw_name], y=[pos_y_nw], marker_color="rgb(33,102,172)"),
        go.Bar(name='Negative', x=[nw_name], y=[neg_y_nw], marker_color="rgb(178,24,43)")
        ])


        fig_pos_neg_overall.update_layout( legend={'traceorder':'normal'}, )
        fig_pos_neg_overall.update_layout( font=dict(family="Roboto",size=15,color="black"),height=300, plot_bgcolor='white', orientation=90, margin=dict(b=0,t=0,pad=0), )




        html_div_fig_pos_neg_overall = str(plotly.offline.plot(fig_pos_neg_overall, output_type='div', config = {'displayModeBar': False}))


        return html_div_fig_pos_neg_overall

    html_div_fig_pos_neg_overall_nyt = neg_pos_chart(pos_compare_nyt, neg_compare_nyt, '')
    html_div_fig_pos_neg_overall_bbc = neg_pos_chart(pos_compare_bbc, neg_compare_bbc, '')
    html_div_fig_pos_neg_overall_fn = neg_pos_chart(pos_compare_fn, neg_compare_fn, '')


    def css_to_hls(calendar_data):
        for record in calendar_data:
            if record[3] > 0:
                record.append('green')
            elif record[3] < 0:
                record.append('red')
            elif record[0] == "No further headlines from this newspaper":
                record.append('gray')
            else:
                record.append('')

        return calendar_data

    list_of_hl =  css_to_hls(list_of_hl)


    return render(request, 'custom_scraper/sentiment_word_search_result.html', { 'form':form, 'search' : search, 'html_div_compare_month': html_div_compare_month, 'html_div_compare': html_div_compare, 'html_div_sentiment': html_div_sentiment, 'sorted_list': sorted_list, 'sorted_list_nyt': sorted_list_nyt,  'sorted_list_bbc': sorted_list_bbc, 'sorted_list_fn': sorted_list_fn, 'list_of_hl':list_of_hl, 'overall_search_average': overall_search_average, 'nyt_search_average': nyt_search_average, 'bbc_search_average': bbc_search_average, 'fn_search_average': fn_search_average, 'html_div_fig_curve_all': html_div_fig_curve_all, 'nyt_average':nyt_average, 'bbc_average':bbc_average, 'fn_average':fn_average, 'overall_average':overall_average, 'html_divosd': html_divosd, 'html_divosd_nyt': html_divosd_nyt, 'html_divosd_bbc': html_divosd_bbc, 'html_divosd_fn': html_divosd_fn, 'html_divosm': html_divosm, 'html_divosm_nyt': html_divosm_nyt, 'html_divosm_bbc': html_divosm_bbc, 'html_divosm_fn': html_divosm_fn, 'html_div_fig_curve_overall': html_div_fig_curve_overall, 'html_div_fig_pos_neg': html_div_fig_pos_neg, 'html_div_fig_pos_neg_overall': html_div_fig_pos_neg_overall, 'final_output':final_output,  'html_div_fig_curve_nyt': html_div_fig_curve_nyt, 'html_div_fig_curve_bbc': html_div_fig_curve_bbc, 'html_div_fig_curve_fn': html_div_fig_curve_fn, 'html_div_fig_pos_neg_overall_nyt': html_div_fig_pos_neg_overall_nyt,  'html_div_fig_pos_neg_overall_bbc': html_div_fig_pos_neg_overall_bbc, 'html_div_fig_pos_neg_overall_fn': html_div_fig_pos_neg_overall_fn, 'nyt_cooc': nyt_cooc, 'bbc_cooc': bbc_cooc, 'fn_cooc': fn_cooc  } )



def sent_compare_search(request):
    form1 = CompareSearch1()


    form2 = CompareSearch2()


    import plotly.graph_objects as go

    from datetime import datetime

    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today = str(today)[:10]
    yesterday = str(yesterday)[:10]


    if not Headline.objects.filter(date__contains=today).values('headline'):
        today = yesterday


    top_10_words_terms = word_count_general.objects.filter(newspaper=4).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:9]
    test_terms = []
    test_overall_values_list = []
    for i in top_10_words_terms:
        test_terms.append(i['word'])
        test_overall_values_list.append(i['word_count'])



    test_values_list = []

    for i in range(1,4):
        newspaper_values = []
        for y in test_terms:
            all_test_values = word_count_general.objects.filter(date__contains=today).filter(newspaper=i).filter(word=y).values('word_count')
            for record in all_test_values:
                newspaper_values.append(record['word_count'])
        test_values_list.append(newspaper_values)






    test_ny_values_list = test_values_list[0]
    test_bbc_values_list = test_values_list[1]
    test_fn_values_list = test_values_list[2]




    values_fig = go.Figure(data=[
        go.Bar(name='New York Times', y=test_terms, x=test_ny_values_list, orientation='h', marker_color="#2d2e30"),
        go.Bar(name='BBC News', y=test_terms, x=test_bbc_values_list, orientation = 'h', marker_color="#bb1919"),
        go.Bar(name='Fox News', y=test_terms, x=test_fn_values_list, orientation = 'h', marker_color="rgba(0,51,102,.99)"),
    ], )
    values_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), height=400, plot_bgcolor='white', orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))

    most_variance_words = []

    today_var_word = date.today()
    from custom_scraper.models import variance_table_word

    variance_words = variance_table_word.objects.filter(graphid=10).filter(date__contains=today_var_word).values('word', 'count', 'news1', 'news2', 'sentiment')

    for i in variance_words:
        interlist = []
        interlist.append(i['word'])
        interlist.append(i['count'])
        interlist.append(i['news1'])
        interlist.append(i['news2'])
        interlist.append(round(i['sentiment'],2))
        most_variance_words.append(interlist)

    most_popular_words = []
    most_popular_query = word_count_general.objects.filter(date__contains=today).filter(newspaper=4).values('word')[:150]
    for record in most_popular_query:
        most_popular_words.append(record['word'])








    return render(request, 'custom_scraper/sent_compare_search.html',{'form1':form1, 'form2':form2, 'html_div_values': html_div_values, 'most_variance_words': most_variance_words, 'most_popular_words': most_popular_words   } )


def sent_compare_search_result(request):

    form1 = CompareSearch1()


    form2 = CompareSearch2()

    search1 = request.GET.get('compare1')


    search2 = request.GET.get('compare2')


    key1data = Headline.objects.filter(headline__icontains=search1)
    key2data = Headline.objects.filter(headline__icontains=search2)

    from django.shortcuts import redirect
    if not key1data or len(key1data) < 3 or not key2data or len(key2data) < 3:
        request.session['search1'] = search1
        request.session['search2'] = search2



        return redirect('research_sent')


    import plotly.graph_objects as go
    animals=['The New York Times', 'BBC News', 'Fox News']

    search1_overall_sent_by_paper = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).values('newspaper').annotate(Average=Avg('sentiment'))

    search1_list = []
    in_newspaper = False
    for record in search1_overall_sent_by_paper:

        if record['newspaper'] == 1:
            search1_list.append(record)
            in_newspaper = True
    if in_newspaper == False:
        search1_list.append({'newspaper':1, 'Average':0})

    in_newspaper = False

    for record in search1_overall_sent_by_paper:
        if record['newspaper'] == 2:
            search1_list.append(record)
            in_newspaper = True
    if in_newspaper == False:
        search1_list.append({'newspaper':2, 'Average':0})

    in_newspaper = False

    for record in search1_overall_sent_by_paper:
        if record['newspaper'] == 3:
            search1_list.append(record)
            in_newspaper = True
    if in_newspaper == False:
        search1_list.append({'newspaper':3, 'Average':0})


    search1_y = []


    for i in search1_list:
        search1_y.append(round(i['Average'] * 100, 2))


    search2_list = []


    search2_overall_sent_by_paper = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).values('newspaper').annotate(Average=Avg('sentiment'))
    in_newspaper = False
    for record in search2_overall_sent_by_paper:

        if record['newspaper'] == 1:
            search2_list.append(record)
            in_newspaper = True

    if in_newspaper == False:
        search2_list.append({'newspaper':1, 'Average':0})

    in_newspaper = False
    for record in search2_overall_sent_by_paper:

        if record['newspaper'] == 2:
            search2_list.append(record)
            in_newspaper = True

    if in_newspaper == False:
        search2_list.append({'newspaper':2, 'Average':0})


    in_newspaper = False
    for record in search2_overall_sent_by_paper:

        if record['newspaper'] == 3:
            search2_list.append(record)
            in_newspaper = True
    if in_newspaper == False:
        search2_list.append({'newspaper':3, 'Average':0})




    search2_y = []

    for i in search2_list:
        search2_y.append(round(i['Average'] * 100, 2))




    fig = go.Figure(data=[
        go.Bar(name=search1, x=animals, y=search1_y),
        go.Bar(name=search2, x=animals, y=search2_y)
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')



    fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white',orientation=90, )

    html_div_sentiment = str(plotly.offline.plot(fig, output_type='div', config = {'displayModeBar': False}))



    from django.db.models import CharField, Value


    average_sentiment_by_date_compare_month_search1 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).annotate(Date=TruncMonth('date')).annotate(Word=Value(search1, output_field=CharField())).values('Word','Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by("Date",)
    average_sentiment_by_date_compare_month_search2 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).annotate(Date=TruncMonth('date')).annotate(Word=Value(search2, output_field=CharField())).values('Word','Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by("Date",)

    from itertools import chain
    result_list = list(chain(average_sentiment_by_date_compare_month_search1, average_sentiment_by_date_compare_month_search2))


    for i in result_list:
        if i['newspaper'] == 3:
            i['Word'] += ' -  Fox News'
        elif i['newspaper'] == 2:
            i['Word'] += ' -  BBC News'
        elif i['newspaper'] == 1:
            i['Word'] += ' -  The New York Times'


    comparesent_month = pd.DataFrame(list(result_list))



    comparesent_month['Average'] = comparesent_month['Average'] * 100
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(1, 'The New York Times')
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(2, 'BBC News')
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(3, 'Fox News')
    comparesent_month.rename(columns={'newspaper':'Newspaper'}, inplace= True)


    figcompare_month = px.line(comparesent_month, x="Date", y="Average", color="Word",   )


    figcompare_month.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0))



    html_div_compare_month = str(plotly.offline.plot(figcompare_month, output_type='div', config = {'displayModeBar': False}))






    average_sentiment_by_date_compare_search1 = Headline.objects.filter(day_order__lte=25).filter(day_order__lte=25).filter(headline__icontains=search1).annotate(Date=TruncDay('date')).annotate(Word=Value(search1, output_field=CharField())).values('Word','Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by("Date",)
    average_sentiment_by_date_compare_search2 = Headline.objects.filter(day_order__lte=25).filter(day_order__lte=25).filter(headline__icontains=search2).annotate(Date=TruncDay('date')).annotate(Word=Value(search2, output_field=CharField())).values('Word','Date', 'newspaper').annotate(Average=Avg('sentiment')).order_by("Date",)


    from itertools import chain
    result_list_date = list(chain(average_sentiment_by_date_compare_search1, average_sentiment_by_date_compare_search2))


    for i in result_list_date:
        if i['newspaper'] == 3:
            i['Word'] += ' -  Fox News'
        elif i['newspaper'] == 2:
            i['Word'] += ' -  BBC News'
        elif i['newspaper'] == 1:
            i['Word'] += ' -  The New York Times'


    comparesent_date = pd.DataFrame(list(result_list_date))




    comparesent_date['Average'] = comparesent_date['Average'] * 100
    comparesent_date['newspaper'] = comparesent_date['newspaper'].replace(1, 'The New York Times')
    comparesent_date['newspaper'] = comparesent_date['newspaper'].replace(2, 'BBC News')
    comparesent_date['newspaper'] = comparesent_date['newspaper'].replace(3, 'Fox News')
    comparesent_date.rename(columns={'newspaper':'Newspaper'}, inplace= True)


    figcompare_date = px.line(comparesent_date, x="Date", y="Average", color="Word",  )


    figcompare_date.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))

    figcompare_date.update_layout(
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


    html_div_compare_date = str(plotly.offline.plot(figcompare_date, output_type='div', config = {'displayModeBar': False}))


    overall_sentiment_search1 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).exclude(sentiment=0).values('sentiment')

    overall_sentiment_search2 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).exclude(sentiment=0).values('sentiment')




    #overlapping distribution for all articles by newspaper
    nyt_sentiment_search1 = Headline.objects.filter(newspaper=1).filter(day_order__lte=25).filter(headline__icontains=search1).exclude(sentiment=0).values('sentiment')
    bbc_sentiment_search1 = Headline.objects.filter(newspaper=2).filter(day_order__lte=25).filter(headline__icontains=search1).exclude(sentiment=0).values('sentiment')
    fn_sentiment_search1 = Headline.objects.filter(newspaper=3).filter(day_order__lte=25).filter(headline__icontains=search1).exclude(sentiment=0).values('sentiment')
    nyt_sentiment_search2 = Headline.objects.filter(newspaper=1).filter(day_order__lte=25).filter(headline__icontains=search2).exclude(sentiment=0).values('sentiment')
    bbc_sentiment_search2 = Headline.objects.filter(newspaper=2).filter(day_order__lte=25).filter(headline__icontains=search2).exclude(sentiment=0).values('sentiment')
    fn_sentiment_search2 = Headline.objects.filter(newspaper=3).filter(day_order__lte=25).filter(headline__icontains=search2).exclude(sentiment=0).values('sentiment')

    def get_daily_average_all(queryset):
        output_list = []
        for i in queryset:
            output_list.append(float(round(i['sentiment'] * 100, 2)))
        return output_list

    nyt_curve_1 = get_daily_average_all(nyt_sentiment_search1)
    bbc_curve_1 = get_daily_average_all(bbc_sentiment_search1)
    fn_curve_1 = get_daily_average_all(fn_sentiment_search1)
    nyt_curve_2 = get_daily_average_all(nyt_sentiment_search2)
    bbc_curve_2 = get_daily_average_all(bbc_sentiment_search2)
    fn_curve_2 = get_daily_average_all(fn_sentiment_search2)




    import plotly.figure_factory as ff

    #checking to see if search result is not empty, and then adding to list that will be used for graph. graph does not generate if a search result is empty

    hist_data_all = []
    group_labels_all = []
    colors_all = []


    if len(nyt_curve_1) > 3:
        hist_data_all.append(nyt_curve_1)
        group_labels_all.append(search1 + ' - The New York Times')


    if len(bbc_curve_1) > 3:
        hist_data_all.append(bbc_curve_1)
        group_labels_all.append(search1 + ' - BBC News')


    if len(fn_curve_1) > 3:
        hist_data_all.append(fn_curve_1)
        group_labels_all.append(search1 + ' - Fox News')

    if len(nyt_curve_2) > 3:
        hist_data_all.append(nyt_curve_2)
        group_labels_all.append(search2 + ' - The New York Times')


    if len(bbc_curve_2) > 3:
        hist_data_all.append(bbc_curve_2)
        group_labels_all.append(search2 + ' - BBC News')


    if len(fn_curve_2) > 3:
        hist_data_all.append(fn_curve_2)
        group_labels_all.append(search2 + ' - Fox News')




    fig_curve_all = ff.create_distplot(hist_data_all, group_labels_all, show_hist=False, )
    fig_curve_all.update_layout(
            font=dict(family="Roboto",size=13,color="black"),  plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0), height=400 )

    html_div_fig_curve_all = str(plotly.offline.plot(fig_curve_all, output_type='div',config = {'displayModeBar': False},))



    overall_sentiment_search1 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).exclude(sentiment=0).values('sentiment')

    overall_sentiment_search2 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).exclude(sentiment=0).values('sentiment')

    overall_curve_1 = get_daily_average_all(overall_sentiment_search1)
    overall_curve_2 = get_daily_average_all(overall_sentiment_search2)


    hist_data_overall = []
    group_labels_overall = []
    colors_overall = []


    if len(overall_curve_1) < 3 and len(overall_curve_2) < 3:
        html_div_fig_curve_overall = '<div class="plotly-graph-div js-plotly-plot">Not enough occurrences of search terms to plot curve</div>'
    else:
        if len(overall_curve_1) > 3:
            hist_data_overall.append(overall_curve_1)
            group_labels_overall.append(search1)


        if len(overall_curve_2) > 3:
            hist_data_overall.append(overall_curve_2)
            group_labels_overall.append(search2)

            fig_curve_overall = ff.create_distplot(hist_data_overall, group_labels_overall, show_hist=False, )
            fig_curve_overall.update_layout(
            font=dict(family="Roboto",size=13,color="black"),  plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0), height=400 )

        html_div_fig_curve_overall = str(plotly.offline.plot(fig_curve_overall, output_type='div',config = {'displayModeBar': False},))


    def get_dist_curve_by_paper(search_term1, search_term2, newspaper_num):
        overall_sentiment_search1 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search_term1).filter(newspaper=newspaper_num).exclude(sentiment=0).values('sentiment')

        overall_sentiment_search2 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search_term2).filter(newspaper=newspaper_num).exclude(sentiment=0).values('sentiment')

        overall_curve_1 = get_daily_average_all(overall_sentiment_search1)
        overall_curve_2 = get_daily_average_all(overall_sentiment_search2)


        hist_data_overall = []
        group_labels_overall = []
        colors_overall = []


        if len(overall_curve_1) < 3 or len(overall_curve_2) < 3:
            html_div_fig_curve_overall = '<div class="plotly-graph-div js-plotly-plot">Not enough occurrences of search terms to plot curve</div>'
        else:
            if len(overall_curve_1) > 3:
                hist_data_overall.append(overall_curve_1)
                group_labels_overall.append(search_term1)


            if len(overall_curve_2) > 3:
                hist_data_overall.append(overall_curve_2)
                group_labels_overall.append(search_term2)

            fig_curve_overall = ff.create_distplot(hist_data_overall, group_labels_overall, show_hist=False, )
            fig_curve_overall.update_layout(
            font=dict(family="Roboto",size=13,color="black"),  plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0, pad=0), height=400 )

            html_div_fig_curve_overall = str(plotly.offline.plot(fig_curve_overall, output_type='div',config = {'displayModeBar': False},))

        return html_div_fig_curve_overall

    html_div_fig_curve_nyt = get_dist_curve_by_paper(search1, search2, 1)
    html_div_fig_curve_bbc = get_dist_curve_by_paper(search1, search2, 2)
    html_div_fig_curve_fn = get_dist_curve_by_paper(search1, search2, 3)









    def find_related_words(papernumber, search_term):
        #Find related words

        all_headlines_with_search_word = Headline.objects.filter(newspaper=papernumber).filter(day_order__lte=25).filter(headline__icontains=search_term).values('headline')

        #make string of all headlines with search word
        all_headlines_with_search_word_list = []
        for i in all_headlines_with_search_word:
            all_headlines_with_search_word_list.append(i['headline'])

        related_words_pool = " ".join(all_headlines_with_search_word_list)


        normalized = related_words_pool.lower()

        normalized = normalized.replace(':', '')
        normalized = normalized.replace(',', '')
        normalized = normalized.replace('.','')

        normalized = normalized.replace('?','')
        normalized = normalized.replace("'",' ')
        normalized = normalized.replace('“','')
        normalized = normalized.replace('”','')
        normalized = normalized.replace("’",' ')
        normalized = normalized.replace("‘",'')
        normalized = normalized.replace("-",' ')

        normalized_list = normalized.split(' ')



        list_of_word_counts = []
        already_listed = [ 'r',  'n', 're', 've', 'ed', 'll', 'm','i', '', 'd','b', 'm'  "i", 'v', "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


        for i in normalized_list:
            if i not in already_listed and len(i) != 1 and i != search_term.lower():
                interlist = []
                interlist.append(i)
                already_listed.append(i)
                interlist.append(normalized.count(i))
                list_of_word_counts.append(interlist)

        sorted_list = sorted(list_of_word_counts, reverse=True, key=lambda item: item[1])




        return sorted_list

    sorted_list_nyt_search1 = find_related_words(1, search1)
    sorted_list_bbc_search1 = find_related_words(2, search1)
    sorted_list_fn_search1 = find_related_words(3, search1)
    sorted_list_nyt_search2 = find_related_words(1, search2)
    sorted_list_bbc_search2 = find_related_words(2, search2)
    sorted_list_fn_search2 = find_related_words(3, search2)

    def limit_sorted_list(sorted_list_var):
        if len(sorted_list_var) > 300:
            sorted_list_var = sorted_list_var[:300]
        return sorted_list_var

    sorted_list_nyt_search1 = limit_sorted_list(sorted_list_nyt_search1)
    sorted_list_nyt_search2 = limit_sorted_list(sorted_list_nyt_search2)

    sorted_list_bbc_search1 = limit_sorted_list(sorted_list_bbc_search1)
    sorted_list_bbc_search2 = limit_sorted_list(sorted_list_bbc_search2)

    sorted_list_fn_search1 = limit_sorted_list(sorted_list_fn_search1)
    sorted_list_fn_search2 = limit_sorted_list(sorted_list_fn_search2)


    search1_headlines_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search1).values('headline', 'date', 'sentiment', 'link')
    search1_headlines_bbc = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search1).values('headline', 'date', 'sentiment', 'link')
    search1_headlines_fn = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search1).values('headline', 'date', 'sentiment', 'link')

    search2_headlines_nyt = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search2).values('headline', 'date', 'sentiment', 'link')
    search2_headlines_bbc = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search2).values('headline', 'date', 'sentiment', 'link')
    search2_headlines_fn = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search2).values('headline', 'date', 'sentiment', 'link')


    def djq_to_list(query):
        output_list = []

        for i in query:
            interlist = []
            interlist.append(i['headline'])
            interlist.append(i['date'])
            interlist.append(round(i['sentiment']*100,1))
            interlist.append(i['link'])
            output_list.append(interlist)

        return output_list



    nyt_small_hl = djq_to_list(search1_headlines_nyt)
    bbc_small_hl = djq_to_list(search1_headlines_bbc)
    fn_small_hl = djq_to_list(search1_headlines_fn)

    nyt_small_hl_2 = djq_to_list(search2_headlines_nyt)
    bbc_small_hl_2 = djq_to_list(search2_headlines_bbc)
    fn_small_hl_2 = djq_to_list(search2_headlines_fn)

    def css_to_hls(calendar_data):
        for record in calendar_data:
            if record[2] > 0:
                record.append('green')
            elif record[2] < 0:
                record.append('red')

            else:
                record.append('small_hl_box')

        return calendar_data


    nyt_small_hl = css_to_hls(nyt_small_hl)
    nyt_small_hl_2 = css_to_hls(nyt_small_hl_2)



    bbc_small_hl = css_to_hls(bbc_small_hl)
    bbc_small_hl_2 = css_to_hls(bbc_small_hl_2)



    fn_small_hl = css_to_hls(fn_small_hl)
    fn_small_hl_2 = css_to_hls(fn_small_hl_2)



    searches = []
    searches.append(search1)
    searches.append(search2)

    overall_average_sent_search1 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).aggregate(Avg('sentiment'))
    overall_average_sent_search2 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).aggregate(Avg('sentiment'))


    y_averages = []
    y_averages.append(round(overall_average_sent_search1['sentiment__avg']*100,2))
    y_averages.append(round(overall_average_sent_search2['sentiment__avg']*100,2))



    fig_avg_searches = go.Figure([go.Bar(x=searches, y=y_averages, marker_color=['#636efa', '#ef553b'])])

    fig_avg_searches.update_layout(barmode='group')



    fig_avg_searches.update_layout(
       font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white',orientation=90, margin=dict(l=50, r=50, t=0, b=30, pad=0) )

    html_div_sentiment_overall = str(plotly.offline.plot(fig_avg_searches, output_type='div', config = {'displayModeBar': False}))


    def newspaper_div_sentiment(first_search, second_search, newspaper_num):

        searches = []
        searches.append(first_search)
        searches.append(second_search)

        overall_average_sent_search1 = Headline.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(headline__icontains=first_search).aggregate(Avg('sentiment'))
        overall_average_sent_search2 = Headline.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(headline__icontains=second_search).aggregate(Avg('sentiment'))

        if overall_average_sent_search1['sentiment__avg'] == None:
            overall_average_sent_search1['sentiment__avg'] = 0
        if overall_average_sent_search2['sentiment__avg'] == None:
            overall_average_sent_search2['sentiment__avg'] = 0



        y_averages = []
        y_averages.append(round(overall_average_sent_search1['sentiment__avg']*100,2))
        y_averages.append(round(overall_average_sent_search2['sentiment__avg']*100,2))



        fig_avg_searches = go.Figure([go.Bar(x=searches, y=y_averages, marker_color=['#636efa', '#ef553b'])])

        fig_avg_searches.update_layout(barmode='group')



        fig_avg_searches.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, margin=dict(l=50, r=50, t=0, b=30, pad=0),plot_bgcolor='white',orientation=90, )

        html_div_sentiment_overall = str(plotly.offline.plot(fig_avg_searches, output_type='div', config = {'displayModeBar': False}))

        return html_div_sentiment_overall

    html_div_sentiment_nyt = newspaper_div_sentiment(search1, search2, 1)
    html_div_sentiment_bbc = newspaper_div_sentiment(search1, search2, 2)
    html_div_sentiment_fn = newspaper_div_sentiment(search1, search2, 3)



    average_sentiment_by_date_compare_month_search1 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).annotate(Date=TruncMonth('date')).annotate(Word=Value(search1, output_field=CharField())).values('Word','Date', ).annotate(Average=Avg('sentiment')).order_by("Date",)
    average_sentiment_by_date_compare_month_search2 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).annotate(Date=TruncMonth('date')).annotate(Word=Value(search2, output_field=CharField())).values('Word','Date', ).annotate(Average=Avg('sentiment')).order_by("Date",)

    from itertools import chain
    result_list = list(chain(average_sentiment_by_date_compare_month_search1, average_sentiment_by_date_compare_month_search2))






    comparesent_month = pd.DataFrame(list(result_list))



    comparesent_month['Average'] = comparesent_month['Average'] * 100



    figcompare_month = px.line(comparesent_month, x="Date", y="Average", color="Word",  )


    figcompare_month.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0))



    html_div_compare_month_overall = str(plotly.offline.plot(figcompare_month, output_type='div', config = {'displayModeBar': False}))

    def get_monthly_search1(papernum, search_term1, search_term2):
        average_sentiment_by_date_compare_month_search1 = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum).filter(headline__icontains=search_term1).annotate(Date=TruncMonth('date')).annotate(Word=Value(search_term1, output_field=CharField())).values('Word','Date', ).annotate(Average=Avg('sentiment')).order_by("Date",)
        average_sentiment_by_date_compare_month_search2 = Headline.objects.filter(day_order__lte=25).filter(newspaper=papernum).filter(headline__icontains=search_term2).annotate(Date=TruncMonth('date')).annotate(Word=Value(search_term2, output_field=CharField())).values('Word','Date', ).annotate(Average=Avg('sentiment')).order_by("Date",)

        from itertools import chain
        result_list = list(chain(average_sentiment_by_date_compare_month_search1, average_sentiment_by_date_compare_month_search2))





        comparesent_month = pd.DataFrame(list(result_list))



        comparesent_month['Average'] = comparesent_month['Average'] * 100



        figcompare_month = px.line(comparesent_month, x="Date", y="Average", color="Word",  )


        figcompare_month.update_layout(
            font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0))



        html_div_compare_month_overall = str(plotly.offline.plot(figcompare_month, output_type='div', config = {'displayModeBar': False}))


        return html_div_compare_month_overall

    html_div_compare_month_nyt = get_monthly_search1(1, search1, search2)
    html_div_compare_month_bbc = get_monthly_search1(2, search1, search2)
    html_div_compare_month_fn = get_monthly_search1(3, search1, search2)



    average_sentiment_by_date_compare_search1_overall = Headline.objects.filter(day_order__lte=25).filter(day_order__lte=25).filter(headline__icontains=search1).annotate(Date=TruncDay('date')).annotate(Word=Value(search1, output_field=CharField())).values('Word','Date', ).annotate(Average=Avg('sentiment')).order_by("Date",)
    average_sentiment_by_date_compare_search2_overall = Headline.objects.filter(day_order__lte=25).filter(day_order__lte=25).filter(headline__icontains=search2).annotate(Date=TruncDay('date')).annotate(Word=Value(search2, output_field=CharField())).values('Word','Date', ).annotate(Average=Avg('sentiment')).order_by("Date",)


    from itertools import chain
    result_list_date_overall = list(chain(average_sentiment_by_date_compare_search1_overall, average_sentiment_by_date_compare_search2_overall))





    comparesent_date_overall = pd.DataFrame(list(result_list_date_overall))




    comparesent_date_overall['Average'] = comparesent_date_overall['Average'] * 100


    figcompare_date_overall = px.line(comparesent_date_overall, x="Date", y="Average", color="Word",  )


    figcompare_date_overall.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))

    figcompare_date_overall.update_layout(
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


    html_div_compare_date_overall = str(plotly.offline.plot(figcompare_date_overall, output_type='div', config = {'displayModeBar': False}))



    def get_date_search1(papernum, search_term1, search_term2):
        average_sentiment_by_date_compare_search1 = Headline.objects.filter(day_order__lte=25).filter(day_order__lte=25).filter(newspaper=papernum).filter(headline__icontains=search_term1).annotate(Date=TruncDay('date')).annotate(Word=Value(search_term1, output_field=CharField())).values('Word','Date', ).annotate(Average=Avg('sentiment')).order_by("Date",)
        average_sentiment_by_date_compare_search2 = Headline.objects.filter(day_order__lte=25).filter(day_order__lte=25).filter(newspaper=papernum).filter(headline__icontains=search_term2).annotate(Date=TruncDay('date')).annotate(Word=Value(search_term2, output_field=CharField())).values('Word','Date', ).annotate(Average=Avg('sentiment')).order_by("Date",)


        from itertools import chain
        result_list_date = list(chain(average_sentiment_by_date_compare_search1, average_sentiment_by_date_compare_search2))






        comparesent_date = pd.DataFrame(list(result_list_date))




        comparesent_date['Average'] = comparesent_date['Average'] * 100



        figcompare_date = px.line(comparesent_date, x="Date", y="Average", color="Word",  )


        figcompare_date.update_layout(
            font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))

        figcompare_date.update_layout(
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


        html_div_compare_date = str(plotly.offline.plot(figcompare_date, output_type='div', config = {'displayModeBar': False}))

        return html_div_compare_date


    html_div_compare_date_nyt = get_date_search1(1, search1, search2)
    html_div_compare_date_bbc = get_date_search1(2, search1, search2)
    html_div_compare_date_fn = get_date_search1(3, search1, search2)


    search1_pos = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(sentiment__gt=0).values('sentiment')
    search1_neg = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(sentiment__lt=0).values('sentiment')
    search2_pos = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(sentiment__gt=0).values('sentiment')
    search2_neg = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(sentiment__lt=0).values('sentiment')

    pos_y_searches = []
    pos_y_searches.append(len(search1_pos))
    pos_y_searches.append(len(search2_pos))

    neg_y_searches = []
    neg_y_searches.append(len(search1_neg))
    neg_y_searches.append(len(search2_neg))


    fig_pos_neg_compare = go.Figure(data=[
    go.Bar(name='Positive', x=[search1, search2], y=pos_y_searches, marker_color="rgb(33,102,172)"),
    go.Bar(name='Negative', x=[search1, search2], y=neg_y_searches, marker_color="rgb(178,24,43)")
    ])

    fig_pos_neg_compare.update_layout( legend={'traceorder':'normal'}, )
    fig_pos_neg_compare.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )




    html_div_fig_pos_neg = str(plotly.offline.plot(fig_pos_neg_compare, output_type='div', config = {'displayModeBar': False}))


    def get_pos_neg_by_paper(search_term1, search_term2, paper_num):

        search1_pos = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=search_term1).filter(sentiment__gt=0).values('sentiment')
        search1_neg = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=search_term1).filter(sentiment__lt=0).values('sentiment')
        search2_pos = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=search_term2).filter(sentiment__gt=0).values('sentiment')
        search2_neg = Headline.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(headline__icontains=search_term2).filter(sentiment__lt=0).values('sentiment')

        pos_y_searches = []
        pos_y_searches.append(len(search1_pos))
        pos_y_searches.append(len(search2_pos))

        neg_y_searches = []
        neg_y_searches.append(len(search1_neg))
        neg_y_searches.append(len(search2_neg))


        fig_pos_neg_compare = go.Figure(data=[
        go.Bar(name='Positive', x=[search1, search2], y=pos_y_searches, marker_color="rgb(33,102,172)"),
        go.Bar(name='Negative', x=[search1, search2], y=neg_y_searches, marker_color="rgb(178,24,43)")
        ])

        fig_pos_neg_compare.update_layout( legend={'traceorder':'normal'}, )
        fig_pos_neg_compare.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )




        html_div_fig_pos_neg = str(plotly.offline.plot(fig_pos_neg_compare, output_type='div', config = {'displayModeBar': False}))

        return html_div_fig_pos_neg

    html_div_fig_pos_neg_nyt = get_pos_neg_by_paper(search1, search2, 1)
    html_div_fig_pos_neg_bbc = get_pos_neg_by_paper(search1, search2, 2)
    html_div_fig_pos_neg_fn = get_pos_neg_by_paper(search1, search2, 3)

    sorted_list_nyt_search1
    sorted_list_bbc_search1
    sorted_list_fn_search1
    sorted_list_nyt_search2
    sorted_list_bbc_search2
    sorted_list_fn_search2

    def convert_to_dict(sorted_list):
        new_dict_output = {}
        for i in sorted_list:
            new_dict_output[i[0]] = i[1]
        return new_dict_output

    nyt_rw_dict_1 = convert_to_dict(sorted_list_nyt_search1)
    nyt_rw_dict_2 = convert_to_dict(sorted_list_nyt_search2)

    bbc_rw_dict_1 = convert_to_dict(sorted_list_bbc_search1)
    bbc_rw_dict_2 = convert_to_dict(sorted_list_bbc_search2)

    fn_rw_dict_1 = convert_to_dict(sorted_list_fn_search1)
    fn_rw_dict_2 = convert_to_dict(sorted_list_fn_search2)

    overall_dict_1 = {}

    for i in nyt_rw_dict_1:
        if i in overall_dict_1:
            overall_dict_1[i] += nyt_rw_dict_1[i]
        else:
            overall_dict_1[i] = nyt_rw_dict_1[i]

    for i in bbc_rw_dict_1:
        if i in overall_dict_1:
            overall_dict_1[i] += bbc_rw_dict_1[i]
        else:
            overall_dict_1[i] = bbc_rw_dict_1[i]

    for i in fn_rw_dict_1:
        if i in overall_dict_1:
            overall_dict_1[i] += fn_rw_dict_1[i]
        else:
            overall_dict_1[i] = fn_rw_dict_1[i]



    overall_dict_2 = {}

    for i in nyt_rw_dict_2:
        if i in overall_dict_2:
            overall_dict_2[i] += nyt_rw_dict_2[i]
        else:
            overall_dict_2[i] = nyt_rw_dict_2[i]

    for i in bbc_rw_dict_2:
        if i in overall_dict_2:
            overall_dict_2[i] += bbc_rw_dict_2[i]
        else:
            overall_dict_2[i] = bbc_rw_dict_2[i]

    for i in fn_rw_dict_2:
        if i in overall_dict_2:
            overall_dict_2[i] += fn_rw_dict_2[i]
        else:
            overall_dict_2[i] = fn_rw_dict_2[i]

    overall_dict_list_1 = []
    for x, y in overall_dict_1.items():
        interlist = []
        interlist.append(x)
        interlist.append(y)
        overall_dict_list_1.append(interlist)

    overall_dict_list_2 = []
    for x, y in overall_dict_2.items():
        interlist = []
        interlist.append(x)
        interlist.append(y)
        overall_dict_list_2.append(interlist)








    sorted_overall_dict_list_1 = sorted(overall_dict_list_1, key=lambda x:x[1], reverse=True)
    sorted_overall_dict_list_2 = sorted(overall_dict_list_2, key=lambda x:x[1], reverse=True)


    return render(request, 'custom_scraper/sent_compare_search_result.html',{'search1':search1, 'search2':search2, 'form1':form1, 'form2':form2, 'html_div_sentiment': html_div_sentiment, 'html_div_compare_month': html_div_compare_month, 'html_div_compare_date': html_div_compare_date, 'html_div_fig_curve_all': html_div_fig_curve_all, 'sorted_list_nyt_search1': sorted_list_nyt_search1, 'sorted_list_bbc_search1': sorted_list_bbc_search1, 'sorted_list_fn_search1': sorted_list_fn_search1, 'sorted_list_nyt_search2': sorted_list_nyt_search2, 'sorted_list_bbc_search2': sorted_list_bbc_search2, 'sorted_list_fn_search2': sorted_list_fn_search2,  'search1_headlines_nyt': search1_headlines_nyt, 'nyt_small_hl': nyt_small_hl, 'bbc_small_hl': bbc_small_hl, 'fn_small_hl': fn_small_hl, 'nyt_small_hl_2': nyt_small_hl_2, 'bbc_small_hl_2': bbc_small_hl_2, 'fn_small_hl_2': fn_small_hl_2, 'html_div_sentiment_overall': html_div_sentiment_overall, 'html_div_sentiment_nyt': html_div_sentiment_nyt, 'html_div_sentiment_bbc': html_div_sentiment_bbc, 'html_div_sentiment_fn': html_div_sentiment_fn, 'html_div_compare_month_overall': html_div_compare_month_overall, 'html_div_compare_month_nyt': html_div_compare_month_nyt, 'html_div_compare_month_bbc': html_div_compare_month_bbc, 'html_div_compare_month_fn': html_div_compare_month_fn, 'html_div_compare_date_overall': html_div_compare_date_overall, 'html_div_compare_date_nyt': html_div_compare_date_nyt, 'html_div_compare_date_bbc': html_div_compare_date_bbc, 'html_div_compare_date_fn': html_div_compare_date_fn, 'html_div_fig_curve_overall': html_div_fig_curve_overall, 'html_div_fig_pos_neg': html_div_fig_pos_neg, 'html_div_fig_pos_neg_nyt': html_div_fig_pos_neg_nyt, 'html_div_fig_pos_neg_bbc': html_div_fig_pos_neg_bbc, 'html_div_fig_pos_neg_fn': html_div_fig_pos_neg_fn, 'sorted_overall_dict_list_1': sorted_overall_dict_list_1, 'sorted_overall_dict_list_2': sorted_overall_dict_list_2, 'html_div_fig_curve_nyt': html_div_fig_curve_nyt, 'html_div_fig_curve_bbc': html_div_fig_curve_bbc, 'html_div_fig_curve_fn': html_div_fig_curve_fn  } )



def research_sent(request):

    form1 = CompareSearch1()

    search1 = request.session['search1']
    search2 = request.session['search2']



    return render(request, 'custom_scraper/research_sent.html',{'form1':form1, 'search1':search1, 'search2':search2},)


def research_emotion_compare(request):

    form1 = CompareSearch1()

    search1 = request.session['search1']
    search2 = request.session['search2']



    return render(request, 'custom_scraper/research_emotion_compare.html',{'form1':form1, 'search1':search1, 'search2':search2},)

def research_emotion_compare_single(request):

    form1 = CompareSearchSingle()

    search1 = request.session['search1']
    search2 = request.session['search2']



    return render(request, 'custom_scraper/research_emotion_compare_single.html',{'form1':form1, 'search1':search1,'search2':search2},)



def word_count_general_og(request):
    from datetime import datetime

    today = datetime.today()
    yesterday = today - timedelta(1)
    today = str(today)[:10]

    yesterday = str(yesterday)[:10]
    cached = False

    if html_cache.objects.filter(date__contains=today).filter(page_num=1):
        html_record = html_cache.objects.filter(date__contains=today).filter(page_num=1).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/word_count_general_og.html',{'html':html, 'cached':cached},)

    if html_cache.objects.filter(date__contains=yesterday).filter(page_num=1):
        html_record = html_cache.objects.filter(date__contains=yesterday).filter(page_num=1).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/word_count_general_og.html',{'html':html, 'cached':cached},)









    if not Headline.objects.filter(date__contains=today).values('headline'):
        today = datetime.today()
        today = today - timedelta(days=1)
        today = str(today)[:10]



    top_nyt_query = word_count_general.objects.filter(newspaper=1).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:50]
    nyt_most = []
    for record in top_nyt_query:
        interlist = []
        interlist.append(record['word'])
        interlist.append(record['word_count'])
        nyt_most.append(interlist)

    top_bbc_query = word_count_general.objects.filter(newspaper=2).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:50]
    bbc_most = []
    for record in top_bbc_query:
        interlist = []
        interlist.append(record['word'])
        interlist.append(record['word_count'])
        bbc_most.append(interlist)

    top_fn_query = word_count_general.objects.filter(newspaper=3).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:50]
    fn_most = []
    for record in top_fn_query:
        interlist = []
        interlist.append(record['word'])
        interlist.append(record['word_count'])
        fn_most.append(interlist)





    top_10_words_terms = word_count_general.objects.filter(newspaper=4).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:7]
    test_terms = []
    test_overall_values_list = []
    for i in top_10_words_terms:
        test_terms.append(i['word'])
        test_overall_values_list.append(i['word_count'])



    test_values_list = []

    for i in range(1,4):
        newspaper_values = []
        for y in test_terms:
            all_test_values = word_count_general.objects.filter(date__contains=today).filter(newspaper=i).filter(word=y).values('word_count')
            for record in all_test_values:
                newspaper_values.append(record['word_count'])
        test_values_list.append(newspaper_values)






    test_ny_values_list = test_values_list[0]
    test_bbc_values_list = test_values_list[1]
    test_fn_values_list = test_values_list[2]


    from plotly import graph_objs as go


    values_fig = go.Figure(data=[
        go.Bar(name='New York Times', y=test_terms, x=test_ny_values_list, orientation='h', marker_color="#2d2e30"),
        go.Bar(name='BBC News', y=test_terms, x=test_bbc_values_list, orientation = 'h', marker_color="#bb1919"),
        go.Bar(name='Fox News', y=test_terms, x=test_fn_values_list, orientation = 'h', marker_color="rgba(0,51,102,.99)"),
        ], )
    values_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, height=325, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))



    top_9_query_nyt = word_count_general.objects.filter(date__contains=today).filter(newspaper=1).values('word', 'word_count').order_by('-word_count')[:7]



    test_terms_nyt = []
    test_ny_values_list_nyt = []
    for record in top_9_query_nyt:
        test_terms_nyt.append(record['word'])
        test_ny_values_list_nyt.append(record['word_count'])



    top_9_query_bbc = word_count_general.objects.filter(date__contains=today).filter(newspaper=2).values('word', 'word_count').order_by('-word_count')[:7]

    test_terms_bbc = []
    test_bbc_values_list_bbc = []
    for record in top_9_query_bbc:
        test_terms_bbc.append(record['word'])
        test_bbc_values_list_bbc.append(record['word_count'])





    top_9_query_fn = word_count_general.objects.filter(date__contains=today).filter(newspaper=3).values('word', 'word_count').order_by('-word_count')[:7]

    test_terms_fn = []
    test_fn_values_list_fn = []
    for record in top_9_query_fn:
        test_terms_fn.append(record['word'])
        test_fn_values_list_fn.append(record['word_count'])









    values_fig_nyt = go.Figure(data=[
        go.Bar(name='New York Times', y=test_terms_nyt, x=test_ny_values_list_nyt, orientation='h', marker_color="#2d2e30"),

        ], )
    values_fig_nyt.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig_nyt.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, height=325, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values_nyt = str(plotly.offline.plot(values_fig_nyt, output_type='div', config = {'displayModeBar': False}))









    values_fig_bbc = go.Figure(data=[
        go.Bar(name='BBC News', y=test_terms_bbc, x=test_bbc_values_list_bbc, orientation = 'h', marker_color="#bb1919"),

        ], )
    values_fig_bbc.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig_bbc.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, height=325, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values_bbc = str(plotly.offline.plot(values_fig_bbc, output_type='div', config = {'displayModeBar': False}))







    values_fig_fn = go.Figure(data=[
        go.Bar(name='Fox News', y=test_terms_fn, x=test_fn_values_list_fn, orientation = 'h', marker_color="rgba(0,51,102,.99)"),

        ], )
    values_fig_fn.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig_fn.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, height=325, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values_fn = str(plotly.offline.plot(values_fig_fn, output_type='div', config = {'displayModeBar': False}))


















    avg_rl_overall = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('ahrl')[0]['ahrl'],1)


    avg_rl_nyt = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('ahrl')[0]['ahrl'],1)


    avg_rl_bbc = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('ahrl')[0]['ahrl'],1)


    avg_rl_fn = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('ahrl')[0]['ahrl'],1)




    avg_wc_overall = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('awc')[0]['awc'],1)

    avg_wc_nyt = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('awc')[0]['awc'],1)

    avg_wc_bbc = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('awc')[0]['awc'],1)

    avg_wc_fn = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('awc')[0]['awc'],1)



    question_percent_overall = str(round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('percent_quest')[0]['percent_quest'],1)) + "%"

    exclamation_percent_overall = str(round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('percent_exclam')[0]['percent_exclam'],1)) + "%"





    question_percent_nyt = str(round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('percent_quest')[0]['percent_quest'],1)) + "%"
    exclamation_percent_nyt = str(round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('percent_exclam')[0]['percent_exclam'],1)) + "%"

    question_percent_bbc = str(round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('percent_quest')[0]['percent_quest'],1)) + "%"
    exclamation_percent_bbc = str(round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('percent_exclam')[0]['percent_exclam'],1)) + "%"

    question_percent_fn = str(round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('percent_quest')[0]['percent_quest'],1)) + "%"
    exclamation_percent_fn = str(round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('percent_exclam')[0]['percent_exclam'],1)) + "%"





    numbered_base_words_query = cooc_wc.objects.filter(date__contains=today).filter(newspaper=4).values('base_word').order_by('id')
    numbered_base_words_list = []

    for record in numbered_base_words_query:
        if record['base_word'] not in numbered_base_words_list:

            numbered_base_words_list.append(record['base_word'])

    numbered_base_words_list = numbered_base_words_list[:100]

    numbered_base_words = enumerate(numbered_base_words_list,1)

    numbered_base_words_query_nyt = cooc_wc.objects.filter(date__contains=today).filter(newspaper=1).values('base_word').order_by('id')
    numbered_base_words_list_nyt = []

    for record in numbered_base_words_query_nyt:
        if record['base_word'] not in numbered_base_words_list_nyt:

            numbered_base_words_list_nyt.append(record['base_word'])

    numbered_base_words_list_nyt = numbered_base_words_list_nyt[:100]

    numbered_base_word_nyt = enumerate(numbered_base_words_list_nyt,1)



    numbered_base_words_query_bbc = cooc_wc.objects.filter(date__contains=today).filter(newspaper=2).values('base_word').order_by('id')
    numbered_base_words_list_bbc = []

    for record in numbered_base_words_query_bbc:
        if record['base_word'] not in numbered_base_words_list_bbc:
            numbered_base_words_list_bbc.append(record['base_word'])
    numbered_base_words_list_bbc = numbered_base_words_list_bbc[:100]

    numbered_base_word_bbc = enumerate(numbered_base_words_list_bbc,1)


    numbered_base_words_query_fn = cooc_wc.objects.filter(date__contains=today).filter(newspaper=3).values('base_word').order_by('id')
    numbered_base_words_list_fn = []
    for record in numbered_base_words_query_fn:
        if record['base_word'] not in numbered_base_words_list_fn:
            numbered_base_words_list_fn.append(record['base_word'])
    numbered_base_words_list_fn = numbered_base_words_list_fn[:100]

    numbered_base_word_fn = enumerate(numbered_base_words_list_fn,1)


    coocs_overall_nyt = cooc_wc.objects.filter(date__contains=today).filter(newspaper=1).values('base_word', 'cooc', 'coocc').order_by('id','-coocc')
    cooc_dict_overall_nyt = {}
    for record in coocs_overall_nyt:
        if record['base_word'] not in cooc_dict_overall_nyt:
            cooc_dict_overall_nyt[record['base_word']] = []
            this_cooc_list = []
            this_cooc_list.append(record['cooc'])
            this_cooc_list.append(record['coocc'])
            cooc_dict_overall_nyt[record['base_word']].append(this_cooc_list)
        else:
            this_cooc_list = []
            this_cooc_list.append(record['cooc'])
            this_cooc_list.append(record['coocc'])
            cooc_dict_overall_nyt[record['base_word']].append(this_cooc_list)


    coocs_list_nyt = []
    for key, value in cooc_dict_overall_nyt.items():
        coocs_list_nyt.append(value)

    coocs_list_nyt = coocs_list_nyt[:100]




    coocs_overall_bbc = cooc_wc.objects.filter(date__contains=today).filter(newspaper=2).values('base_word', 'cooc', 'coocc').order_by('id','-coocc')
    cooc_dict_overall_bbc = {}
    for record in coocs_overall_bbc:
        if record['base_word'] not in cooc_dict_overall_bbc:
            cooc_dict_overall_bbc[record['base_word']] = []
            this_cooc_list = []
            this_cooc_list.append(record['cooc'])
            this_cooc_list.append(record['coocc'])
            cooc_dict_overall_bbc[record['base_word']].append(this_cooc_list)
        else:
            this_cooc_list = []
            this_cooc_list.append(record['cooc'])
            this_cooc_list.append(record['coocc'])
            cooc_dict_overall_bbc[record['base_word']].append(this_cooc_list)



    coocs_list_bbc = []
    for key, value in cooc_dict_overall_bbc.items():
        coocs_list_bbc.append(value)

    coocs_list_bbc = coocs_list_bbc[:100]


    coocs_overall_fn = cooc_wc.objects.filter(date__contains=today).filter(newspaper=3).values('base_word', 'cooc', 'coocc').order_by('id','-coocc')
    cooc_dict_overall_fn = {}
    for record in coocs_overall_fn:
        if record['base_word'] not in cooc_dict_overall_fn:
            cooc_dict_overall_fn[record['base_word']] = []
            this_cooc_list = []
            this_cooc_list.append(record['cooc'])
            this_cooc_list.append(record['coocc'])
            cooc_dict_overall_fn[record['base_word']].append(this_cooc_list)
        else:
            this_cooc_list = []
            this_cooc_list.append(record['cooc'])
            this_cooc_list.append(record['coocc'])
            cooc_dict_overall_fn[record['base_word']].append(this_cooc_list)


    coocs_list_fn = []
    for key, value in cooc_dict_overall_fn.items():
        coocs_list_fn.append(value)

    coocs_list_fn = coocs_list_fn[:100]


    coocs_overall = cooc_wc.objects.filter(date__contains=today).filter(newspaper=4).values('base_word', 'cooc', 'coocc').order_by('id','-coocc')
    cooc_dict_overall = {}
    for record in coocs_overall:
        if record['base_word'] not in cooc_dict_overall:
            cooc_dict_overall[record['base_word']] = []
            this_cooc_list = []
            this_cooc_list.append(record['cooc'])
            this_cooc_list.append(record['coocc'])
            cooc_dict_overall[record['base_word']].append(this_cooc_list)
        else:
            this_cooc_list = []
            this_cooc_list.append(record['cooc'])
            this_cooc_list.append(record['coocc'])
            cooc_dict_overall[record['base_word']].append(this_cooc_list)


    coocs_list = []
    for key, value in cooc_dict_overall.items():
        coocs_list.append(value)

    coocs_list = coocs_list[:100]






    all_unique_words = format(int(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('uw')[0]['uw']),',d')
    nyt_unique_words = format(int(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('uw')[0]['uw']),',d')
    bbc_unique_words = format(int(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('uw')[0]['uw']),',d')
    fn_unique_words = format(int(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('uw')[0]['uw']),',d')





    overall_top_50 = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('wd')[0]['wd'],1)
    nyt_top_50 = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('wd')[0]['wd'],1)
    bbc_top_50 = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('wd')[0]['wd'],1)
    fn_top_50 = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('wd')[0]['wd'],1)






    all_avg_word_length = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('ahwl')[0]['ahwl'],1)
    nyt_avg_word_length = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('ahwl')[0]['ahwl'],1)
    bbc_avg_word_length = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('ahwl')[0]['ahwl'],1)
    fn_avg_word_length = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('ahwl')[0]['ahwl'],1)

    template = loader.get_template('custom_scraper/word_count_general_og.html')


    context = {'overall_top_50': overall_top_50, 'nyt_top_50': nyt_top_50, 'bbc_top_50': bbc_top_50, 'fn_top_50': fn_top_50, 'all_unique_words': all_unique_words, 'nyt_unique_words': nyt_unique_words, 'bbc_unique_words': bbc_unique_words, 'fn_unique_words': fn_unique_words,'all_avg_word_length': all_avg_word_length, 'nyt_avg_word_length': nyt_avg_word_length, 'bbc_avg_word_length': bbc_avg_word_length, 'fn_avg_word_length': fn_avg_word_length, 'numbered_base_word_nyt': numbered_base_word_nyt, 'numbered_base_word_bbc': numbered_base_word_bbc, 'numbered_base_word_fn': numbered_base_word_fn, 'html_div_values_fn': html_div_values_fn,'html_div_values_bbc': html_div_values_bbc, 'html_div_values_nyt': html_div_values_nyt, 'numbered_base_words': numbered_base_words, 'coocs_list': coocs_list, 'coocs_list_nyt': coocs_list_nyt, 'coocs_list_bbc': coocs_list_bbc, 'coocs_list_fn': coocs_list_fn, 'nyt_most': nyt_most, 'bbc_most': bbc_most, 'fn_most': fn_most, 'html_div_values': html_div_values, 'avg_rl_overall': avg_rl_overall, 'avg_rl_nyt': avg_rl_nyt, 'avg_rl_bbc': avg_rl_bbc, 'avg_rl_fn': avg_rl_fn, 'avg_wc_overall': avg_wc_overall, 'avg_wc_nyt': avg_wc_nyt, 'avg_wc_bbc': avg_wc_bbc, 'avg_wc_fn': avg_wc_fn, 'question_percent_overall': question_percent_overall, 'question_percent_nyt': question_percent_nyt, 'question_percent_bbc': question_percent_bbc, 'question_percent_fn': question_percent_fn, 'exclamation_percent_overall': exclamation_percent_overall, 'exclamation_percent_nyt': exclamation_percent_nyt, 'exclamation_percent_bbc': exclamation_percent_bbc, 'exclamation_percent_fn': exclamation_percent_fn}
    cache_test = HttpResponse(template.render(context, request),)

    cache_test = cache_test.content.decode("utf-8")
    html_cache_save = html_cache(page_num=1, cache_html=cache_test)
    html_cache_save.save()

    return render(request, 'custom_scraper/word_count_general_og.html',{'cached':cached,'overall_top_50': overall_top_50, 'nyt_top_50': nyt_top_50, 'bbc_top_50': bbc_top_50, 'fn_top_50': fn_top_50, 'all_unique_words': all_unique_words, 'nyt_unique_words': nyt_unique_words, 'bbc_unique_words': bbc_unique_words, 'fn_unique_words': fn_unique_words,'all_avg_word_length': all_avg_word_length, 'nyt_avg_word_length': nyt_avg_word_length, 'bbc_avg_word_length': bbc_avg_word_length, 'fn_avg_word_length': fn_avg_word_length, 'numbered_base_word_nyt': numbered_base_word_nyt, 'numbered_base_word_bbc': numbered_base_word_bbc, 'numbered_base_word_fn': numbered_base_word_fn, 'html_div_values_fn': html_div_values_fn,'html_div_values_bbc': html_div_values_bbc, 'html_div_values_nyt': html_div_values_nyt, 'numbered_base_words': numbered_base_words, 'coocs_list': coocs_list, 'coocs_list_nyt': coocs_list_nyt, 'coocs_list_bbc': coocs_list_bbc, 'coocs_list_fn': coocs_list_fn, 'nyt_most': nyt_most, 'bbc_most': bbc_most, 'fn_most': fn_most, 'html_div_values': html_div_values, 'avg_rl_overall': avg_rl_overall, 'avg_rl_nyt': avg_rl_nyt, 'avg_rl_bbc': avg_rl_bbc, 'avg_rl_fn': avg_rl_fn, 'avg_wc_overall': avg_wc_overall, 'avg_wc_nyt': avg_wc_nyt, 'avg_wc_bbc': avg_wc_bbc, 'avg_wc_fn': avg_wc_fn, 'question_percent_overall': question_percent_overall, 'question_percent_nyt': question_percent_nyt, 'question_percent_bbc': question_percent_bbc, 'question_percent_fn': question_percent_fn, 'exclamation_percent_overall': exclamation_percent_overall, 'exclamation_percent_nyt': exclamation_percent_nyt, 'exclamation_percent_bbc': exclamation_percent_bbc, 'exclamation_percent_fn': exclamation_percent_fn}, )


def word_count_general_db(request):
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    today_headline_check = Headline.objects.filter(date__contains=today).values('headline')
    if not today_headline_check:
        today = yesterday

    import plotly.graph_objects as go

    terms = []
    ny_values_list = []
    bbc_values_list = []
    fn_values_list = []

    overall_terms = word_count_general.objects.filter(date__contains=today).filter(newspaper=4).values('word','word_count')

    for i in overall_terms[:9]:
        terms.append(i['word'])
        nyt = word_count_general.objects.filter(date__contains=today).filter(newspaper=1).filter(word=i['word']).values('word_count')
        for y in nyt:
            ny_values_list.append(y['word_count'])
        bbc = word_count_general.objects.filter(date__contains=today).filter(newspaper=2).filter(word=i['word']).values('word_count')
        for y in bbc:
            bbc_values_list.append(y['word_count'])
        fn = word_count_general.objects.filter(date__contains=today).filter(newspaper=3).filter(word=i['word']).values('word_count')
        for y in fn:
            fn_values_list.append(y['word_count'])



    values_fig = go.Figure(data=[
        go.Bar(name='New York Times', y=terms, x=ny_values_list, orientation='h', marker_color="#2d2e30"),
        go.Bar(name='BBC News', y=terms, x=bbc_values_list, orientation = 'h', marker_color="#bb1919"),
        go.Bar(name='Fox News', y=terms, x=fn_values_list, orientation = 'h', marker_color="rgba(0,51,102,.99)"),
        ], )
    values_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, height=450, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))



    terms_nyt = []
    ny_values_list_nyt = []

    nyt_words_with_counts = word_count_general.objects.filter(date__contains=today).filter(newspaper=1).values('word', 'word_count')
    for i in nyt_words_with_counts[:9]:
        terms_nyt.append(i['word'])
        ny_values_list_nyt.append(i['word_count'])




    values_fig_nyt = go.Figure(data=[
        go.Bar(name='New York Times', y=terms_nyt, x=ny_values_list_nyt, orientation='h', marker_color="#2d2e30"),

        ], )
    values_fig_nyt.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig_nyt.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, height=450, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values_nyt = str(plotly.offline.plot(values_fig_nyt, output_type='div', config = {'displayModeBar': False}))





    terms_bbc = []
    bbc_values_list_bbc = []

    bbc_words_with_counts = word_count_general.objects.filter(date__contains=today).filter(newspaper=2).values('word', 'word_count')
    for i in bbc_words_with_counts[:9]:
        terms_bbc.append(i['word'])
        bbc_values_list_bbc.append(i['word_count'])



    values_fig_bbc = go.Figure(data=[
        go.Bar(name='BBC News', y=terms_bbc, x=bbc_values_list_bbc, orientation = 'h', marker_color="#bb1919"),

        ], )
    values_fig_bbc.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig_bbc.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, height=450, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values_bbc = str(plotly.offline.plot(values_fig_bbc, output_type='div', config = {'displayModeBar': False}))



    terms_fn = []
    fn_values_list_fn = []

    fn_words_with_counts = word_count_general.objects.filter(date__contains=today).filter(newspaper=3).values('word', 'word_count')
    for i in fn_words_with_counts[:9]:
        terms_fn.append(i['word'])
        fn_values_list_fn.append(i['word_count'])


    values_fig_fn = go.Figure(data=[
        go.Bar(name='Fox News', y=terms_fn, x=fn_values_list_fn, orientation = 'h', marker_color="rgba(0,51,102,.99)"),

        ], )
    values_fig_fn.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig_fn.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, height=450, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values_fn = str(plotly.offline.plot(values_fig_fn, output_type='div', config = {'displayModeBar': False}))

    nyt_most_common = word_count_general.objects.filter(date__contains=today).filter(newspaper=1).values('word', 'word_count')
    bbc_most_common = word_count_general.objects.filter(date__contains=today).filter(newspaper=2).values('word', 'word_count')
    fn_most_common = word_count_general.objects.filter(date__contains=today).filter(newspaper=3).values('word', 'word_count')



    nyt_most = []
    bbc_most = []
    fn_most = []

    for i in nyt_most_common:
        interlist = []
        interlist.append(i['word'])
        interlist.append(i['word_count'])
        nyt_most.append(interlist)


    for i in bbc_most_common:
        interlist = []
        interlist.append(i['word'])
        interlist.append(i['word_count'])
        bbc_most.append(interlist)

    for i in fn_most_common:
        interlist = []
        interlist.append(i['word'])
        interlist.append(i['word_count'])
        fn_most.append(interlist)


    avg_wc_overall = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('awc')[0]['awc'],1)
    avg_wc_nyt = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('awc')[0]['awc'],1)
    avg_wc_bbc = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('awc')[0]['awc'],1)
    avg_wc_fn = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('awc')[0]['awc'],1)

    avg_rl_overall = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('ahrl')[0]['ahrl'],1)
    avg_rl_nyt = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('ahrl')[0]['ahrl'],1)
    avg_rl_bbc = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('ahrl')[0]['ahrl'],1)
    avg_rl_fn = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('ahrl')[0]['ahrl'],1)

    question_percent_overall = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('percent_quest')[0]['percent_quest'],1)
    question_percent_nyt = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('percent_quest')[0]['percent_quest'],1)
    question_percent_bbc = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('percent_quest')[0]['percent_quest'],1)
    question_percent_fn = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('percent_quest')[0]['percent_quest'],1)

    exclamation_percent_overall = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('percent_exclam')[0]['percent_exclam'],1)
    exclamation_percent_nyt = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('percent_exclam')[0]['percent_exclam'],1)
    exclamation_percent_bbc = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('percent_exclam')[0]['percent_exclam'],1)
    exclamation_percent_fn = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('percent_exclam')[0]['percent_exclam'],1)

    all_avg_word_length = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('ahwl')[0]['ahwl'],1)
    nyt_avg_word_length = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('ahwl')[0]['ahwl'],1)
    bbc_avg_word_length = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('ahwl')[0]['ahwl'],1)
    fn_avg_word_length = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('ahwl')[0]['ahwl'],1)

    all_unique_words = format(int(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('uw')[0]['uw']),',d')
    nyt_unique_words = format(int(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('uw')[0]['uw']),',d')
    bbc_unique_words = format(int(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('uw')[0]['uw']),',d')
    fn_unique_words = format(int(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('uw')[0]['uw']),',d')

    overall_top_50 = round(style_wc.objects.filter(date__contains=today).filter(newspaper=4).values('wd')[0]['wd'],1)
    nyt_top_50 = round(style_wc.objects.filter(date__contains=today).filter(newspaper=1).values('wd')[0]['wd'],1)
    bbc_top_50 = round(style_wc.objects.filter(date__contains=today).filter(newspaper=2).values('wd')[0]['wd'],1)
    fn_top_50 = round(style_wc.objects.filter(date__contains=today).filter(newspaper=3).values('wd')[0]['wd'],1)

    base_word = cooc_wc.objects.filter(date__contains=today).filter(newspaper=4).values('base_word')

    base_words = []
    for i in base_word:
        if i['base_word'] not in base_words:
            base_words.append(i['base_word'])

    base_word_nyt = cooc_wc.objects.filter(date__contains=today).filter(newspaper=1).values('base_word')

    base_words_nyt = []
    for i in base_word_nyt:
        if i['base_word'] not in base_words_nyt:
            base_words_nyt.append(i['base_word'])

    base_word_bbc = cooc_wc.objects.filter(date__contains=today).filter(newspaper=2).values('base_word')

    base_words_bbc = []
    for i in base_word_bbc:
        if i['base_word'] not in base_words_bbc:
            base_words_bbc.append(i['base_word'])

    base_word_fn = cooc_wc.objects.filter(date__contains=today).filter(newspaper=3).values('base_word')

    base_words_fn = []
    for i in base_word_fn:
        if i['base_word'] not in base_words_fn:
            base_words_fn.append(i['base_word'])

    numbered_base_words = enumerate(base_words,1)
    numbered_base_word_nyt = enumerate(base_words_nyt,1)
    numbered_base_word_bbc = enumerate(base_words_bbc,1)
    numbered_base_word_fn = enumerate(base_words_fn,1)



    coocs_list = []
    for i in base_words:
        cooc_query = cooc_wc.objects.filter(date__contains=today).filter(newspaper=4).filter(base_word=i).values('cooc', 'coocc')
        coocs_for_word = []
        for y in cooc_query:
            interlist = []
            interlist.append(y['cooc'])
            interlist.append(y['coocc'])
            coocs_for_word.append(interlist)
        coocs_list.append(coocs_for_word)


    coocs_list_nyt = []
    for i in base_words_nyt:
        cooc_query = cooc_wc.objects.filter(date__contains=today).filter(newspaper=1).filter(base_word=i).values('cooc', 'coocc')
        coocs_for_word = []
        for y in cooc_query:
            interlist = []
            interlist.append(y['cooc'])
            interlist.append(y['coocc'])
            coocs_for_word.append(interlist)
        coocs_list_nyt.append(coocs_for_word)

    coocs_list_bbc = []
    for i in base_words_bbc:
        cooc_query = cooc_wc.objects.filter(date__contains=today).filter(newspaper=2).filter(base_word=i).values('cooc', 'coocc')
        coocs_for_word = []
        for y in cooc_query:
            interlist = []
            interlist.append(y['cooc'])
            interlist.append(y['coocc'])
            coocs_for_word.append(interlist)
        coocs_list_bbc.append(coocs_for_word)

    coocs_list_fn = []
    for i in base_words_fn:
        cooc_query = cooc_wc.objects.filter(date__contains=today).filter(newspaper=3).filter(base_word=i).values('cooc', 'coocc')
        coocs_for_word = []
        for y in cooc_query:
            interlist = []
            interlist.append(y['cooc'])
            interlist.append(y['coocc'])
            coocs_for_word.append(interlist)
        coocs_list_fn.append(coocs_for_word)





    return render(request, 'custom_scraper/word_count_general_db.html',{'coocs_list_nyt': coocs_list_nyt, 'coocs_list_bbc': coocs_list_bbc, 'coocs_list_fn': coocs_list_fn,  'coocs_list': coocs_list, 'numbered_base_words': numbered_base_words, 'numbered_base_word_nyt': numbered_base_word_nyt, 'numbered_base_word_bbc': numbered_base_word_bbc, 'numbered_base_word_fn': numbered_base_word_fn,   'overall_top_50': overall_top_50, 'nyt_top_50': nyt_top_50, 'bbc_top_50': bbc_top_50, 'fn_top_50': fn_top_50, 'all_unique_words': all_unique_words, 'nyt_unique_words': nyt_unique_words, 'bbc_unique_words': bbc_unique_words, 'fn_unique_words': fn_unique_words, 'all_avg_word_length': all_avg_word_length, 'nyt_avg_word_length': nyt_avg_word_length, 'bbc_avg_word_length': bbc_avg_word_length, 'fn_avg_word_length': fn_avg_word_length, 'exclamation_percent_overall': exclamation_percent_overall, 'exclamation_percent_nyt': exclamation_percent_nyt, 'exclamation_percent_bbc': exclamation_percent_bbc, 'exclamation_percent_fn': exclamation_percent_fn, 'question_percent_overall': question_percent_overall, 'question_percent_nyt': question_percent_nyt, 'question_percent_bbc': question_percent_bbc, 'question_percent_fn': question_percent_fn, 'avg_rl_overall': avg_rl_overall, 'avg_rl_nyt': avg_rl_nyt, 'avg_rl_bbc': avg_rl_bbc, 'avg_rl_fn': avg_rl_fn,   'avg_wc_nyt': avg_wc_nyt, 'avg_wc_bbc': avg_wc_bbc, 'avg_wc_fn': avg_wc_fn,  'avg_wc_overall': avg_wc_overall, 'nyt_most': nyt_most, 'bbc_most': bbc_most, 'fn_most': fn_most, 'html_div_values_nyt': html_div_values_nyt,'html_div_values_bbc': html_div_values_bbc,'html_div_values_fn': html_div_values_fn,  'html_div_values': html_div_values},)


def emotion_newspaper(request):
    from datetime import datetime

    today = datetime.today()
    yesterday = today - timedelta(1)
    today = str(today)[:10]

    yesterday = str(yesterday)[:10]
    cached = False

    if html_cache.objects.filter(date__contains=today).filter(page_num=4):
        html_record = html_cache.objects.filter(date__contains=today).filter(page_num=4).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/emotion_newspaper.html',{'html':html, 'cached':cached},)

    if html_cache.objects.filter(date__contains=yesterday).filter(page_num=4):
        html_record = html_cache.objects.filter(date__contains=yesterday).filter(page_num=4).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/emotion_newspaper.html',{'html':html, 'cached':cached},)



    import plotly.graph_objects as go

    categories = ['disgust','trust','joy', 'anticipation', 'surprise', 'fear', 'sadness', 'anger']

    fear_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(fear__gte=1).count()
    anger_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(anger__gte=1).count()
    anticip_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(anticip__gte=1).count()
    trust_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(trust__gte=1).count()
    surprise_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(surprise__gte=1).count()
    sadness_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(sadness__gte=1).count()
    disgust_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(disgust__gte=1).count()
    joy_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(joy__gte=1).count()



    fig_emotion_overall = go.Figure()

    fig_emotion_overall.add_trace(go.Scatterpolar(
        r=[disgust_overall, trust_overall, joy_overall, anticip_overall, surprise_overall, fear_overall, sadness_overall, anger_overall ],
        theta=categories,
        fill='toself', line_color='black',fillcolor='rgba(0, 0, 0, 0.63)',
        name='All Newspapers',

    ))

    fig_emotion_overall.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=False,

    gridcolor='rgba(0,0,0,0)'
        )),
    showlegend=False,
   height=400, font=dict(family="Roboto", size=15,color="black"),  margin=dict(pad=0),
        paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'


    )

    fig_emotion_overall.update_layout(    paper_bgcolor='rgba(0,0,0,0)',
  )



    html_div_emotion_overall = str(plotly.offline.plot(fig_emotion_overall, output_type='div', config = {'displayModeBar': False}))


    def make_radar_graph(newspaper_num):
        categories = ['disgust','trust','joy', 'anticipation', 'surprise', 'fear', 'sadness', 'anger']

        fear_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(fear__gte=1).count()
        anger_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(anger__gte=1).count()
        anticip_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(anticip__gte=1).count()
        trust_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(trust__gte=1).count()
        surprise_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(surprise__gte=1).count()
        sadness_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(sadness__gte=1).count()
        disgust_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(disgust__gte=1).count()
        joy_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(joy__gte=1).count()



        fig_emotion_overall = go.Figure()

        fig_emotion_overall.add_trace(go.Scatterpolar(
            r=[disgust_overall, trust_overall, joy_overall, anticip_overall, surprise_overall, fear_overall, sadness_overall, anger_overall ],
            theta=categories,
            fill='toself', line_color='black',fillcolor='rgba(0, 0, 0, 0.63)',
            name='All Newspapers',

        ))

        fig_emotion_overall.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=False,

        gridcolor='rgba(0,0,0,0)'
            )),
        showlegend=False,
        height=400,font=dict(family="Roboto", size=15,color="black"),  margin=dict(pad=0),
            paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'


        )

        fig_emotion_overall.update_layout(    paper_bgcolor='rgba(0,0,0,0)',
    )



        html_div_emotion_overall = str(plotly.offline.plot(fig_emotion_overall, output_type='div',config = {'displayModeBar': False,  }))


        return html_div_emotion_overall

    html_div_emotion_radar_nyt = make_radar_graph(1)
    html_div_emotion_radar_bbc = make_radar_graph(2)
    html_div_emotion_radar_fn = make_radar_graph(3)

    from django.db.models import Sum

    #emotion_by_date = Headline_emotion.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date', 'disgust', 'trust', 'joy', ).annotate(Disgust=Count('disgust')).annotate(Trust=Count('trust')).annotate(Joy=Count('joy')).annotate(Disgust=Count('disgust')).annotate(Disgust=Count('disgust')).annotate(Disgust=Count('disgust')).annotate(Disgust=Count('disgust')).annotate(Disgust=Count('disgust')).order_by("Date")

    emotion_list = ['disgust', 'trust', 'joy', 'anticip', 'surprise', 'fear', 'sadness', 'anger']

    emotion_by_date = Headline_emotion.objects.filter(day_order__lte=25).annotate(Date=TruncDay('date')).values('Date').annotate(Anger=Sum('anger')).annotate(Disgust=Sum('disgust')).annotate(Trust=Sum('trust')).annotate(Joy=Sum('joy')).annotate(Anticip=Sum('anticip')).annotate(Surprise=Sum('surprise')).annotate(Fear=Sum('fear')).annotate(Sadness=Sum('sadness')).order_by("Date")



    emotion_data = []
    trust_data = []
    joy_data = []
    anticip_data = []
    surprise_data = []
    fear_data = []
    sadness_data = []
    anger_data = []
    disgust_data = []

    for i in emotion_by_date:


        trust_dict = {}
        trust_dict['Date'] = i['Date']
        trust_dict['Emotion'] = "trust"
        trust_dict['Count'] = i['Trust']
        emotion_data.append(trust_dict)
        trust_data.append(trust_dict)

        joy_dict = {}
        joy_dict['Date'] = i['Date']
        joy_dict['Emotion'] = "joy"
        joy_dict['Count'] = i['Joy']
        emotion_data.append(joy_dict)
        joy_data.append(joy_dict)

        anticip_dict = {}
        anticip_dict['Date'] = i['Date']
        anticip_dict['Emotion'] = "anticipation"
        anticip_dict['Count'] = i['Anticip']
        emotion_data.append(anticip_dict)
        anticip_data.append(anticip_dict)

        surprise_dict = {}
        surprise_dict['Date'] = i['Date']
        surprise_dict['Emotion'] = "surprise"
        surprise_dict['Count'] = i['Surprise']
        emotion_data.append(surprise_dict)
        surprise_data.append(surprise_dict)

        fear_dict = {}
        fear_dict['Date'] = i['Date']
        fear_dict['Emotion'] = "fear"
        fear_dict['Count'] = i['Fear']
        emotion_data.append(fear_dict)
        fear_data.append(fear_dict)

        sadness_dict = {}
        sadness_dict['Date'] = i['Date']
        sadness_dict['Emotion'] = "sadness"
        sadness_dict['Count'] = i['Sadness']
        emotion_data.append(sadness_dict)
        sadness_data.append(sadness_dict)

        anger_dict = {}
        anger_dict['Date'] = i['Date']
        anger_dict['Emotion'] = "anger"
        anger_dict['Count'] = i['Anger']
        emotion_data.append(anger_dict)
        anger_data.append(anger_dict)

        disgust_dict = {}
        disgust_dict['Date'] = i['Date']
        disgust_dict['Emotion'] = "disgust"
        disgust_dict['Count'] = i['Disgust']
        emotion_data.append(disgust_dict)
        disgust_data.append(disgust_dict)

    emotion_data_pd = pd.DataFrame(list(emotion_data))
    fig_emotion_month = px.line(emotion_data_pd, x="Date", y="Count", color="Emotion")

    fig_emotion_month.update_layout( font=dict(family="Roboto",size=15,color="black"), height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0))

    html_div_emotion_month = str(plotly.offline.plot(fig_emotion_month, output_type='div', config = {'displayModeBar': False}))

    by_emotion_data_all = [trust_data, joy_data, anticip_data, surprise_data, fear_data, sadness_data, anger_data, disgust_data]

    def emotion_by_date_by_newspaper(paper_num):
        emotion_by_date = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).annotate(Date=TruncDay('date')).values('Date').annotate(Anger=Sum('anger')).annotate(Disgust=Sum('disgust')).annotate(Trust=Sum('trust')).annotate(Joy=Sum('joy')).annotate(Anticip=Sum('anticip')).annotate(Surprise=Sum('surprise')).annotate(Fear=Sum('fear')).annotate(Sadness=Sum('sadness')).order_by("Date")



        emotion_data = []

        trust_data = []
        joy_data = []
        anticip_data = []
        surprise_data = []
        fear_data = []
        sadness_data = []
        anger_data = []
        disgust_data = []

        for i in emotion_by_date:


            trust_dict = {}
            trust_dict['Date'] = i['Date']
            trust_dict['Emotion'] = "trust"
            trust_dict['Count'] = i['Trust']
            emotion_data.append(trust_dict)
            trust_data.append(trust_dict)

            joy_dict = {}
            joy_dict['Date'] = i['Date']
            joy_dict['Emotion'] = "joy"
            joy_dict['Count'] = i['Joy']
            emotion_data.append(joy_dict)
            joy_data.append(joy_dict)


            anticip_dict = {}
            anticip_dict['Date'] = i['Date']
            anticip_dict['Emotion'] = "anticipation"
            anticip_dict['Count'] = i['Anticip']
            emotion_data.append(anticip_dict)
            anticip_data.append(anticip_dict)


            surprise_dict = {}
            surprise_dict['Date'] = i['Date']
            surprise_dict['Emotion'] = "surprise"
            surprise_dict['Count'] = i['Surprise']
            emotion_data.append(surprise_dict)
            surprise_data.append(surprise_dict)


            fear_dict = {}
            fear_dict['Date'] = i['Date']
            fear_dict['Emotion'] = "fear"
            fear_dict['Count'] = i['Fear']
            emotion_data.append(fear_dict)
            fear_data.append(fear_dict)


            sadness_dict = {}
            sadness_dict['Date'] = i['Date']
            sadness_dict['Emotion'] = "sadness"
            sadness_dict['Count'] = i['Sadness']
            emotion_data.append(sadness_dict)
            sadness_data.append(sadness_dict)



            anger_dict = {}
            anger_dict['Date'] = i['Date']
            anger_dict['Emotion'] = "anger"
            anger_dict['Count'] = i['Anger']
            emotion_data.append(anger_dict)
            anger_data.append(anger_dict)


            disgust_dict = {}
            disgust_dict['Date'] = i['Date']
            disgust_dict['Emotion'] = "disgust"
            disgust_dict['Count'] = i['Disgust']
            emotion_data.append(disgust_dict)
            disgust_data.append(disgust_dict)


        emotion_data_pd = pd.DataFrame(list(emotion_data))
        fig_emotion_month = px.line(emotion_data_pd, x="Date", y="Count", color="Emotion")

        fig_emotion_month.update_layout( font=dict(family="Roboto",size=15,color="black"), height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0))

        html_div_emotion_month = str(plotly.offline.plot(fig_emotion_month, output_type='div', config = {'displayModeBar': False}))
        return html_div_emotion_month, trust_data, joy_data, anticip_data, surprise_data, fear_data, sadness_data, anger_data, disgust_data

    html_div_emotion_nyt = emotion_by_date_by_newspaper(1)
    html_div_emotion_bbc = emotion_by_date_by_newspaper(2)
    html_div_emotion_fn = emotion_by_date_by_newspaper(3)

    html_div_emotion_month_nyt = html_div_emotion_nyt[0]
    html_div_emotion_month_bbc = html_div_emotion_bbc[0]
    html_div_emotion_month_fn = html_div_emotion_fn[0]

    by_emotion_data_nyt = html_div_emotion_nyt[1:]
    by_emotion_data_bbc = html_div_emotion_bbc[1:]
    by_emotion_data_fn = html_div_emotion_fn[1:]



    """
    comparesent_month = pd.DataFrame(list(average_sentiment_by_date_compare_month))
    print(comparesent_month)
    comparesent_month['Average'] = comparesent_month['Average'] * 100
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(1, 'The New York Times')
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(2, 'BBC News')
    comparesent_month['newspaper'] = comparesent_month['newspaper'].replace(3, 'Fox News')
    comparesent_month.rename(columns={'newspaper':'Newspaper'}, inplace= True)


    figcompare_month = px.line(comparesent_month, x="Date", y="Average", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )


    figcompare_month.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0))



    html_div_compare_month = str(plotly.offline.plot(figcompare_month, output_type='div', config = {'displayModeBar': False}))
    """

    emotion_list_2 = [ 'trust', 'joy', 'anticipation', 'surprise', 'fear', 'sadness', 'anger','disgust']

    emotion_values_list = [ trust_overall, joy_overall, anticip_overall, surprise_overall, fear_overall, sadness_overall, anger_overall, disgust_overall,]
    emotion_bar_fig = go.Figure(data=[
        go.Bar(name='Overall', y=emotion_list_2, x=emotion_values_list, orientation='h',marker=dict(color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']),)])
    emotion_bar_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    emotion_bar_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', height=400, orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=5, t=0, b=0, pad=10), )




    html_div_emotion_bar = str(plotly.offline.plot(emotion_bar_fig, output_type='div', config = {'displayModeBar': False}))

    def emotion_bar_by_newspaper(newspaper_num):

        fear_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(fear__gte=1).count()
        anger_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(anger__gte=1).count()
        anticip_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(anticip__gte=1).count()
        trust_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(trust__gte=1).count()
        surprise_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(surprise__gte=1).count()
        sadness_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(sadness__gte=1).count()
        disgust_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(disgust__gte=1).count()
        joy_overall = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=newspaper_num).filter(joy__gte=1).count()

        emotion_list_2 = [ 'trust', 'joy', 'anticipation', 'surprise', 'fear', 'sadness', 'anger','disgust']


        emotion_values_list = [ trust_overall, joy_overall, anticip_overall, surprise_overall, fear_overall, sadness_overall, anger_overall, disgust_overall]
        emotion_bar_fig = go.Figure(data=[
            go.Bar(name='Overall', y=emotion_list_2, x=emotion_values_list, orientation='h', marker=dict(color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']),),
        ], )
        emotion_bar_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
        emotion_bar_fig.update_layout(
        font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', height=400, orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )


        html_div_emotion_bar = str(plotly.offline.plot(emotion_bar_fig, output_type='div', config = {'displayModeBar': False}))

        return html_div_emotion_bar

    html_div_emotion_bar_nyt = emotion_bar_by_newspaper(1)
    html_div_emotion_bar_bbc = emotion_bar_by_newspaper(2)
    html_div_emotion_bar_fn = emotion_bar_by_newspaper(3)

    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']






    def individual_emotion_by_date(emotion_num, emotion_data_list, emotion_list, colors):


        emotion_data_pd = pd.DataFrame(list(emotion_data_list[emotion_num-1]))
        fig_emotion_month = px.line(emotion_data_pd, x="Date", y="Count", color="Emotion")

        fig_emotion_month.update_layout( font=dict(family="Roboto",size=15,), height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0))

        html_div_emotion_month = str(plotly.offline.plot(fig_emotion_month, output_type='div', config = {'displayModeBar': False}))
        return html_div_emotion_month

        return html_div_emotion_bar

    trust_nyt = individual_emotion_by_date(1,by_emotion_data_nyt, emotion_list_2, colors)
    joy_nyt = individual_emotion_by_date(2,by_emotion_data_nyt, emotion_list_2, colors)
    anticipation_nyt = individual_emotion_by_date(3,by_emotion_data_nyt, emotion_list_2, colors)
    surprise_nyt = individual_emotion_by_date(4,by_emotion_data_nyt, emotion_list_2, colors)
    fear_nyt = individual_emotion_by_date(5,by_emotion_data_nyt, emotion_list_2, colors)
    sadness_nyt = individual_emotion_by_date(6,by_emotion_data_nyt, emotion_list_2, colors)
    anger_nyt = individual_emotion_by_date(7,by_emotion_data_nyt, emotion_list_2, colors)
    disgust_nyt = individual_emotion_by_date(8,by_emotion_data_nyt, emotion_list_2, colors)

    trust_bbc = individual_emotion_by_date(1,by_emotion_data_bbc, emotion_list_2, colors)
    joy_bbc = individual_emotion_by_date(2,by_emotion_data_bbc, emotion_list_2, colors)
    anticipation_bbc = individual_emotion_by_date(3,by_emotion_data_bbc, emotion_list_2, colors)
    surprise_bbc = individual_emotion_by_date(4,by_emotion_data_bbc, emotion_list_2, colors)
    fear_bbc = individual_emotion_by_date(5,by_emotion_data_bbc, emotion_list_2, colors)
    sadness_bbc = individual_emotion_by_date(6,by_emotion_data_bbc, emotion_list_2, colors)
    anger_bbc = individual_emotion_by_date(7,by_emotion_data_bbc, emotion_list_2, colors)
    disgust_bbc = individual_emotion_by_date(8,by_emotion_data_bbc, emotion_list_2, colors)

    trust_fn = individual_emotion_by_date(1,by_emotion_data_fn, emotion_list_2, colors)
    joy_fn = individual_emotion_by_date(2,by_emotion_data_fn, emotion_list_2, colors)
    anticipation_fn = individual_emotion_by_date(3,by_emotion_data_fn, emotion_list_2, colors)
    surprise_fn = individual_emotion_by_date(4,by_emotion_data_fn, emotion_list_2, colors)
    fear_fn = individual_emotion_by_date(5,by_emotion_data_fn, emotion_list_2, colors)
    sadness_fn = individual_emotion_by_date(6,by_emotion_data_fn, emotion_list_2, colors)
    anger_fn = individual_emotion_by_date(7,by_emotion_data_fn, emotion_list_2, colors)
    disgust_fn = individual_emotion_by_date(8,by_emotion_data_fn, emotion_list_2, colors)

    trust_all = individual_emotion_by_date(1,by_emotion_data_all, emotion_list_2, colors)
    joy_all = individual_emotion_by_date(2,by_emotion_data_all, emotion_list_2, colors)
    anticipation_all = individual_emotion_by_date(3,by_emotion_data_all, emotion_list_2, colors)
    surprise_all = individual_emotion_by_date(4,by_emotion_data_all, emotion_list_2, colors)
    fear_all = individual_emotion_by_date(5,by_emotion_data_all, emotion_list_2, colors)
    sadness_all = individual_emotion_by_date(6,by_emotion_data_all, emotion_list_2, colors)
    anger_all = individual_emotion_by_date(7,by_emotion_data_all, emotion_list_2, colors)
    disgust_all = individual_emotion_by_date(8,by_emotion_data_all, emotion_list_2, colors)


    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    today_headline_check = Headline.objects.filter(date__contains=today).values('headline')
    if not today_headline_check:
        today = yesterday


    #top_emotion_table_queries
    def get_emotion_tables(paper_num):
        emotion_table_query = top_words_emotions_percent.objects.filter(date__contains=today).filter(newspaper=paper_num).values("word", 'fear_percent', 'anger_percent', 'anticip_percent', 'trust_percent', 'surprise_percent', 'sadness_percent', 'disgust_percent', 'joy_percent')
        trust_tally = []
        joy_tally = []
        anticip_tally = []
        surprise_tally = []
        fear_tally = []
        sadness_tally = []
        anger_tally=[]
        disgust_tally = []
        for result in emotion_table_query:
            trust_tally.append([result['word'], round(result['trust_percent']*100)])
            joy_tally.append([result['word'], round(result['joy_percent']*100)])
            anticip_tally.append([result['word'], round(result['anticip_percent']*100)])
            surprise_tally.append([result['word'], round(result['surprise_percent']*100)])
            fear_tally.append([result['word'], round(result['fear_percent']*100)])
            sadness_tally.append([result['word'], round(result['sadness_percent']*100)])
            anger_tally.append([result['word'], round(result['anger_percent']*100)])
            disgust_tally.append([result['word'], round(result['disgust_percent']*100)])

        trust_tally = sorted(trust_tally, key=lambda x:x[1], reverse=True)
        joy_tally = sorted(joy_tally, key=lambda x:x[1], reverse=True)
        anticip_tally = sorted(anticip_tally, key=lambda x:x[1], reverse=True)
        surprise_tally = sorted(surprise_tally, key=lambda x:x[1], reverse=True)
        fear_tally = sorted(fear_tally, key=lambda x:x[1], reverse=True)
        sadness_tally = sorted(sadness_tally, key=lambda x:x[1], reverse=True)
        anger_tally = sorted(anger_tally, key=lambda x:x[1], reverse=True)

        disgust_tally = sorted(disgust_tally, key=lambda x:x[1], reverse=True)

        return trust_tally, joy_tally, anticip_tally, surprise_tally, fear_tally, sadness_tally, anger_tally, disgust_tally

    nyt_emotion_tables = get_emotion_tables(1)
    bbc_emotion_tables = get_emotion_tables(2)
    fn_emotion_tables = get_emotion_tables(3)
    overall_emotion_tables = get_emotion_tables(4)

    nyt_trust_tally = nyt_emotion_tables[0]
    nyt_joy_tally = nyt_emotion_tables[1]
    nyt_anticip_tally = nyt_emotion_tables[2]
    nyt_surprise_tally = nyt_emotion_tables[3]
    nyt_fear_tally = nyt_emotion_tables[4]
    nyt_sadness_tally = nyt_emotion_tables[5]
    nyt_anger_tally = nyt_emotion_tables[6]
    nyt_disgust_tally = nyt_emotion_tables[7]

    bbc_trust_tally = bbc_emotion_tables[0]
    bbc_joy_tally = bbc_emotion_tables[1]
    bbc_anticip_tally = bbc_emotion_tables[2]
    bbc_surprise_tally = bbc_emotion_tables[3]
    bbc_fear_tally = bbc_emotion_tables[4]
    bbc_sadness_tally = bbc_emotion_tables[5]
    bbc_anger_tally = bbc_emotion_tables[6]
    bbc_disgust_tally = bbc_emotion_tables[7]

    fn_trust_tally = fn_emotion_tables[0]
    fn_joy_tally = fn_emotion_tables[1]
    fn_anticip_tally = fn_emotion_tables[2]
    fn_surprise_tally = fn_emotion_tables[3]
    fn_fear_tally = fn_emotion_tables[4]
    fn_sadness_tally = fn_emotion_tables[5]
    fn_anger_tally = fn_emotion_tables[6]
    fn_disgust_tally = fn_emotion_tables[7]

    overall_trust_tally = overall_emotion_tables[0]
    overall_joy_tally = overall_emotion_tables[1]
    overall_anticip_tally = overall_emotion_tables[2]
    overall_surprise_tally = overall_emotion_tables[3]
    overall_fear_tally = overall_emotion_tables[4]
    overall_sadness_tally = overall_emotion_tables[5]
    overall_anger_tally = overall_emotion_tables[6]
    overall_disgust_tally = overall_emotion_tables[7]




    headline_emotion_query_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(trust__gt=1).values("date", "newspaper","headline", "trust", "link").order_by("-trust", "-date")[:50]
    headline_emotion_query_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(joy__gt=1).values("date", "newspaper","headline", "joy", "link").order_by("-joy", "-date")[:50]
    headline_emotion_query_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(anticip__gt=1).values("date", "newspaper","headline", "anticip", "link").order_by("-anticip", "-date")[:50]
    headline_emotion_query_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(surprise__gt=1).values("date", "newspaper","headline", "surprise", "link").order_by("-surprise", "-date")[:50]
    headline_emotion_query_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(fear__gt=1).values("date", "newspaper","headline", "fear", "link").order_by("-fear", "-date")[:50]
    headline_emotion_query_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(sadness__gt=1).values("date", "newspaper","headline", "sadness", "link").order_by("-sadness", "-date")[:50]
    headline_emotion_query_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(anger__gt=1).values("date", "newspaper","headline", "anger", "link").order_by("-anger", "-date")[:50]
    headline_emotion_query_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(disgust__gt=1).values("date", "newspaper","headline", "disgust", "link").order_by("-disgust", "-date")[:50]

    emotions = ['trust', 'joy', 'anticip', 'surprise', 'fear', 'sadness', 'anger', 'disgust']

    def format_emotion_query(list_of_emotion_queries):
        list_output = []
        for emotion_query in list_of_emotion_queries:

            formated_list = []
            for result in emotion_query:
                for emotion in emotions:
                    if emotion in result.keys():
                        this_emotion = emotion
                if result['newspaper'] == 1:
                    paper = "NYT"
                if result['newspaper'] == 2:
                    paper = "BBC"
                if result['newspaper'] == 3:
                    paper = "FN"
                result_list = [result['date'].strftime("%m/%d/%y"), paper, result['headline'], result[this_emotion], result['link']]
                formated_list.append(result_list)

            list_output.append(formated_list)
        return list_output

    all_emotions_queries_list = [headline_emotion_query_trust, headline_emotion_query_joy, headline_emotion_query_anticip, headline_emotion_query_surprise, headline_emotion_query_fear, headline_emotion_query_sadness, headline_emotion_query_anger, headline_emotion_query_disgust]

    all_emotions_query = format_emotion_query(all_emotions_queries_list)
    trust_formatted = all_emotions_query[0]
    joy_formatted = all_emotions_query[1]
    anticip_formatted = all_emotions_query[2]
    surprise_formatted = all_emotions_query[3]
    fear_formatted = all_emotions_query[4]
    sadness_formatted = all_emotions_query[5]
    anger_formatted = all_emotions_query[6]
    disgust_formatted = all_emotions_query[7]


    def get_emotions_formatted_by_paper(paper_num):
        headline_emotion_query_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(trust__gt=1).values("date", "newspaper","headline", "trust", "link").order_by("-trust", "-date")[:50]
        headline_emotion_query_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(joy__gt=1).values("date", "newspaper","headline", "joy", "link").order_by("-joy", "-date")[:50]
        headline_emotion_query_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(anticip__gt=1).values("date", "newspaper","headline", "anticip", "link").order_by("-anticip", "-date")[:50]
        headline_emotion_query_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(surprise__gt=1).values("date", "newspaper","headline", "surprise", "link").order_by("-surprise", "-date")[:50]
        headline_emotion_query_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(fear__gt=1).values("date", "newspaper","headline", "fear", "link").order_by("-fear", "-date")[:50]
        headline_emotion_query_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(sadness__gt=1).values("date", "newspaper","headline", "sadness", "link").order_by("-sadness", "-date")[:50]
        headline_emotion_query_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(anger__gt=1).values("date", "newspaper","headline", "anger", "link").order_by("-anger", "-date")[:50]
        headline_emotion_query_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(newspaper=paper_num).filter(disgust__gt=1).values("date", "newspaper","headline", "disgust", "link").order_by("-disgust", "-date")[:50]
        emotions = ['trust', 'joy', 'anticip', 'surprise', 'fear', 'sadness', 'anger', 'disgust']


        def format_emotion_query(list_of_emotion_queries):
            list_output = []
            for emotion_query in list_of_emotion_queries:

                formated_list = []
                for result in emotion_query:
                    for emotion in emotions:
                        if emotion in result.keys():
                            this_emotion = emotion
                    if result['newspaper'] == 1:
                        paper = "NYT"
                    if result['newspaper'] == 2:
                        paper = "BBC"
                    if result['newspaper'] == 3:
                        paper = "FN"
                    result_list = [result['date'].strftime("%m/%d/%y"), paper, result['headline'], result[this_emotion], result['link']]
                    formated_list.append(result_list)

                list_output.append(formated_list)
            return list_output

        all_emotions_queries_list = [headline_emotion_query_trust, headline_emotion_query_joy, headline_emotion_query_anticip, headline_emotion_query_surprise, headline_emotion_query_fear, headline_emotion_query_sadness, headline_emotion_query_anger, headline_emotion_query_disgust]


        all_emotions_query = format_emotion_query(all_emotions_queries_list)
        return all_emotions_query

    nyt_trust_formatted = get_emotions_formatted_by_paper(1)[0]
    nyt_joy_formatted = get_emotions_formatted_by_paper(1)[1]
    nyt_anticip_formatted = get_emotions_formatted_by_paper(1)[2]
    nyt_surprise_formatted = get_emotions_formatted_by_paper(1)[3]
    nyt_fear_formatted = get_emotions_formatted_by_paper(1)[4]
    nyt_sadness_formatted = get_emotions_formatted_by_paper(1)[5]
    nyt_anger_formatted = get_emotions_formatted_by_paper(1)[6]
    nyt_disgust_formatted = get_emotions_formatted_by_paper(1)[7]

    bbc_trust_formatted = get_emotions_formatted_by_paper(2)[0]
    bbc_joy_formatted = get_emotions_formatted_by_paper(2)[1]
    bbc_anticip_formatted = get_emotions_formatted_by_paper(2)[2]
    bbc_surprise_formatted = get_emotions_formatted_by_paper(2)[3]
    bbc_fear_formatted = get_emotions_formatted_by_paper(2)[4]
    bbc_sadness_formatted = get_emotions_formatted_by_paper(2)[5]
    bbc_anger_formatted = get_emotions_formatted_by_paper(2)[6]
    bbc_disgust_formatted = get_emotions_formatted_by_paper(2)[7]

    fn_trust_formatted = get_emotions_formatted_by_paper(3)[0]
    fn_joy_formatted = get_emotions_formatted_by_paper(3)[1]
    fn_anticip_formatted = get_emotions_formatted_by_paper(3)[2]
    fn_surprise_formatted = get_emotions_formatted_by_paper(3)[3]
    fn_fear_formatted = get_emotions_formatted_by_paper(3)[4]
    fn_sadness_formatted = get_emotions_formatted_by_paper(3)[5]
    fn_anger_formatted = get_emotions_formatted_by_paper(3)[6]
    fn_disgust_formatted = get_emotions_formatted_by_paper(3)[7]







    df_radar = pd.DataFrame(dict(
    r=[disgust_overall, trust_overall, joy_overall, anticip_overall, surprise_overall, fear_overall, sadness_overall, anger_overall],
    theta=categories))
    fig_radar = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
    radar_overall = str(plotly.offline.plot(fig_radar, output_type='div', config = {'displayModeBar': False}))

    template = loader.get_template('custom_scraper/emotion_newspaper.html')


    context = {'radar_overall': radar_overall,'html_div_emotion_radar_nyt': html_div_emotion_radar_nyt, 'html_div_emotion_radar_bbc': html_div_emotion_radar_bbc, 'html_div_emotion_radar_fn': html_div_emotion_radar_fn, 'bbc_joy_formatted':bbc_joy_formatted, 'bbc_anticip_formatted':bbc_anticip_formatted, 'bbc_surprise_formatted':bbc_surprise_formatted, 'bbc_fear_formatted':bbc_fear_formatted, 'bbc_sadness_formatted':bbc_sadness_formatted, 'bbc_anger_formatted':bbc_anger_formatted, 'bbc_disgust_formatted':bbc_disgust_formatted, 'bbc_trust_formatted':bbc_trust_formatted,'fn_joy_formatted':fn_joy_formatted, 'fn_anticip_formatted':fn_anticip_formatted, 'fn_surprise_formatted':fn_surprise_formatted, 'fn_fear_formatted':fn_fear_formatted, 'fn_sadness_formatted':fn_sadness_formatted, 'fn_anger_formatted':fn_anger_formatted, 'fn_disgust_formatted':fn_disgust_formatted, 'fn_trust_formatted':fn_trust_formatted,'nyt_joy_formatted':nyt_joy_formatted, 'nyt_anticip_formatted':nyt_anticip_formatted, 'nyt_surprise_formatted':nyt_surprise_formatted, 'nyt_fear_formatted':nyt_fear_formatted, 'nyt_sadness_formatted':nyt_sadness_formatted, 'nyt_anger_formatted':nyt_anger_formatted, 'nyt_disgust_formatted':nyt_disgust_formatted, 'nyt_trust_formatted':nyt_trust_formatted, 'joy_formatted':joy_formatted, 'anticip_formatted':anticip_formatted, 'surprise_formatted':surprise_formatted, 'fear_formatted':fear_formatted, 'sadness_formatted':sadness_formatted, 'anger_formatted':anger_formatted, 'disgust_formatted':disgust_formatted, 'trust_formatted':trust_formatted, 'overall_trust_tally':overall_trust_tally, 'overall_joy_tally':overall_joy_tally, 'overall_anticip_tally':overall_anticip_tally, 'overall_surprise_tally':overall_surprise_tally, 'overall_fear_tally': overall_fear_tally, 'overall_sadness_tally':overall_sadness_tally, 'overall_anger_tally':overall_anger_tally, 'overall_disgust_tally':overall_disgust_tally, 'fn_trust_tally':fn_trust_tally, 'fn_joy_tally':fn_joy_tally, 'fn_anticip_tally':fn_anticip_tally, 'fn_surprise_tally':fn_surprise_tally, 'fn_fear_tally': fn_fear_tally, 'fn_sadness_tally':fn_sadness_tally, 'fn_anger_tally':fn_anger_tally, 'fn_disgust_tally':fn_disgust_tally, 'nyt_trust_tally':nyt_trust_tally, 'nyt_joy_tally':nyt_joy_tally, 'nyt_anticip_tally':nyt_anticip_tally, 'nyt_surprise_tally':nyt_surprise_tally, 'nyt_fear_tally': nyt_fear_tally, 'nyt_sadness_tally':nyt_sadness_tally, 'nyt_anger_tally':nyt_anger_tally, 'nyt_disgust_tally':nyt_disgust_tally, 'bbc_trust_tally':bbc_trust_tally, 'bbc_joy_tally':bbc_joy_tally, 'bbc_anticip_tally':bbc_anticip_tally, 'bbc_surprise_tally':bbc_surprise_tally, 'bbc_fear_tally': bbc_fear_tally, 'bbc_sadness_tally':bbc_sadness_tally, 'bbc_anger_tally':bbc_anger_tally, 'bbc_disgust_tally':bbc_disgust_tally,  'trust_all': trust_all, 'joy_all': joy_all, 'anticipation_all': anticipation_all, 'surprise_all': surprise_all, 'fear_all': fear_all, 'sadness_all': sadness_all, 'anger_all': anger_all, 'disgust_all': disgust_all, 'trust_nyt': trust_nyt, 'joy_nyt': joy_nyt, 'anticipation_nyt': anticipation_nyt, 'surprise_nyt': surprise_nyt, 'fear_nyt': fear_nyt, 'sadness_nyt': sadness_nyt, 'anger_nyt': anger_nyt, 'disgust_nyt': disgust_nyt, 'trust_bbc': trust_bbc, 'joy_bbc': joy_bbc, 'anticipation_bbc': anticipation_bbc, 'surprise_bbc': surprise_bbc, 'fear_bbc': fear_bbc, 'sadness_bbc': sadness_bbc, 'anger_bbc': anger_bbc, 'disgust_bbc': disgust_bbc, 'trust_fn': trust_fn, 'joy_fn': joy_fn, 'anticipation_fn': anticipation_fn, 'surprise_fn': surprise_fn, 'fear_fn': fear_fn, 'sadness_fn': sadness_fn, 'anger_fn': anger_fn, 'disgust_fn': disgust_fn, 'html_div_emotion_bar': html_div_emotion_bar, 'html_div_emotion_bar_nyt': html_div_emotion_bar_nyt, 'html_div_emotion_bar_bbc': html_div_emotion_bar_bbc, 'html_div_emotion_bar_fn': html_div_emotion_bar_fn, 'html_div_emotion_month_nyt': html_div_emotion_month_nyt, 'html_div_emotion_month_bbc': html_div_emotion_month_bbc, 'html_div_emotion_month_fn': html_div_emotion_month_fn, 'html_div_emotion_month': html_div_emotion_month, 'html_div_emotion_nyt': html_div_emotion_nyt, 'html_div_emotion_bbc': html_div_emotion_bbc, 'html_div_emotion_fn': html_div_emotion_fn,   'html_div_emotion_overall': html_div_emotion_overall}
    cache_test = HttpResponse(template.render(context, request),)

    cache_test = cache_test.content.decode("utf-8")
    html_cache_save = html_cache(page_num=4, cache_html=cache_test)
    html_cache_save.save()


    return render(request, 'custom_scraper/emotion_newspaper.html',{'radar_overall': radar_overall,'html_div_emotion_radar_nyt': html_div_emotion_radar_nyt, 'html_div_emotion_radar_bbc': html_div_emotion_radar_bbc, 'html_div_emotion_radar_fn': html_div_emotion_radar_fn, 'bbc_joy_formatted':bbc_joy_formatted, 'bbc_anticip_formatted':bbc_anticip_formatted, 'bbc_surprise_formatted':bbc_surprise_formatted, 'bbc_fear_formatted':bbc_fear_formatted, 'bbc_sadness_formatted':bbc_sadness_formatted, 'bbc_anger_formatted':bbc_anger_formatted, 'bbc_disgust_formatted':bbc_disgust_formatted, 'bbc_trust_formatted':bbc_trust_formatted,'fn_joy_formatted':fn_joy_formatted, 'fn_anticip_formatted':fn_anticip_formatted, 'fn_surprise_formatted':fn_surprise_formatted, 'fn_fear_formatted':fn_fear_formatted, 'fn_sadness_formatted':fn_sadness_formatted, 'fn_anger_formatted':fn_anger_formatted, 'fn_disgust_formatted':fn_disgust_formatted, 'fn_trust_formatted':fn_trust_formatted,'nyt_joy_formatted':nyt_joy_formatted, 'nyt_anticip_formatted':nyt_anticip_formatted, 'nyt_surprise_formatted':nyt_surprise_formatted, 'nyt_fear_formatted':nyt_fear_formatted, 'nyt_sadness_formatted':nyt_sadness_formatted, 'nyt_anger_formatted':nyt_anger_formatted, 'nyt_disgust_formatted':nyt_disgust_formatted, 'nyt_trust_formatted':nyt_trust_formatted, 'joy_formatted':joy_formatted, 'anticip_formatted':anticip_formatted, 'surprise_formatted':surprise_formatted, 'fear_formatted':fear_formatted, 'sadness_formatted':sadness_formatted, 'anger_formatted':anger_formatted, 'disgust_formatted':disgust_formatted, 'trust_formatted':trust_formatted, 'overall_trust_tally':overall_trust_tally, 'overall_joy_tally':overall_joy_tally, 'overall_anticip_tally':overall_anticip_tally, 'overall_surprise_tally':overall_surprise_tally, 'overall_fear_tally': overall_fear_tally, 'overall_sadness_tally':overall_sadness_tally, 'overall_anger_tally':overall_anger_tally, 'overall_disgust_tally':overall_disgust_tally, 'fn_trust_tally':fn_trust_tally, 'fn_joy_tally':fn_joy_tally, 'fn_anticip_tally':fn_anticip_tally, 'fn_surprise_tally':fn_surprise_tally, 'fn_fear_tally': fn_fear_tally, 'fn_sadness_tally':fn_sadness_tally, 'fn_anger_tally':fn_anger_tally, 'fn_disgust_tally':fn_disgust_tally, 'nyt_trust_tally':nyt_trust_tally, 'nyt_joy_tally':nyt_joy_tally, 'nyt_anticip_tally':nyt_anticip_tally, 'nyt_surprise_tally':nyt_surprise_tally, 'nyt_fear_tally': nyt_fear_tally, 'nyt_sadness_tally':nyt_sadness_tally, 'nyt_anger_tally':nyt_anger_tally, 'nyt_disgust_tally':nyt_disgust_tally, 'bbc_trust_tally':bbc_trust_tally, 'bbc_joy_tally':bbc_joy_tally, 'bbc_anticip_tally':bbc_anticip_tally, 'bbc_surprise_tally':bbc_surprise_tally, 'bbc_fear_tally': bbc_fear_tally, 'bbc_sadness_tally':bbc_sadness_tally, 'bbc_anger_tally':bbc_anger_tally, 'bbc_disgust_tally':bbc_disgust_tally,  'trust_all': trust_all, 'joy_all': joy_all, 'anticipation_all': anticipation_all, 'surprise_all': surprise_all, 'fear_all': fear_all, 'sadness_all': sadness_all, 'anger_all': anger_all, 'disgust_all': disgust_all, 'trust_nyt': trust_nyt, 'joy_nyt': joy_nyt, 'anticipation_nyt': anticipation_nyt, 'surprise_nyt': surprise_nyt, 'fear_nyt': fear_nyt, 'sadness_nyt': sadness_nyt, 'anger_nyt': anger_nyt, 'disgust_nyt': disgust_nyt, 'trust_bbc': trust_bbc, 'joy_bbc': joy_bbc, 'anticipation_bbc': anticipation_bbc, 'surprise_bbc': surprise_bbc, 'fear_bbc': fear_bbc, 'sadness_bbc': sadness_bbc, 'anger_bbc': anger_bbc, 'disgust_bbc': disgust_bbc, 'trust_fn': trust_fn, 'joy_fn': joy_fn, 'anticipation_fn': anticipation_fn, 'surprise_fn': surprise_fn, 'fear_fn': fear_fn, 'sadness_fn': sadness_fn, 'anger_fn': anger_fn, 'disgust_fn': disgust_fn, 'html_div_emotion_bar': html_div_emotion_bar, 'html_div_emotion_bar_nyt': html_div_emotion_bar_nyt, 'html_div_emotion_bar_bbc': html_div_emotion_bar_bbc, 'html_div_emotion_bar_fn': html_div_emotion_bar_fn, 'html_div_emotion_month_nyt': html_div_emotion_month_nyt, 'html_div_emotion_month_bbc': html_div_emotion_month_bbc, 'html_div_emotion_month_fn': html_div_emotion_month_fn, 'html_div_emotion_month': html_div_emotion_month, 'html_div_emotion_nyt': html_div_emotion_nyt, 'html_div_emotion_bbc': html_div_emotion_bbc, 'html_div_emotion_fn': html_div_emotion_fn,   'html_div_emotion_overall': html_div_emotion_overall})



def emotion_compare(request):

    from django.db.models import Count

    from datetime import datetime


    today = datetime.today()
    yesterday = today - timedelta(1)
    today = str(today)[:10]

    yesterday = str(yesterday)[:10]
    cached = False

    if html_cache.objects.filter(date__contains=today).filter(page_num=5):
        html_record = html_cache.objects.filter(date__contains=today).filter(page_num=5).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/emotion_compare.html',{'html':html, 'cached':cached},)

    if html_cache.objects.filter(date__contains=yesterday).filter(page_num=5):
        html_record = html_cache.objects.filter(date__contains=yesterday).filter(page_num=5).values('cache_html')[0]
        html = html_record['cache_html']
        cached = True
        return render(request, 'custom_scraper/emotion_compare.html',{'html':html, 'cached':cached},)




    emotion_list = []
    for i in range(1,4):
        count_of_emotion_by_newspaper = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(newspaper=i).filter(fear__gt=0).values('headline_id','newspaper').annotate(HL_Count=Count('id'))

        new_dict = {}
        new_dict['Newspaper'] = i
        new_dict['Emotion'] = 'Fear'
        new_dict['Count'] = len(count_of_emotion_by_newspaper)
        emotion_list.append(new_dict)

    for i in range(1,4):
        count_of_emotion_by_newspaper = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(newspaper=i).filter(anger__gt=0).values('headline_id','newspaper').annotate(HL_Count=Count('id'))

        new_dict = {}
        new_dict['Newspaper'] = i
        new_dict['Emotion'] = 'Anger'
        new_dict['Count'] = len(count_of_emotion_by_newspaper)
        emotion_list.append(new_dict)

    for i in range(1,4):
        count_of_emotion_by_newspaper = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(newspaper=i).filter(anticip__gt=0).values('headline_id','newspaper').annotate(HL_Count=Count('id'))

        new_dict = {}
        new_dict['Newspaper'] = i
        new_dict['Emotion'] = 'Anticipation'
        new_dict['Count'] = len(count_of_emotion_by_newspaper)
        emotion_list.append(new_dict)

    for i in range(1,4):
        count_of_emotion_by_newspaper = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(newspaper=i).filter(trust__gt=0).values('headline_id','newspaper').annotate(HL_Count=Count('id'))

        new_dict = {}
        new_dict['Newspaper'] = i
        new_dict['Emotion'] = 'Trust'
        new_dict['Count'] = len(count_of_emotion_by_newspaper)
        emotion_list.append(new_dict)

    for i in range(1,4):
        count_of_emotion_by_newspaper = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(newspaper=i).filter(surprise__gt=0).values('headline_id','newspaper').annotate(HL_Count=Count('id'))

        new_dict = {}
        new_dict['Newspaper'] = i
        new_dict['Emotion'] = 'Surprise'
        new_dict['Count'] = len(count_of_emotion_by_newspaper)
        emotion_list.append(new_dict)

    for i in range(1,4):
        count_of_emotion_by_newspaper = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(newspaper=i).filter(sadness__gt=0).values('headline_id','newspaper').annotate(HL_Count=Count('id'))

        new_dict = {}
        new_dict['Newspaper'] = i
        new_dict['Emotion'] = 'Sadness'
        new_dict['Count'] = len(count_of_emotion_by_newspaper)
        emotion_list.append(new_dict)

    for i in range(1,4):
        count_of_emotion_by_newspaper = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(newspaper=i).filter(disgust__gt=0).values('headline_id','newspaper').annotate(HL_Count=Count('id'))

        new_dict = {}
        new_dict['Newspaper'] = i
        new_dict['Emotion'] = 'Disgust'
        new_dict['Count'] = len(count_of_emotion_by_newspaper)
        emotion_list.append(new_dict)


    for i in range(1,4):
        count_of_emotion_by_newspaper = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(newspaper=i).filter(joy__gt=0).values('headline_id','newspaper').annotate(HL_Count=Count('id'))

        new_dict = {}
        new_dict['Newspaper'] = i
        new_dict['Emotion'] = 'Joy'
        new_dict['Count'] = len(count_of_emotion_by_newspaper)
        emotion_list.append(new_dict)




    comparesent_month = pd.DataFrame(emotion_list)
    comparesent_month['Count'] = comparesent_month['Count']
    comparesent_month['Newspaper'] = comparesent_month['Newspaper'].replace(1, 'The New York Times')
    comparesent_month['Newspaper'] = comparesent_month['Newspaper'].replace(2, 'BBC News')
    comparesent_month['Newspaper'] = comparesent_month['Newspaper'].replace(3, 'Fox News')





    figcompare_month_pos = px.line(comparesent_month, x="Emotion", y="Count", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )


    figcompare_month_pos.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions = str(plotly.offline.plot(figcompare_month_pos, output_type='div', config = {'displayModeBar': False}))





    def get_emotion_tables(paper_num):
        emotion_table_query = top_words_emotions_percent.objects.filter(date__contains=today).filter(newspaper=paper_num).values("word", 'fear_percent', 'anger_percent', 'anticip_percent', 'trust_percent', 'surprise_percent', 'sadness_percent', 'disgust_percent', 'joy_percent')
        trust_tally = []
        joy_tally = []
        anticip_tally = []
        surprise_tally = []
        fear_tally = []
        sadness_tally = []
        anger_tally=[]
        disgust_tally = []
        for result in emotion_table_query:
            trust_tally.append([result['word'], round(result['trust_percent']*100)])
            joy_tally.append([result['word'], round(result['joy_percent']*100)])
            anticip_tally.append([result['word'], round(result['anticip_percent']*100)])
            surprise_tally.append([result['word'], round(result['surprise_percent']*100)])
            fear_tally.append([result['word'], round(result['fear_percent']*100)])
            sadness_tally.append([result['word'], round(result['sadness_percent']*100)])
            anger_tally.append([result['word'], round(result['anger_percent']*100)])
            disgust_tally.append([result['word'], round(result['disgust_percent']*100)])

        trust_tally = sorted(trust_tally, key=lambda x:x[1], reverse=True)
        joy_tally = sorted(joy_tally, key=lambda x:x[1], reverse=True)
        anticip_tally = sorted(anticip_tally, key=lambda x:x[1], reverse=True)
        surprise_tally = sorted(surprise_tally, key=lambda x:x[1], reverse=True)
        fear_tally = sorted(fear_tally, key=lambda x:x[1], reverse=True)
        sadness_tally = sorted(sadness_tally, key=lambda x:x[1], reverse=True)
        anger_tally = sorted(anger_tally, key=lambda x:x[1], reverse=True)

        disgust_tally = sorted(disgust_tally, key=lambda x:x[1], reverse=True)

        return trust_tally, joy_tally, anticip_tally, surprise_tally, fear_tally, sadness_tally, anger_tally, disgust_tally

    nyt_emotion_tables = get_emotion_tables(1)
    bbc_emotion_tables = get_emotion_tables(2)
    fn_emotion_tables = get_emotion_tables(3)


    nyt_trust_tally = nyt_emotion_tables[0]
    nyt_joy_tally = nyt_emotion_tables[1]
    nyt_anticip_tally = nyt_emotion_tables[2]
    nyt_surprise_tally = nyt_emotion_tables[3]
    nyt_fear_tally = nyt_emotion_tables[4]
    nyt_sadness_tally = nyt_emotion_tables[5]
    nyt_anger_tally = nyt_emotion_tables[6]
    nyt_disgust_tally = nyt_emotion_tables[7]

    bbc_trust_tally = bbc_emotion_tables[0]
    bbc_joy_tally = bbc_emotion_tables[1]
    bbc_anticip_tally = bbc_emotion_tables[2]
    bbc_surprise_tally = bbc_emotion_tables[3]
    bbc_fear_tally = bbc_emotion_tables[4]
    bbc_sadness_tally = bbc_emotion_tables[5]
    bbc_anger_tally = bbc_emotion_tables[6]
    bbc_disgust_tally = bbc_emotion_tables[7]

    fn_trust_tally = fn_emotion_tables[0]
    fn_joy_tally = fn_emotion_tables[1]
    fn_anticip_tally = fn_emotion_tables[2]
    fn_surprise_tally = fn_emotion_tables[3]
    fn_fear_tally = fn_emotion_tables[4]
    fn_sadness_tally = fn_emotion_tables[5]
    fn_anger_tally = fn_emotion_tables[6]
    fn_disgust_tally = fn_emotion_tables[7]

    #create monthly chart of each emotion
    #figure out what format we need the data in

    #daily for fear
    query_daily_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(fear__gt=0).values('newspaper').annotate(Date=TruncDay("date")).annotate(Count=Count("id")).order_by('Date')
    query_daily_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(anger__gt=0).values('newspaper').annotate(Date=TruncDay("date")).annotate(Count=Count("id")).order_by('Date')
    query_daily_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(anticip__gt=0).values('newspaper').annotate(Date=TruncDay("date")).annotate(Count=Count("id")).order_by('Date')
    query_daily_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(trust__gt=0).values('newspaper').annotate(Date=TruncDay("date")).annotate(Count=Count("id")).order_by('Date')
    query_daily_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(surprise__gt=0).values('newspaper').annotate(Date=TruncDay("date")).annotate(Count=Count("id")).order_by('Date')
    query_daily_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(sadness__gt=0).values('newspaper').annotate(Date=TruncDay("date")).annotate(Count=Count("id")).order_by('Date')
    query_daily_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(disgust__gt=0).values('newspaper').annotate(Date=TruncDay("date")).annotate(Count=Count("id")).order_by('Date')
    query_daily_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(joy__gt=0).values('newspaper').annotate(Date=TruncDay("date")).annotate(Count=Count("id")).order_by('Date')

    query_monthly_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(fear__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(Count=Count("id")).order_by('Date')
    query_monthly_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(anger__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(Count=Count("id")).order_by('Date')
    query_monthly_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(anticip__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(Count=Count("id")).order_by('Date')
    query_monthly_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(trust__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(Count=Count("id")).order_by('Date')
    query_monthly_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(surprise__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(Count=Count("id")).order_by('Date')
    query_monthly_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(sadness__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(Count=Count("id")).order_by('Date')
    query_monthly_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(disgust__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(Count=Count("id")).order_by('Date')
    query_monthly_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(joy__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(Count=Count("id")).order_by('Date')


    def get_daily_emotion_plot(emotion_query):
        comparesent = pd.DataFrame(list(emotion_query))
        comparesent['newspaper'] = comparesent['newspaper'].replace(1, 'The New York Times')
        comparesent['newspaper'] = comparesent['newspaper'].replace(2, 'BBC News')
        comparesent['newspaper'] = comparesent['newspaper'].replace(3, 'Fox News')
        comparesent.rename(columns={'newspaper':'Newspaper'}, inplace= True)


        figcompare = px.line(comparesent, x="Date", y="Count", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )


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

        return html_div_compare


    def get_monthly_emotion_plot(emotion_query):
        comparesent = pd.DataFrame(list(emotion_query))
        comparesent['newspaper'] = comparesent['newspaper'].replace(1, 'The New York Times')
        comparesent['newspaper'] = comparesent['newspaper'].replace(2, 'BBC News')
        comparesent['newspaper'] = comparesent['newspaper'].replace(3, 'Fox News')
        comparesent.rename(columns={'newspaper':'Newspaper'}, inplace= True)


        figcompare = px.line(comparesent, x="Date", y="Count", color="Newspaper", color_discrete_map={'The New York Times':"#8e949e",'BBC News':"#e61e1e",'Fox News':"#006edb" }  )


        figcompare.update_layout(
            font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




        html_div_compare = str(plotly.offline.plot(figcompare, output_type='div', config = {'displayModeBar': False}))

        return html_div_compare

    trust_daily_plot = get_daily_emotion_plot(query_daily_trust)
    trust_monthly_plot = get_monthly_emotion_plot(query_monthly_trust)
    joy_daily_plot = get_daily_emotion_plot(query_daily_joy)
    joy_monthly_plot = get_monthly_emotion_plot(query_monthly_joy)
    anticip_daily_plot = get_daily_emotion_plot(query_daily_anticip)
    anticip_monthly_plot = get_monthly_emotion_plot(query_monthly_anticip)
    surprise_daily_plot = get_daily_emotion_plot(query_daily_surprise)
    surprise_monthly_plot = get_monthly_emotion_plot(query_monthly_surprise)
    fear_daily_plot = get_daily_emotion_plot(query_daily_fear)
    fear_monthly_plot = get_monthly_emotion_plot(query_monthly_fear)
    sadness_daily_plot = get_daily_emotion_plot(query_daily_sadness)
    sadness_monthly_plot = get_monthly_emotion_plot(query_monthly_sadness)
    anger_daily_plot = get_daily_emotion_plot(query_daily_anger)
    anger_monthly_plot = get_monthly_emotion_plot(query_monthly_anger)
    disgust_daily_plot = get_daily_emotion_plot(query_daily_disgust)
    disgust_monthly_plot = get_monthly_emotion_plot(query_monthly_disgust)

    #get count of words that show up much often in headlines marked "trust"

    #find headline_id of headlines marked "trust"
    trust_headline_ids = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(trust__gt=0).values("headline_id").annotate(Count=Count("id"))
    joy_headline_ids = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(joy__gt=0).values("headline_id").annotate(Count=Count("id"))
    anticip_headline_ids = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(anticip__gt=0).values("headline_id").annotate(Count=Count("id"))
    surprise_headline_ids = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(surprise__gt=0).values("headline_id").annotate(Count=Count("id"))
    fear_headline_ids = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(fear__gt=0).values("headline_id").annotate(Count=Count("id"))
    sadness_headline_ids = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(sadness__gt=0).values("headline_id").annotate(Count=Count("id"))
    anger_headline_ids = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(anger__gt=0).values("headline_id").annotate(Count=Count("id"))
    disgust_headline_ids = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(disgust__gt=0).values("headline_id").annotate(Count=Count("id"))
    """
    #find most common words in these headlines
    def find_most_common_word(headline_id_query):
        counting_dict = {}
        for result in headline_id_query:
            terms_in_headline_query = hl_tokens_emotions.objects.filter(headline_id=result['headline_id']).values('word')
            for word_result in terms_in_headline_query:
                if word_result['word'] in counting_dict:
                    counting_dict[word_result['word']] += 1
                    print(counting_dict)
                else:
                    counting_dict[word_result['word']] = 1
                    print(counting_dict)

        return counting_dict

    print(find_most_common_word(trust_headline_ids))
    """
    all_trust_word_query = hl_tokens_emotions.objects.filter(day_order__lte=25).values('headline_id', 'word', 'newspaper')

    all_trust_headline_id = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(trust__gt=0).values('headline_id')
    all_joy_headline_id = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(joy__gt=0).values('headline_id')
    all_surprise_headline_id = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(surprise__gt=0).values('headline_id')
    all_fear_headline_id = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(fear__gt=0).values('headline_id')
    all_sadness_headline_id = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(sadness__gt=0).values('headline_id')
    all_anger_headline_id = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(anger__gt=0).values('headline_id')
    all_disgust_headline_id = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(disgust__gt=0).values('headline_id')
    all_anticip_headline_id = hl_tokens_emotions.objects.filter(day_order__lte=25).filter(anticip__gt=0).values('headline_id')

    def most_occuring_words_by_paper_in_headlines_with_emotion(all_trust_headline_ids, all_trust_words_query):
        trust_headline_id_dict = {}
        for result in all_trust_headline_ids:
            if result['headline_id'] not in trust_headline_id_dict:
                trust_headline_id_dict[result['headline_id']] = 1



        trust_word_count_nyt = {}
        trust_word_count_bbc = {}
        trust_word_count_fn = {}
        for result in all_trust_words_query:
            if result['headline_id'] in trust_headline_id_dict:
                if result['newspaper'] == 1:
                    if result['word'] not in trust_word_count_nyt:
                        trust_word_count_nyt[result['word']] = 1
                    else:
                        trust_word_count_nyt[result['word']] += 1
                if result['newspaper'] == 2:
                    if result['word'] not in trust_word_count_bbc:
                        trust_word_count_bbc[result['word']] = 1
                    else:
                        trust_word_count_bbc[result['word']] += 1
                if result['newspaper'] == 3:
                    if result['word'] not in trust_word_count_fn:
                        trust_word_count_fn[result['word']] = 1
                    else:
                        trust_word_count_fn[result['word']] += 1






        sorted_trust_word_count_nyt = {k: v for k, v in sorted(trust_word_count_nyt.items(), key=lambda item: item[1], reverse=True)}
        sorted_trust_word_count_bbc = {k: v for k, v in sorted(trust_word_count_bbc.items(), key=lambda item: item[1], reverse=True)}
        sorted_trust_word_count_fn = {k: v for k, v in sorted(trust_word_count_fn.items(), key=lambda item: item[1], reverse=True)}

        nyt_count_list = []

        for key, term in sorted_trust_word_count_nyt.items():
            if len(nyt_count_list) < 51:
                nyt_count_list.append([key,term])

        bbc_count_list = []

        for key, term in sorted_trust_word_count_bbc.items():
            if len(bbc_count_list) < 51:
                bbc_count_list.append([key,term])

        fn_count_list = []

        for key, term in sorted_trust_word_count_fn.items():
            if len(fn_count_list) < 51:
                fn_count_list.append([key,term])

        return nyt_count_list, bbc_count_list, fn_count_list

    trust_lists = most_occuring_words_by_paper_in_headlines_with_emotion(all_trust_headline_id, all_trust_word_query)
    joy_lists = most_occuring_words_by_paper_in_headlines_with_emotion(all_joy_headline_id, all_trust_word_query)
    surprise_lists = most_occuring_words_by_paper_in_headlines_with_emotion(all_surprise_headline_id, all_trust_word_query)
    fear_lists = most_occuring_words_by_paper_in_headlines_with_emotion(all_fear_headline_id, all_trust_word_query)
    sadness_lists = most_occuring_words_by_paper_in_headlines_with_emotion(all_sadness_headline_id, all_trust_word_query)
    anger_lists = most_occuring_words_by_paper_in_headlines_with_emotion(all_anger_headline_id, all_trust_word_query)
    disgust_lists = most_occuring_words_by_paper_in_headlines_with_emotion(all_disgust_headline_id, all_trust_word_query)
    anticip_lists = most_occuring_words_by_paper_in_headlines_with_emotion(all_anticip_headline_id, all_trust_word_query)

    nyt_trust_list = trust_lists[0]
    bbc_trust_list = trust_lists[1]
    fn_trust_list = trust_lists[2]

    nyt_joy_list = joy_lists[0]
    bbc_joy_list = joy_lists[1]
    fn_joy_list = joy_lists[2]

    nyt_surprise_list = surprise_lists[0]
    bbc_surprise_list = surprise_lists[1]
    fn_surprise_list = surprise_lists[2]

    nyt_fear_list = fear_lists[0]
    bbc_fear_list = fear_lists[1]
    fn_fear_list = fear_lists[2]

    nyt_sadness_list = sadness_lists[0]
    bbc_sadness_list = sadness_lists[1]
    fn_sadness_list = sadness_lists[2]

    nyt_anger_list = anger_lists[0]
    bbc_anger_list = anger_lists[1]
    fn_anger_list = anger_lists[2]

    nyt_disgust_list = disgust_lists[0]
    bbc_disgust_list = disgust_lists[1]
    fn_disgust_list = disgust_lists[2]

    nyt_anticip_list = anticip_lists[0]
    bbc_anticip_list = anticip_lists[1]
    fn_anticip_list = anticip_lists[2]
    #below is generalized headline_query have to make it so that can generate different hl lists out of it for each newspaper
    headlines_indicating_trust_query = Headline_emotion.objects.filter(day_order__lte=25).filter(trust__gt=0).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link', 'newspaper').order_by("Date")
    headlines_indicating_surprise_query = Headline_emotion.objects.filter(day_order__lte=25).filter(surprise__gt=0).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link', 'newspaper').order_by("Date")
    headlines_indicating_fear_query = Headline_emotion.objects.filter(day_order__lte=25).filter(fear__gt=0).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link', 'newspaper').order_by("Date")
    headlines_indicating_sadness_query = Headline_emotion.objects.filter(day_order__lte=25).filter(sadness__gt=0).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link', 'newspaper').order_by("Date")
    headlines_indicating_anger_query = Headline_emotion.objects.filter(day_order__lte=25).filter(anger__gt=0).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link', 'newspaper').order_by("Date")
    headlines_indicating_disgust_query = Headline_emotion.objects.filter(day_order__lte=25).filter(disgust__gt=0).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link', 'newspaper').order_by("Date")
    headlines_indicating_anticip_query = Headline_emotion.objects.filter(day_order__lte=25).filter(anticip__gt=0).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link', 'newspaper').order_by("Date")
    headlines_indicating_joy_query = Headline_emotion.objects.filter(day_order__lte=25).filter(joy__gt=0).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link', 'newspaper').order_by("Date")


    def get_hl_lists(hl_query):
        nyt_list = []
        bbc_list = []
        fn_list = []

        for result in hl_query:
            if result['newspaper'] == 1:
                nyt_list.append([result['Date'].date(), result['headline'], result['link']])
            if result['newspaper'] == 2:
                bbc_list.append([result['Date'], result['headline'], result['link']])
            if result['newspaper'] == 3:
                fn_list.append([result['Date'], result['headline'], result['link']])
        return nyt_list, bbc_list, fn_list

    joy_hl_lists = get_hl_lists(headlines_indicating_joy_query)
    trust_hl_lists = get_hl_lists(headlines_indicating_trust_query)
    sadness_hl_lists = get_hl_lists(headlines_indicating_sadness_query)
    disgust_hl_lists = get_hl_lists(headlines_indicating_disgust_query)
    fear_hl_lists = get_hl_lists(headlines_indicating_fear_query)
    anger_hl_lists = get_hl_lists(headlines_indicating_anger_query)
    anticip_hl_lists = get_hl_lists(headlines_indicating_anticip_query)
    surprise_hl_lists = get_hl_lists(headlines_indicating_surprise_query)

    joy_nyt_hls = joy_hl_lists[0]
    joy_bbc_hls = joy_hl_lists[1]
    joy_fn_hls = joy_hl_lists[2]

    anger_nyt_hls = anger_hl_lists[0]
    anger_bbc_hls = anger_hl_lists[1]
    anger_fn_hls = anger_hl_lists[2]

    fear_nyt_hls = fear_hl_lists[0]
    fear_bbc_hls = fear_hl_lists[1]
    fear_fn_hls = fear_hl_lists[2]

    disgust_nyt_hls = disgust_hl_lists[0]
    disgust_bbc_hls = disgust_hl_lists[1]
    disgust_fn_hls = disgust_hl_lists[2]

    trust_nyt_hls = trust_hl_lists[0]
    trust_bbc_hls = trust_hl_lists[1]
    trust_fn_hls = trust_hl_lists[2]

    surprise_nyt_hls = surprise_hl_lists[0]
    surprise_bbc_hls = surprise_hl_lists[1]
    surprise_fn_hls = surprise_hl_lists[2]

    anticip_nyt_hls = anticip_hl_lists[0]
    anticip_bbc_hls = anticip_hl_lists[1]
    anticip_fn_hls = anticip_hl_lists[2]

    sadness_nyt_hls = sadness_hl_lists[0]
    sadness_bbc_hls = sadness_hl_lists[1]
    sadness_fn_hls = sadness_hl_lists[2]


    headline_emotion_query_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(trust__gt=1).values("date", "newspaper","headline", "trust", "link").order_by("-trust", "-date")[:50]
    headline_emotion_query_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(joy__gt=1).values("date", "newspaper","headline", "joy", "link").order_by("-joy", "-date")[:50]
    headline_emotion_query_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(anticip__gt=1).values("date", "newspaper","headline", "anticip", "link").order_by("-anticip", "-date")[:50]
    headline_emotion_query_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(surprise__gt=1).values("date", "newspaper","headline", "surprise", "link").order_by("-surprise", "-date")[:50]
    headline_emotion_query_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(fear__gt=1).values("date", "newspaper","headline", "fear", "link").order_by("-fear", "-date")[:50]
    headline_emotion_query_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(sadness__gt=1).values("date", "newspaper","headline", "sadness", "link").order_by("-sadness", "-date")[:50]
    headline_emotion_query_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(anger__gt=1).values("date", "newspaper","headline", "anger", "link").order_by("-anger", "-date")[:50]
    headline_emotion_query_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(disgust__gt=1).values("date", "newspaper","headline", "disgust", "link").order_by("-disgust", "-date")[:50]

    emotions = ['trust', 'joy', 'anticip', 'surprise', 'fear', 'sadness', 'anger', 'disgust']

    def format_emotion_query(list_of_emotion_queries):
        list_output = []
        for emotion_query in list_of_emotion_queries:

            formated_list = []
            for result in emotion_query:
                for emotion in emotions:
                    if emotion in result.keys():
                        this_emotion = emotion
                if result['newspaper'] == 1:
                    paper = "NYT"
                if result['newspaper'] == 2:
                    paper = "BBC"
                if result['newspaper'] == 3:
                    paper = "FN"
                result_list = [result['date'].strftime("%m/%d/%y"), paper, result['headline'], result[this_emotion], result['link']]
                formated_list.append(result_list)

            list_output.append(formated_list)
        return list_output

    all_emotions_queries_list = [headline_emotion_query_trust, headline_emotion_query_joy, headline_emotion_query_anticip, headline_emotion_query_surprise, headline_emotion_query_fear, headline_emotion_query_sadness, headline_emotion_query_anger, headline_emotion_query_disgust]

    all_emotions_query = format_emotion_query(all_emotions_queries_list)
    trust_formatted = all_emotions_query[0]
    joy_formatted = all_emotions_query[1]
    anticip_formatted = all_emotions_query[2]
    surprise_formatted = all_emotions_query[3]
    fear_formatted = all_emotions_query[4]
    sadness_formatted = all_emotions_query[5]
    anger_formatted = all_emotions_query[6]
    disgust_formatted = all_emotions_query[7]

    def get_emotion_tables(paper_num):
        emotion_table_query = top_words_emotions_percent.objects.filter(date__contains=today).filter(newspaper=paper_num).values("word", 'fear_percent', 'anger_percent', 'anticip_percent', 'trust_percent', 'surprise_percent', 'sadness_percent', 'disgust_percent', 'joy_percent')
        trust_tally = []
        joy_tally = []
        anticip_tally = []
        surprise_tally = []
        fear_tally = []
        sadness_tally = []
        anger_tally=[]
        disgust_tally = []
        for result in emotion_table_query:
            trust_tally.append([result['word'], round(result['trust_percent']*100)])
            joy_tally.append([result['word'], round(result['joy_percent']*100)])
            anticip_tally.append([result['word'], round(result['anticip_percent']*100)])
            surprise_tally.append([result['word'], round(result['surprise_percent']*100)])
            fear_tally.append([result['word'], round(result['fear_percent']*100)])
            sadness_tally.append([result['word'], round(result['sadness_percent']*100)])
            anger_tally.append([result['word'], round(result['anger_percent']*100)])
            disgust_tally.append([result['word'], round(result['disgust_percent']*100)])

        trust_tally = sorted(trust_tally, key=lambda x:x[1], reverse=True)
        joy_tally = sorted(joy_tally, key=lambda x:x[1], reverse=True)
        anticip_tally = sorted(anticip_tally, key=lambda x:x[1], reverse=True)
        surprise_tally = sorted(surprise_tally, key=lambda x:x[1], reverse=True)
        fear_tally = sorted(fear_tally, key=lambda x:x[1], reverse=True)
        sadness_tally = sorted(sadness_tally, key=lambda x:x[1], reverse=True)
        anger_tally = sorted(anger_tally, key=lambda x:x[1], reverse=True)

        disgust_tally = sorted(disgust_tally, key=lambda x:x[1], reverse=True)

        return trust_tally, joy_tally, anticip_tally, surprise_tally, fear_tally, sadness_tally, anger_tally, disgust_tally

    nyt_emotion_tables = get_emotion_tables(1)
    bbc_emotion_tables = get_emotion_tables(2)
    fn_emotion_tables = get_emotion_tables(3)


    nyt_trust_tally = nyt_emotion_tables[0]
    nyt_joy_tally = nyt_emotion_tables[1]
    nyt_anticip_tally = nyt_emotion_tables[2]
    nyt_surprise_tally = nyt_emotion_tables[3]
    nyt_fear_tally = nyt_emotion_tables[4]
    nyt_sadness_tally = nyt_emotion_tables[5]
    nyt_anger_tally = nyt_emotion_tables[6]
    nyt_disgust_tally = nyt_emotion_tables[7]

    bbc_trust_tally = bbc_emotion_tables[0]
    bbc_joy_tally = bbc_emotion_tables[1]
    bbc_anticip_tally = bbc_emotion_tables[2]
    bbc_surprise_tally = bbc_emotion_tables[3]
    bbc_fear_tally = bbc_emotion_tables[4]
    bbc_sadness_tally = bbc_emotion_tables[5]
    bbc_anger_tally = bbc_emotion_tables[6]
    bbc_disgust_tally = bbc_emotion_tables[7]

    fn_trust_tally = fn_emotion_tables[0]
    fn_joy_tally = fn_emotion_tables[1]
    fn_anticip_tally = fn_emotion_tables[2]
    fn_surprise_tally = fn_emotion_tables[3]
    fn_fear_tally = fn_emotion_tables[4]
    fn_sadness_tally = fn_emotion_tables[5]
    fn_anger_tally = fn_emotion_tables[6]
    fn_disgust_tally = fn_emotion_tables[7]


    template = loader.get_template('custom_scraper/emotion_compare.html')

    context = {'fn_trust_tally':fn_trust_tally, 'fn_joy_tally':fn_joy_tally, 'fn_anticip_tally':fn_anticip_tally, 'fn_surprise_tally':fn_surprise_tally, 'fn_fear_tally': fn_fear_tally, 'fn_sadness_tally':fn_sadness_tally, 'fn_anger_tally':fn_anger_tally, 'fn_disgust_tally':fn_disgust_tally, 'nyt_trust_tally':nyt_trust_tally, 'nyt_joy_tally':nyt_joy_tally, 'nyt_anticip_tally':nyt_anticip_tally, 'nyt_surprise_tally':nyt_surprise_tally, 'nyt_fear_tally': nyt_fear_tally, 'nyt_sadness_tally':nyt_sadness_tally, 'nyt_anger_tally':nyt_anger_tally, 'nyt_disgust_tally':nyt_disgust_tally, 'bbc_trust_tally':bbc_trust_tally, 'bbc_joy_tally':bbc_joy_tally, 'bbc_anticip_tally':bbc_anticip_tally, 'bbc_surprise_tally':bbc_surprise_tally, 'bbc_fear_tally': bbc_fear_tally, 'bbc_sadness_tally':bbc_sadness_tally, 'bbc_anger_tally':bbc_anger_tally, 'bbc_disgust_tally':bbc_disgust_tally,'joy_formatted':joy_formatted, 'anticip_formatted':anticip_formatted, 'surprise_formatted':surprise_formatted, 'fear_formatted':fear_formatted, 'sadness_formatted':sadness_formatted, 'anger_formatted':anger_formatted, 'disgust_formatted':disgust_formatted, 'trust_formatted':trust_formatted,'joy_nyt_hls': joy_nyt_hls, 'joy_bbc_hls': joy_bbc_hls, 'joy_fn_hls': joy_fn_hls, 'trust_nyt_hls': trust_nyt_hls, 'trust_bbc_hls': trust_bbc_hls, 'trust_fn_hls': trust_fn_hls, 'anticip_nyt_hls': anticip_nyt_hls, 'anticip_bbc_hls': anticip_bbc_hls, 'anticip_fn_hls': anticip_fn_hls, 'surprise_nyt_hls': surprise_nyt_hls, 'surprise_bbc_hls': surprise_bbc_hls, 'surprise_fn_hls': surprise_fn_hls, 'fear_nyt_hls': fear_nyt_hls, 'fear_bbc_hls': fear_bbc_hls, 'fear_fn_hls': fear_fn_hls, 'sadness_nyt_hls': sadness_nyt_hls, 'sadness_bbc_hls': sadness_bbc_hls, 'sadness_fn_hls': sadness_fn_hls, 'anger_nyt_hls': anger_nyt_hls, 'anger_bbc_hls': anger_bbc_hls, 'anger_fn_hls': anger_fn_hls, 'disgust_nyt_hls': disgust_nyt_hls, 'disgust_bbc_hls': disgust_bbc_hls, 'disgust_fn_hls': disgust_fn_hls,'nyt_trust_list': nyt_trust_list, 'bbc_trust_list': bbc_trust_list, 'fn_trust_list': fn_trust_list, 'nyt_joy_list': nyt_joy_list, 'bbc_joy_list': bbc_joy_list, 'fn_joy_list': fn_joy_list, 'nyt_anticip_list': nyt_anticip_list, 'bbc_anticip_list': bbc_anticip_list, 'fn_anticip_list': fn_anticip_list, 'nyt_surprise_list': nyt_surprise_list, 'bbc_surprise_list': bbc_surprise_list, 'fn_surprise_list': fn_surprise_list, 'nyt_fear_list': nyt_fear_list, 'bbc_fear_list': bbc_fear_list, 'fn_fear_list': fn_fear_list, 'nyt_sadness_list': nyt_sadness_list, 'bbc_sadness_list': bbc_sadness_list, 'fn_sadness_list': fn_sadness_list, 'nyt_anger_list': nyt_anger_list, 'bbc_anger_list': bbc_anger_list, 'fn_anger_list': fn_anger_list, 'nyt_disgust_list': nyt_disgust_list, 'bbc_disgust_list': bbc_disgust_list, 'fn_disgust_list': fn_disgust_list, 'trust_daily_plot': trust_daily_plot, 'trust_monthly_plot': trust_monthly_plot, 'joy_daily_plot': joy_daily_plot, 'joy_monthly_plot': joy_monthly_plot, 'anticip_daily_plot': anticip_daily_plot, 'anticip_monthly_plot': anticip_monthly_plot, 'surprise_daily_plot': surprise_daily_plot, 'surprise_monthly_plot': surprise_monthly_plot, 'fear_daily_plot': fear_daily_plot, 'fear_monthly_plot': fear_monthly_plot, 'sadness_daily_plot': sadness_daily_plot, 'sadness_monthly_plot': sadness_monthly_plot, 'anger_daily_plot': anger_daily_plot, 'anger_monthly_plot': anger_monthly_plot, 'disgust_daily_plot': disgust_daily_plot, 'disgust_monthly_plot': disgust_monthly_plot,  'html_div_compare_emotions':html_div_compare_emotions,  'fn_trust_tally':fn_trust_tally, 'fn_joy_tally':fn_joy_tally, 'fn_anticip_tally':fn_anticip_tally, 'fn_surprise_tally':fn_surprise_tally, 'fn_fear_tally': fn_fear_tally, 'fn_sadness_tally':fn_sadness_tally, 'fn_anger_tally':fn_anger_tally, 'fn_disgust_tally':fn_disgust_tally, 'nyt_trust_tally':nyt_trust_tally, 'nyt_joy_tally':nyt_joy_tally, 'nyt_anticip_tally':nyt_anticip_tally, 'nyt_surprise_tally':nyt_surprise_tally, 'nyt_fear_tally': nyt_fear_tally, 'nyt_sadness_tally':nyt_sadness_tally, 'nyt_anger_tally':nyt_anger_tally, 'nyt_disgust_tally':nyt_disgust_tally, 'bbc_trust_tally':bbc_trust_tally, 'bbc_joy_tally':bbc_joy_tally, 'bbc_anticip_tally':bbc_anticip_tally, 'bbc_surprise_tally':bbc_surprise_tally, 'bbc_fear_tally': bbc_fear_tally, 'bbc_sadness_tally':bbc_sadness_tally, 'bbc_anger_tally':bbc_anger_tally, 'bbc_disgust_tally':bbc_disgust_tally, }
    cache_test = HttpResponse(template.render(context, request),)

    cache_test = cache_test.content.decode("utf-8")
    html_cache_save = html_cache(page_num=5, cache_html=cache_test)
    html_cache_save.save()


    return render(request, 'custom_scraper/emotion_compare.html',{'fn_trust_tally':fn_trust_tally, 'fn_joy_tally':fn_joy_tally, 'fn_anticip_tally':fn_anticip_tally, 'fn_surprise_tally':fn_surprise_tally, 'fn_fear_tally': fn_fear_tally, 'fn_sadness_tally':fn_sadness_tally, 'fn_anger_tally':fn_anger_tally, 'fn_disgust_tally':fn_disgust_tally, 'nyt_trust_tally':nyt_trust_tally, 'nyt_joy_tally':nyt_joy_tally, 'nyt_anticip_tally':nyt_anticip_tally, 'nyt_surprise_tally':nyt_surprise_tally, 'nyt_fear_tally': nyt_fear_tally, 'nyt_sadness_tally':nyt_sadness_tally, 'nyt_anger_tally':nyt_anger_tally, 'nyt_disgust_tally':nyt_disgust_tally, 'bbc_trust_tally':bbc_trust_tally, 'bbc_joy_tally':bbc_joy_tally, 'bbc_anticip_tally':bbc_anticip_tally, 'bbc_surprise_tally':bbc_surprise_tally, 'bbc_fear_tally': bbc_fear_tally, 'bbc_sadness_tally':bbc_sadness_tally, 'bbc_anger_tally':bbc_anger_tally, 'bbc_disgust_tally':bbc_disgust_tally,'joy_formatted':joy_formatted, 'anticip_formatted':anticip_formatted, 'surprise_formatted':surprise_formatted, 'fear_formatted':fear_formatted, 'sadness_formatted':sadness_formatted, 'anger_formatted':anger_formatted, 'disgust_formatted':disgust_formatted, 'trust_formatted':trust_formatted,'joy_nyt_hls': joy_nyt_hls, 'joy_bbc_hls': joy_bbc_hls, 'joy_fn_hls': joy_fn_hls, 'trust_nyt_hls': trust_nyt_hls, 'trust_bbc_hls': trust_bbc_hls, 'trust_fn_hls': trust_fn_hls, 'anticip_nyt_hls': anticip_nyt_hls, 'anticip_bbc_hls': anticip_bbc_hls, 'anticip_fn_hls': anticip_fn_hls, 'surprise_nyt_hls': surprise_nyt_hls, 'surprise_bbc_hls': surprise_bbc_hls, 'surprise_fn_hls': surprise_fn_hls, 'fear_nyt_hls': fear_nyt_hls, 'fear_bbc_hls': fear_bbc_hls, 'fear_fn_hls': fear_fn_hls, 'sadness_nyt_hls': sadness_nyt_hls, 'sadness_bbc_hls': sadness_bbc_hls, 'sadness_fn_hls': sadness_fn_hls, 'anger_nyt_hls': anger_nyt_hls, 'anger_bbc_hls': anger_bbc_hls, 'anger_fn_hls': anger_fn_hls, 'disgust_nyt_hls': disgust_nyt_hls, 'disgust_bbc_hls': disgust_bbc_hls, 'disgust_fn_hls': disgust_fn_hls,'nyt_trust_list': nyt_trust_list, 'bbc_trust_list': bbc_trust_list, 'fn_trust_list': fn_trust_list, 'nyt_joy_list': nyt_joy_list, 'bbc_joy_list': bbc_joy_list, 'fn_joy_list': fn_joy_list, 'nyt_anticip_list': nyt_anticip_list, 'bbc_anticip_list': bbc_anticip_list, 'fn_anticip_list': fn_anticip_list, 'nyt_surprise_list': nyt_surprise_list, 'bbc_surprise_list': bbc_surprise_list, 'fn_surprise_list': fn_surprise_list, 'nyt_fear_list': nyt_fear_list, 'bbc_fear_list': bbc_fear_list, 'fn_fear_list': fn_fear_list, 'nyt_sadness_list': nyt_sadness_list, 'bbc_sadness_list': bbc_sadness_list, 'fn_sadness_list': fn_sadness_list, 'nyt_anger_list': nyt_anger_list, 'bbc_anger_list': bbc_anger_list, 'fn_anger_list': fn_anger_list, 'nyt_disgust_list': nyt_disgust_list, 'bbc_disgust_list': bbc_disgust_list, 'fn_disgust_list': fn_disgust_list, 'trust_daily_plot': trust_daily_plot, 'trust_monthly_plot': trust_monthly_plot, 'joy_daily_plot': joy_daily_plot, 'joy_monthly_plot': joy_monthly_plot, 'anticip_daily_plot': anticip_daily_plot, 'anticip_monthly_plot': anticip_monthly_plot, 'surprise_daily_plot': surprise_daily_plot, 'surprise_monthly_plot': surprise_monthly_plot, 'fear_daily_plot': fear_daily_plot, 'fear_monthly_plot': fear_monthly_plot, 'sadness_daily_plot': sadness_daily_plot, 'sadness_monthly_plot': sadness_monthly_plot, 'anger_daily_plot': anger_daily_plot, 'anger_monthly_plot': anger_monthly_plot, 'disgust_daily_plot': disgust_daily_plot, 'disgust_monthly_plot': disgust_monthly_plot,  'html_div_compare_emotions':html_div_compare_emotions,  'fn_trust_tally':fn_trust_tally, 'fn_joy_tally':fn_joy_tally, 'fn_anticip_tally':fn_anticip_tally, 'fn_surprise_tally':fn_surprise_tally, 'fn_fear_tally': fn_fear_tally, 'fn_sadness_tally':fn_sadness_tally, 'fn_anger_tally':fn_anger_tally, 'fn_disgust_tally':fn_disgust_tally, 'nyt_trust_tally':nyt_trust_tally, 'nyt_joy_tally':nyt_joy_tally, 'nyt_anticip_tally':nyt_anticip_tally, 'nyt_surprise_tally':nyt_surprise_tally, 'nyt_fear_tally': nyt_fear_tally, 'nyt_sadness_tally':nyt_sadness_tally, 'nyt_anger_tally':nyt_anger_tally, 'nyt_disgust_tally':nyt_disgust_tally, 'bbc_trust_tally':bbc_trust_tally, 'bbc_joy_tally':bbc_joy_tally, 'bbc_anticip_tally':bbc_anticip_tally, 'bbc_surprise_tally':bbc_surprise_tally, 'bbc_fear_tally': bbc_fear_tally, 'bbc_sadness_tally':bbc_sadness_tally, 'bbc_anger_tally':bbc_anger_tally, 'bbc_disgust_tally':bbc_disgust_tally, })



def emotion_search_compare(request):
    form1 = CompareSearch1()


    form2 = CompareSearch2()


    import plotly.graph_objects as go

    from datetime import datetime

    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today = str(today)[:10]
    yesterday = str(yesterday)[:10]



    if not Headline.objects.filter(date__contains=today).values('headline'):
        today = yesterday


    top_10_words_terms = word_count_general.objects.filter(newspaper=4).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:9]
    test_terms = []
    test_overall_values_list = []
    for i in top_10_words_terms:
        test_terms.append(i['word'])
        test_overall_values_list.append(i['word_count'])



    test_values_list = []

    for i in range(1,4):
        newspaper_values = []
        for y in test_terms:
            all_test_values = word_count_general.objects.filter(date__contains=today).filter(newspaper=i).filter(word=y).values('word_count')
            for record in all_test_values:
                newspaper_values.append(record['word_count'])
        test_values_list.append(newspaper_values)






    test_ny_values_list = test_values_list[0]
    test_bbc_values_list = test_values_list[1]
    test_fn_values_list = test_values_list[2]




    values_fig = go.Figure(data=[
        go.Bar(name='New York Times', y=test_terms, x=test_ny_values_list, orientation='h', marker_color="#2d2e30"),
        go.Bar(name='BBC News', y=test_terms, x=test_bbc_values_list, orientation = 'h', marker_color="#bb1919"),
        go.Bar(name='Fox News', y=test_terms, x=test_fn_values_list, orientation = 'h', marker_color="rgba(0,51,102,.99)"),
    ], )
    values_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), height=400, plot_bgcolor='white', orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))


    return render(request, 'custom_scraper/emotion_search_compare.html',{'form1':form1, 'form2':form2, 'html_div_values': html_div_values,  } )



def emotion_search_compare_result(request):
    form1 = CompareSearch1()


    form2 = CompareSearch2()

    search1 = request.GET.get('compare1')


    search2 = request.GET.get('compare2')


    key1data = Headline.objects.filter(headline__icontains=search1)
    key2data = Headline.objects.filter(headline__icontains=search2)

    from django.shortcuts import redirect
    if not key1data or len(key1data) < 3 or not key2data or len(key2data) < 3:
        request.session['search1'] = search1
        request.session['search2'] = search2



        return redirect('research_emotion_compare')


    from django.db.models import Count


    def get_search_term_emotion_dict_list(search_word):

        search = search_word.lower()
        emotion_dict_list = []
        emotion_dict_list_overall = []
        #for each newspaper (1,2,3)
        hlcount_nyt = Headline_emotion.objects.filter(newspaper=1).filter(day_order__lte=25).filter(headline__icontains=search).values('id').count()
        hlcount_bbc = Headline_emotion.objects.filter(newspaper=2).filter(day_order__lte=25).filter(headline__icontains=search).values('id').count()
        hlcount_fn = Headline_emotion.objects.filter(newspaper=3).filter(day_order__lte=25).filter(headline__icontains=search).values('id').count()

        searchword_headline_emotion_by_newspaper_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(fear__gt=0).values('newspaper').annotate(Count=Count('id'))

        for record in searchword_headline_emotion_by_newspaper_fear:

            emotion_dict = {}
            emotion_dict_overall = {}
            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc

            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Fear'




            emotion_dict_list.append(emotion_dict)





        searchword_headline_emotion_by_newspaper_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(anger__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_anger:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt

            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc

            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Anger'


            emotion_dict_list.append(emotion_dict)



        searchword_headline_emotion_by_newspaper_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(anticip__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_anticip:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Anticipation'


            emotion_dict_list.append(emotion_dict)



        searchword_headline_emotion_by_newspaper_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(trust__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_trust:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Trust'


            emotion_dict_list.append(emotion_dict)




        searchword_headline_emotion_by_newspaper_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(surprise__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_surprise:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Surprise'


            emotion_dict_list.append(emotion_dict)


        searchword_headline_emotion_by_newspaper_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(sadness__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_sadness:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Sadness'


            emotion_dict_list.append(emotion_dict)


        searchword_headline_emotion_by_newspaper_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(disgust__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_disgust:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Disgust'


            emotion_dict_list.append(emotion_dict)





        searchword_headline_emotion_by_newspaper_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(joy__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_joy:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Joy'


            emotion_dict_list.append(emotion_dict)



        return emotion_dict_list


    search1_data = get_search_term_emotion_dict_list(search1)
    search2_data = get_search_term_emotion_dict_list(search2)



    for emotion_dict in search2_data:
        search1_data.append(emotion_dict)



    nyt_search1_data = []
    bbc_search1_data = []
    fn_search1_data = []

    for record in search1_data:
        if record['Search Term'] == 'The New York Times - ' + str(search1.lower()) or record['Search Term'] == 'The New York Times - ' + str(search2.lower()):
            nyt_search1_data.append(record)
        elif record['Search Term'] == 'BBC News - ' + str(search1.lower()) or record['Search Term'] == 'BBC News - ' + str(search2.lower()):
            bbc_search1_data.append(record)
        elif record['Search Term'] == 'Fox News - ' + str(search1.lower()) or record['Search Term'] == 'Fox News - ' + str(search2.lower()):
            fn_search1_data.append(record)

    comparesent_month_nyt = pd.DataFrame(nyt_search1_data)
    comparesent_month_bbc = pd.DataFrame(bbc_search1_data)
    comparesent_month_fn = pd.DataFrame(fn_search1_data)




    figcompare_month_pos_nyt = px.line(comparesent_month_nyt, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos_nyt.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions_nyt = str(plotly.offline.plot(figcompare_month_pos_nyt, output_type='div', config = {'displayModeBar': False}))



    figcompare_month_pos_bbc = px.line(comparesent_month_bbc, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos_bbc.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions_bbc = str(plotly.offline.plot(figcompare_month_pos_bbc, output_type='div', config = {'displayModeBar': False}))


    figcompare_month_pos_fn = px.line(comparesent_month_fn, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos_fn.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions_fn = str(plotly.offline.plot(figcompare_month_pos_fn, output_type='div', config = {'displayModeBar': False}))
















    comparesent_month = pd.DataFrame(search1_data)












    figcompare_month_pos = px.line(comparesent_month, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions = str(plotly.offline.plot(figcompare_month_pos, output_type='div', config = {'displayModeBar': False}))

    #get overall data for overall tab
    search_dict_list = []

    search1_total_hls = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).values('id').count()

    search2_total_hls = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search2).values('id').count()

    search1_dict_fear = {}
    searchword_headline_emotion_by_newspaper_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(fear__gt=0).values('id').count()
    search1_dict_fear['Search Term'] = str(search1.lower())
    search1_dict_fear['Emotion'] = 'Fear'
    search1_dict_fear['Count'] = searchword_headline_emotion_by_newspaper_fear/search1_total_hls
    search_dict_list.append(search1_dict_fear)


    search1_dict_trust = {}
    searchword_headline_emotion_by_newspaper_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(trust__gt=0).values('id').count()
    search1_dict_trust['Search Term'] = str(search1.lower())
    search1_dict_trust['Emotion'] = 'Trust'
    search1_dict_trust['Count'] = searchword_headline_emotion_by_newspaper_trust/search1_total_hls
    search_dict_list.append(search1_dict_trust)

    search1_dict_joy = {}
    searchword_headline_emotion_by_newspaper_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(joy__gt=0).values('id').count()
    search1_dict_joy['Search Term'] = str(search1.lower())
    search1_dict_joy['Emotion'] = 'Joy'
    search1_dict_joy['Count'] = searchword_headline_emotion_by_newspaper_joy/search1_total_hls
    search_dict_list.append(search1_dict_joy)

    search1_dict_anticip = {}
    searchword_headline_emotion_by_newspaper_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(anticip__gt=0).values('id').count()
    search1_dict_anticip['Search Term'] = str(search1.lower())
    search1_dict_anticip['Emotion'] = 'Anticipation'
    search1_dict_anticip['Count'] = searchword_headline_emotion_by_newspaper_anticip/search1_total_hls
    search_dict_list.append(search1_dict_anticip)

    search1_dict_surprise = {}
    searchword_headline_emotion_by_newspaper_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(surprise__gt=0).values('id').count()
    search1_dict_surprise['Search Term'] = str(search1.lower())
    search1_dict_surprise['Emotion'] = 'Surprise'
    search1_dict_surprise['Count'] = searchword_headline_emotion_by_newspaper_surprise/search1_total_hls
    search_dict_list.append(search1_dict_surprise)

    search1_dict_sadness = {}
    searchword_headline_emotion_by_newspaper_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(sadness__gt=0).values('id').count()
    search1_dict_sadness['Search Term'] = str(search1.lower())
    search1_dict_sadness['Emotion'] = 'Sadness'
    search1_dict_sadness['Count'] = searchword_headline_emotion_by_newspaper_sadness/search1_total_hls
    search_dict_list.append(search1_dict_sadness)

    search1_dict_anger = {}
    searchword_headline_emotion_by_newspaper_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(anger__gt=0).values('id').count()
    search1_dict_anger['Search Term'] = str(search1.lower())
    search1_dict_anger['Emotion'] = 'Anger'
    search1_dict_anger['Count'] = searchword_headline_emotion_by_newspaper_anger/search1_total_hls
    search_dict_list.append(search1_dict_anger)

    search1_dict_disgust = {}
    searchword_headline_emotion_by_newspaper_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(disgust__gt=0).values('id').count()
    search1_dict_disgust['Search Term'] = str(search1.lower())
    search1_dict_disgust['Emotion'] = 'Disgust'
    search1_dict_disgust['Count'] = searchword_headline_emotion_by_newspaper_disgust/search1_total_hls
    search_dict_list.append(search1_dict_disgust)

    search2_dict_fear = {}
    searchword_headline_emotion_by_newspaper_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(fear__gt=0).values('id').count()
    search2_dict_fear['Search Term'] = str(search2.lower())
    search2_dict_fear['Emotion'] = 'Fear'
    search2_dict_fear['Count'] = searchword_headline_emotion_by_newspaper_fear/search2_total_hls
    search_dict_list.append(search2_dict_fear)


    search2_dict_trust = {}
    searchword_headline_emotion_by_newspaper_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(trust__gt=0).values('id').count()
    search2_dict_trust['Search Term'] = str(search2.lower())
    search2_dict_trust['Emotion'] = 'Trust'
    search2_dict_trust['Count'] = searchword_headline_emotion_by_newspaper_trust/search2_total_hls
    search_dict_list.append(search2_dict_trust)

    search2_dict_joy = {}
    searchword_headline_emotion_by_newspaper_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(joy__gt=0).values('id').count()
    search2_dict_joy['Search Term'] = str(search2.lower())
    search2_dict_joy['Emotion'] = 'Joy'
    search2_dict_joy['Count'] = searchword_headline_emotion_by_newspaper_joy/search2_total_hls
    search_dict_list.append(search2_dict_joy)

    search2_dict_anticip = {}
    searchword_headline_emotion_by_newspaper_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(anticip__gt=0).values('id').count()
    search2_dict_anticip['Search Term'] = str(search2.lower())
    search2_dict_anticip['Emotion'] = 'Anticipation'
    search2_dict_anticip['Count'] = searchword_headline_emotion_by_newspaper_anticip/search2_total_hls
    search_dict_list.append(search2_dict_anticip)

    search2_dict_surprise = {}
    searchword_headline_emotion_by_newspaper_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(surprise__gt=0).values('id').count()
    search2_dict_surprise['Search Term'] = str(search2.lower())
    search2_dict_surprise['Emotion'] = 'Surprise'
    search2_dict_surprise['Count'] = searchword_headline_emotion_by_newspaper_surprise/search2_total_hls
    search_dict_list.append(search2_dict_surprise)

    search2_dict_sadness = {}
    searchword_headline_emotion_by_newspaper_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(sadness__gt=0).values('id').count()
    search2_dict_sadness['Search Term'] = str(search2.lower())
    search2_dict_sadness['Emotion'] = 'Sadness'
    search2_dict_sadness['Count'] = searchword_headline_emotion_by_newspaper_sadness/search2_total_hls
    search_dict_list.append(search2_dict_sadness)

    search2_dict_anger = {}
    searchword_headline_emotion_by_newspaper_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(anger__gt=0).values('id').count()
    search2_dict_anger['Search Term'] = str(search2.lower())
    search2_dict_anger['Emotion'] = 'Anger'
    search2_dict_anger['Count'] = searchword_headline_emotion_by_newspaper_anger/search2_total_hls
    search_dict_list.append(search2_dict_anger)

    search2_dict_disgust = {}
    searchword_headline_emotion_by_newspaper_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search2).filter(disgust__gt=0).values('id').count()
    search2_dict_disgust['Search Term'] = str(search2.lower())
    search2_dict_disgust['Emotion'] = 'Disgust'
    search2_dict_disgust['Count'] = searchword_headline_emotion_by_newspaper_disgust/search2_total_hls
    search_dict_list.append(search2_dict_disgust)

    comparesent_month_overall = pd.DataFrame(search_dict_list)












    figcompare_month_pos_overall = px.line(comparesent_month_overall, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos_overall.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions_overall = str(plotly.offline.plot(figcompare_month_pos_overall, output_type='div', config = {'displayModeBar': False}))


    def get_monthly_query_data_search_term(search_term1, search_term2):
        searched1 = search_term1.lower()
        searched2 = search_term2.lower()
        query_monthly_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(fear__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Fear", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(anger__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Anger", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(anticip__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Anticipation", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(trust__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Trust", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(surprise__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Surprise", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(sadness__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Sadness", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(disgust__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Disgust", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(joy__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Joy", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_fear2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(fear__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Fear", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anger2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(anger__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Anger", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anticip2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(anticip__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Anticipation", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_trust2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(trust__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Trust", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_surprise2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(surprise__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Surprise", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_sadness2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(sadness__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Sadness", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_disgust2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(disgust__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Disgust", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_joy2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(joy__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Joy", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))

        querylist = [query_monthly_fear, query_monthly_anger, query_monthly_anticip, query_monthly_trust, query_monthly_surprise, query_monthly_sadness, query_monthly_disgust, query_monthly_joy, query_monthly_fear2, query_monthly_anger2, query_monthly_anticip2, query_monthly_trust2, query_monthly_surprise2, query_monthly_sadness2, query_monthly_disgust2, query_monthly_joy2]

        nyt_query_data = []
        bbc_query_data = []
        fn_query_data = []
        overall_query_data = []

        for query in querylist:
            for record in query:
                if record['newspaper'] == 1:
                    nyt_query_data.append(record)
                    overall_query_data.append(record)
                elif record['newspaper'] == 2:
                    bbc_query_data.append(record)
                    overall_query_data.append(record)
                elif record['newspaper'] == 3:
                    fn_query_data.append(record)
                    overall_query_data.append(record)




        return overall_query_data, nyt_query_data, bbc_query_data, fn_query_data




    def sort_query_data_by_emotion(emotion_query):

        fear_data = []
        anger_data = []
        anticip_data = []
        trust_data = []
        surprise_data = []
        sadness_data = []
        disgust_data = []
        joy_data = []



        for record in emotion_query:
            if record['mycolumn'] == 'Fear':
                fear_data.append(record)
            elif record['mycolumn'] == 'Anger':
                anger_data.append(record)
            elif record['mycolumn'] == 'Anticipation':
                anticip_data.append(record)
            elif record['mycolumn'] == 'Trust':
                trust_data.append(record)
            elif record['mycolumn'] == 'Surprise':
                surprise_data.append(record)
            elif record['mycolumn'] == 'Sadness':
                sadness_data.append(record)
            elif record['mycolumn'] == 'Disgust':
                disgust_data.append(record)
            elif record['mycolumn'] == 'Joy':
                joy_data.append(record)

        return fear_data, anger_data, anticip_data, trust_data, surprise_data, sadness_data, disgust_data, joy_data

    all_data = get_monthly_query_data_search_term(search1,search2)

    overall_tab_data = all_data[0]

    overall_data = sort_query_data_by_emotion(all_data[0])

    nyt_data = sort_query_data_by_emotion(all_data[1])
    bbc_data = sort_query_data_by_emotion(all_data[2])
    fn_data = sort_query_data_by_emotion(all_data[3])

    def get_plot_by_emotion(data_set):
        output_list = []
        for data in data_set:
            comparesent = pd.DataFrame(list(data))

            comparesent.rename(columns={'search_term':'Search Term'}, inplace= True)


            figcompare = px.line(comparesent, x="Date", y="Count", color="Search Term",   )


            figcompare.update_layout(
                font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




            html_div_compare = str(plotly.offline.plot(figcompare, output_type='div', config = {'displayModeBar': False}))
            output_list.append(html_div_compare)


        return output_list



    nyt_fear_search_date_div = get_plot_by_emotion(nyt_data)[0]
    nyt_anger_search_date_div = get_plot_by_emotion(nyt_data)[1]
    nyt_anticip_search_date_div = get_plot_by_emotion(nyt_data)[2]
    nyt_trust_search_date_div = get_plot_by_emotion(nyt_data)[3]
    nyt_surprise_search_date_div = get_plot_by_emotion(nyt_data)[4]
    nyt_sadness_search_date_div = get_plot_by_emotion(nyt_data)[5]
    nyt_disgust_search_date_div = get_plot_by_emotion(nyt_data)[6]
    nyt_joy_search_date_div = get_plot_by_emotion(nyt_data)[7]

    bbc_fear_search_date_div = get_plot_by_emotion(bbc_data)[0]
    bbc_anger_search_date_div = get_plot_by_emotion(bbc_data)[1]
    bbc_anticip_search_date_div = get_plot_by_emotion(bbc_data)[2]
    bbc_trust_search_date_div = get_plot_by_emotion(bbc_data)[3]
    bbc_surprise_search_date_div = get_plot_by_emotion(bbc_data)[4]
    bbc_sadness_search_date_div = get_plot_by_emotion(bbc_data)[5]
    bbc_disgust_search_date_div = get_plot_by_emotion(bbc_data)[6]
    bbc_joy_search_date_div = get_plot_by_emotion(bbc_data)[7]

    fn_fear_search_date_div = get_plot_by_emotion(fn_data)[0]
    fn_anger_search_date_div = get_plot_by_emotion(fn_data)[1]
    fn_anticip_search_date_div = get_plot_by_emotion(fn_data)[2]
    fn_trust_search_date_div = get_plot_by_emotion(fn_data)[3]
    fn_surprise_search_date_div = get_plot_by_emotion(fn_data)[4]
    fn_sadness_search_date_div = get_plot_by_emotion(fn_data)[5]
    fn_disgust_search_date_div = get_plot_by_emotion(fn_data)[6]
    fn_joy_search_date_div = get_plot_by_emotion(fn_data)[7]


    #below is Compare tab code

    for emotion in overall_data:
        for record in emotion:
            if record['newspaper'] == 1 and record['search_term'] == str(search1.lower()):
                record['search_term'] = 'The New York Times - ' + str(search1.lower())
            elif record['newspaper'] == 2 and record['search_term'] == str(search1.lower()):
                record['search_term'] = 'BBC News - ' + str(search1.lower())
            elif record['newspaper'] == 3 and record['search_term'] == str(search1.lower()):
                record['search_term'] = 'Fox News - ' + str(search1.lower())

            elif record['newspaper'] == 1 and record['search_term'] == str(search2.lower()):
                record['search_term'] = 'The New York Times - ' + str(search2.lower())
            elif record['newspaper'] == 2 and record['search_term'] == str(search2.lower()):
                record['search_term'] = 'BBC News - ' + str(search2.lower())
            elif record['newspaper'] == 3 and record['search_term'] == str(search2.lower()):
                record['search_term'] = 'Fox News - ' + str(search2.lower())



    compare_fear_search_date_div = get_plot_by_emotion(overall_data)[0]
    compare_anger_search_date_div = get_plot_by_emotion(overall_data)[1]
    compare_anticip_search_date_div = get_plot_by_emotion(overall_data)[2]
    compare_trust_search_date_div = get_plot_by_emotion(overall_data)[3]
    compare_surprise_search_date_div = get_plot_by_emotion(overall_data)[4]
    compare_sadness_search_date_div = get_plot_by_emotion(overall_data)[5]
    compare_disgust_search_date_div = get_plot_by_emotion(overall_data)[6]
    compare_joy_search_date_div = get_plot_by_emotion(overall_data)[7]


    def get_monthly_query_data_search_term_overall(search_term1, search_term2):
        searched1 = search_term1.lower()
        searched2 = search_term2.lower()
        query_monthly_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(fear__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Fear", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(anger__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Anger", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(anticip__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Anticipation", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(trust__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Trust", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(surprise__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Surprise", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(sadness__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Sadness", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(disgust__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Disgust", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(joy__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Joy", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_fear2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(fear__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Fear", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anger2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(anger__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Anger", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anticip2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(anticip__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Anticipation", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_trust2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(trust__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Trust", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_surprise2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(surprise__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Surprise", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_sadness2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(sadness__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Sadness", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_disgust2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(disgust__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Disgust", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_joy2 = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched2).filter(joy__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Joy", output_field=CharField())).annotate(search_term=Value(str(searched2), output_field=CharField())).annotate(Count=Count("id"))



        querylist = [query_monthly_fear, query_monthly_anger, query_monthly_anticip, query_monthly_trust, query_monthly_surprise, query_monthly_sadness, query_monthly_disgust, query_monthly_joy, query_monthly_fear2, query_monthly_anger2, query_monthly_anticip2, query_monthly_trust2, query_monthly_surprise2, query_monthly_sadness2, query_monthly_disgust2, query_monthly_joy2]


        overall_query_data = []


        for query in querylist:
            for record in query:

                    overall_query_data.append(record)




        return overall_query_data



    overall_search_data_sort = sort_query_data_by_emotion(get_monthly_query_data_search_term_overall(search1,search2))









    overall_search_fear_search_date_div = get_plot_by_emotion(overall_search_data_sort)[0]
    overall_search_anger_search_date_div = get_plot_by_emotion(overall_search_data_sort)[1]
    overall_search_anticip_search_date_div = get_plot_by_emotion(overall_search_data_sort)[2]
    overall_search_trust_search_date_div = get_plot_by_emotion(overall_search_data_sort)[3]
    overall_search_surprise_search_date_div = get_plot_by_emotion(overall_search_data_sort)[4]
    overall_search_sadness_search_date_div = get_plot_by_emotion(overall_search_data_sort)[5]
    overall_search_disgust_search_date_div = get_plot_by_emotion(overall_search_data_sort)[6]
    overall_search_joy_search_date_div = get_plot_by_emotion(overall_search_data_sort)[7]


    return render(request, 'custom_scraper/emotion_search_compare_result.html',{'form1':form1, 'search1':search1, 'search2':search2, 'html_div_compare_emotions': html_div_compare_emotions, 'html_div_compare_emotions_overall': html_div_compare_emotions_overall, 'html_div_compare_emotions_nyt': html_div_compare_emotions_nyt, 'html_div_compare_emotions_bbc': html_div_compare_emotions_bbc, 'html_div_compare_emotions_fn': html_div_compare_emotions_fn, 'compare_fear_search_date_div': compare_fear_search_date_div, 'compare_anger_search_date_div': compare_anger_search_date_div, 'compare_anticip_search_date_div': compare_anticip_search_date_div, 'compare_trust_search_date_div': compare_trust_search_date_div, 'compare_surprise_search_date_div': compare_surprise_search_date_div, 'compare_joy_search_date_div': compare_joy_search_date_div, 'compare_sadness_search_date_div': compare_sadness_search_date_div, 'compare_disgust_search_date_div': compare_disgust_search_date_div, 'compare_fear_search_date_div': compare_fear_search_date_div, 'nyt_anger_search_date_div': nyt_anger_search_date_div, 'nyt_anticip_search_date_div': nyt_anticip_search_date_div, 'nyt_trust_search_date_div': nyt_trust_search_date_div, 'nyt_surprise_search_date_div': nyt_surprise_search_date_div, 'nyt_joy_search_date_div': nyt_joy_search_date_div, 'nyt_sadness_search_date_div': nyt_sadness_search_date_div, 'nyt_disgust_search_date_div': nyt_disgust_search_date_div, 'nyt_fear_search_date_div': nyt_fear_search_date_div, 'overall_search_fear_search_date_div': overall_search_fear_search_date_div, 'overall_search_anger_search_date_div': overall_search_anger_search_date_div, 'overall_search_anticip_search_date_div': overall_search_anticip_search_date_div, 'overall_search_trust_search_date_div': overall_search_trust_search_date_div, 'overall_search_surprise_search_date_div': overall_search_surprise_search_date_div, 'overall_search_joy_search_date_div': overall_search_joy_search_date_div, 'overall_search_sadness_search_date_div': overall_search_sadness_search_date_div, 'overall_search_disgust_search_date_div': overall_search_disgust_search_date_div, 'overall_search_fear_search_date_div': overall_search_fear_search_date_div,'bbc_anger_search_date_div': bbc_anger_search_date_div, 'bbc_anticip_search_date_div': bbc_anticip_search_date_div, 'bbc_trust_search_date_div': bbc_trust_search_date_div, 'bbc_surprise_search_date_div': bbc_surprise_search_date_div, 'bbc_joy_search_date_div': bbc_joy_search_date_div, 'bbc_sadness_search_date_div': bbc_sadness_search_date_div, 'bbc_disgust_search_date_div': bbc_disgust_search_date_div, 'bbc_fear_search_date_div': bbc_fear_search_date_div, 'fn_anger_search_date_div': fn_anger_search_date_div, 'fn_anticip_search_date_div': fn_anticip_search_date_div, 'fn_trust_search_date_div': fn_trust_search_date_div, 'fn_surprise_search_date_div': fn_surprise_search_date_div, 'fn_joy_search_date_div': fn_joy_search_date_div, 'fn_sadness_search_date_div': fn_sadness_search_date_div, 'fn_disgust_search_date_div': fn_disgust_search_date_div, 'fn_fear_search_date_div': fn_fear_search_date_div, } )



def emotion_search_compare_result_single(request):
    form1 = CompareSearchSingle()



    form2 = CompareSearch2()

    search1 = request.GET.get('compare1')


    search2 = "This is filler to get the two search to work for one search"


    key1data = Headline.objects.filter(headline__icontains=search1)

    from django.shortcuts import redirect
    if not key1data or len(key1data) < 3:
        request.session['search1'] = search1




        return redirect('research_emotion_compare_single')


    from django.db.models import Count


    def get_search_term_emotion_dict_list(search_word):

        search = search_word.lower()
        emotion_dict_list = []
        emotion_dict_list_overall = []
        #for each newspaper (1,2,3)
        hlcount_nyt = Headline_emotion.objects.filter(newspaper=1).filter(day_order__lte=25).filter(headline__icontains=search).values('id').count()
        hlcount_bbc = Headline_emotion.objects.filter(newspaper=2).filter(day_order__lte=25).filter(headline__icontains=search).values('id').count()
        hlcount_fn = Headline_emotion.objects.filter(newspaper=3).filter(day_order__lte=25).filter(headline__icontains=search).values('id').count()

        searchword_headline_emotion_by_newspaper_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(fear__gt=0).values('newspaper').annotate(Count=Count('id'))

        for record in searchword_headline_emotion_by_newspaper_fear:

            emotion_dict = {}
            emotion_dict_overall = {}
            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc

            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Fear'




            emotion_dict_list.append(emotion_dict)





        searchword_headline_emotion_by_newspaper_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(anger__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_anger:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt

            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc

            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Anger'


            emotion_dict_list.append(emotion_dict)



        searchword_headline_emotion_by_newspaper_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(anticip__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_anticip:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Anticipation'


            emotion_dict_list.append(emotion_dict)



        searchword_headline_emotion_by_newspaper_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(trust__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_trust:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Trust'


            emotion_dict_list.append(emotion_dict)




        searchword_headline_emotion_by_newspaper_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(surprise__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_surprise:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Surprise'


            emotion_dict_list.append(emotion_dict)


        searchword_headline_emotion_by_newspaper_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(sadness__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_sadness:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Sadness'


            emotion_dict_list.append(emotion_dict)


        searchword_headline_emotion_by_newspaper_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(disgust__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_disgust:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Disgust'


            emotion_dict_list.append(emotion_dict)





        searchword_headline_emotion_by_newspaper_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search).filter(joy__gt=0).values('newspaper').annotate(Count=Count('id'))
        for record in searchword_headline_emotion_by_newspaper_joy:

            emotion_dict = {}
            emotion_dict_overall = {}

            if record['newspaper'] == 1:
                emotion_dict['Search Term'] = 'The New York Times - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_nyt
            elif record['newspaper'] == 2:
                emotion_dict['Search Term'] = 'BBC News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_bbc
            elif record['newspaper'] == 3:
                emotion_dict['Search Term'] = 'Fox News - ' + str(search)
                emotion_dict['Count'] = record['Count']/hlcount_fn

            emotion_dict['Emotion'] = 'Joy'


            emotion_dict_list.append(emotion_dict)



        return emotion_dict_list


    search1_data = get_search_term_emotion_dict_list(search1)






    nyt_search1_data = []
    bbc_search1_data = []
    fn_search1_data = []

    for record in search1_data:
        if record['Search Term'] == 'The New York Times - ' + str(search1.lower()) or record['Search Term'] == 'The New York Times - ' + str(search2.lower()):
            nyt_search1_data.append(record)
        elif record['Search Term'] == 'BBC News - ' + str(search1.lower()) or record['Search Term'] == 'BBC News - ' + str(search2.lower()):
            bbc_search1_data.append(record)
        elif record['Search Term'] == 'Fox News - ' + str(search1.lower()) or record['Search Term'] == 'Fox News - ' + str(search2.lower()):
            fn_search1_data.append(record)


    if len(bbc_search1_data) < 1:
        bbc_search1_data = [{'Count': 0, 'Emotion': 'None','Search Term': search1}]

    if len(nyt_search1_data) < 1:
        nyt_search1_data = [{'Count': 0,'Emotion': 'None','Search Term': search1}]

    if len(fn_search1_data) < 1:
        fn_search1_data = [{'Count': 0,'Emotion': 'None','Search Term': search1}]

    """
    if len(bbc_search2_data) < 1:
        bbc_search2_data = [{'Count': 0, 'Emotion': 'None','Search Term': search2}]

    if len(nyt_search2_data) < 1:
        nyt_search2_data = [{'Count': 0,'Emotion': 'None','Search Term': search2}]

    if len(fn_search2_data) < 1:
        fn_search2_data = [{'Count': 0,'Emotion': 'None','Search Term': search2}]
    """
    comparesent_month_nyt = pd.DataFrame(nyt_search1_data)
    comparesent_month_bbc = pd.DataFrame(bbc_search1_data)
    comparesent_month_fn = pd.DataFrame(fn_search1_data)




    figcompare_month_pos_nyt = px.line(comparesent_month_nyt, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos_nyt.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions_nyt = str(plotly.offline.plot(figcompare_month_pos_nyt, output_type='div', config = {'displayModeBar': False}))



    figcompare_month_pos_bbc = px.line(comparesent_month_bbc, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos_bbc.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions_bbc = str(plotly.offline.plot(figcompare_month_pos_bbc, output_type='div', config = {'displayModeBar': False}))


    figcompare_month_pos_fn = px.line(comparesent_month_fn, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos_fn.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions_fn = str(plotly.offline.plot(figcompare_month_pos_fn, output_type='div', config = {'displayModeBar': False}))
















    comparesent_month = pd.DataFrame(search1_data)












    figcompare_month_pos = px.line(comparesent_month, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions = str(plotly.offline.plot(figcompare_month_pos, output_type='div', config = {'displayModeBar': False}))

    #get overall data for overall tab
    search_dict_list = []

    search1_total_hls = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).values('id').count()



    search1_dict_fear = {}
    searchword_headline_emotion_by_newspaper_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(fear__gt=0).values('id').count()
    search1_dict_fear['Search Term'] = str(search1.lower())
    search1_dict_fear['Emotion'] = 'Fear'
    search1_dict_fear['Count'] = searchword_headline_emotion_by_newspaper_fear/search1_total_hls
    search_dict_list.append(search1_dict_fear)


    search1_dict_trust = {}
    searchword_headline_emotion_by_newspaper_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(trust__gt=0).values('id').count()
    search1_dict_trust['Search Term'] = str(search1.lower())
    search1_dict_trust['Emotion'] = 'Trust'
    search1_dict_trust['Count'] = searchword_headline_emotion_by_newspaper_trust/search1_total_hls
    search_dict_list.append(search1_dict_trust)

    search1_dict_joy = {}
    searchword_headline_emotion_by_newspaper_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(joy__gt=0).values('id').count()
    search1_dict_joy['Search Term'] = str(search1.lower())
    search1_dict_joy['Emotion'] = 'Joy'
    search1_dict_joy['Count'] = searchword_headline_emotion_by_newspaper_joy/search1_total_hls
    search_dict_list.append(search1_dict_joy)

    search1_dict_anticip = {}
    searchword_headline_emotion_by_newspaper_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(anticip__gt=0).values('id').count()
    search1_dict_anticip['Search Term'] = str(search1.lower())
    search1_dict_anticip['Emotion'] = 'Anticipation'
    search1_dict_anticip['Count'] = searchword_headline_emotion_by_newspaper_anticip/search1_total_hls
    search_dict_list.append(search1_dict_anticip)

    search1_dict_surprise = {}
    searchword_headline_emotion_by_newspaper_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(surprise__gt=0).values('id').count()
    search1_dict_surprise['Search Term'] = str(search1.lower())
    search1_dict_surprise['Emotion'] = 'Surprise'
    search1_dict_surprise['Count'] = searchword_headline_emotion_by_newspaper_surprise/search1_total_hls
    search_dict_list.append(search1_dict_surprise)

    search1_dict_sadness = {}
    searchword_headline_emotion_by_newspaper_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(sadness__gt=0).values('id').count()
    search1_dict_sadness['Search Term'] = str(search1.lower())
    search1_dict_sadness['Emotion'] = 'Sadness'
    search1_dict_sadness['Count'] = searchword_headline_emotion_by_newspaper_sadness/search1_total_hls
    search_dict_list.append(search1_dict_sadness)

    search1_dict_anger = {}
    searchword_headline_emotion_by_newspaper_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(anger__gt=0).values('id').count()
    search1_dict_anger['Search Term'] = str(search1.lower())
    search1_dict_anger['Emotion'] = 'Anger'
    search1_dict_anger['Count'] = searchword_headline_emotion_by_newspaper_anger/search1_total_hls
    search_dict_list.append(search1_dict_anger)

    search1_dict_disgust = {}
    searchword_headline_emotion_by_newspaper_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=search1).filter(disgust__gt=0).values('id').count()
    search1_dict_disgust['Search Term'] = str(search1.lower())
    search1_dict_disgust['Emotion'] = 'Disgust'
    search1_dict_disgust['Count'] = searchword_headline_emotion_by_newspaper_disgust/search1_total_hls
    search_dict_list.append(search1_dict_disgust)



    comparesent_month_overall = pd.DataFrame(search_dict_list)












    figcompare_month_pos_overall = px.line(comparesent_month_overall, x="Emotion", y="Count", color="Search Term", )


    figcompare_month_pos_overall.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=0, r=0, t=0, b=0, pad=0), xaxis_tickformat = '%b')


    html_div_compare_emotions_overall = str(plotly.offline.plot(figcompare_month_pos_overall, output_type='div', config = {'displayModeBar': False}))


    def get_monthly_query_data_search_term(search_term1, search_term2):
        searched1 = search_term1.lower()

        query_monthly_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(fear__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Fear", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(anger__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Anger", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(anticip__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Anticipation", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(trust__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Trust", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(surprise__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Surprise", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(sadness__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Sadness", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(disgust__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Disgust", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(joy__gt=0).values('newspaper').annotate(Date=TruncMonth("date")).annotate(mycolumn=Value("Joy", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))

        querylist = [query_monthly_fear, query_monthly_anger, query_monthly_anticip, query_monthly_trust, query_monthly_surprise, query_monthly_sadness, query_monthly_disgust, query_monthly_joy, ]

        nyt_query_data = []
        bbc_query_data = []
        fn_query_data = []
        overall_query_data = []

        for query in querylist:
            for record in query:
                if record['newspaper'] == 1:
                    nyt_query_data.append(record)
                    overall_query_data.append(record)
                elif record['newspaper'] == 2:
                    bbc_query_data.append(record)
                    overall_query_data.append(record)
                elif record['newspaper'] == 3:
                    fn_query_data.append(record)
                    overall_query_data.append(record)




        return overall_query_data, nyt_query_data, bbc_query_data, fn_query_data




    def sort_query_data_by_emotion(emotion_query):

        fear_data = []
        anger_data = []
        anticip_data = []
        trust_data = []
        surprise_data = []
        sadness_data = []
        disgust_data = []
        joy_data = []



        for record in emotion_query:
            if record['mycolumn'] == 'Fear':
                fear_data.append(record)
            elif record['mycolumn'] == 'Anger':
                anger_data.append(record)
            elif record['mycolumn'] == 'Anticipation':
                anticip_data.append(record)
            elif record['mycolumn'] == 'Trust':
                trust_data.append(record)
            elif record['mycolumn'] == 'Surprise':
                surprise_data.append(record)
            elif record['mycolumn'] == 'Sadness':
                sadness_data.append(record)
            elif record['mycolumn'] == 'Disgust':
                disgust_data.append(record)
            elif record['mycolumn'] == 'Joy':
                joy_data.append(record)

        return fear_data, anger_data, anticip_data, trust_data, surprise_data, sadness_data, disgust_data, joy_data

    all_data = get_monthly_query_data_search_term(search1,search2)


    overall_tab_data = all_data[0]

    overall_data = sort_query_data_by_emotion(all_data[0])

    nyt_data = sort_query_data_by_emotion(all_data[1])
    bbc_data = sort_query_data_by_emotion(all_data[2])
    fn_data = sort_query_data_by_emotion(all_data[3])

    def get_plot_by_emotion(data_set):
        output_list = []
        for data in data_set:
            if len(data) > 0:
                comparesent = pd.DataFrame(list(data))

                comparesent.rename(columns={'search_term':'Search Term'}, inplace= True)


                figcompare = px.line(comparesent, x="Date", y="Count", color="Search Term",   )


                figcompare.update_layout(
                    font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




                html_div_compare = str(plotly.offline.plot(figcompare, output_type='div', config = {'displayModeBar': False}))
                output_list.append(html_div_compare)
            else:
                output_list.append('<div class="plotly-graph-div js-plotly-plot">Not enough occurrences of "'+ search1 + '" to plot line</div>')


        return output_list


    nyt_fear_search_date_div = get_plot_by_emotion(nyt_data)[0]
    nyt_anger_search_date_div = get_plot_by_emotion(nyt_data)[1]
    nyt_anticip_search_date_div = get_plot_by_emotion(nyt_data)[2]
    nyt_trust_search_date_div = get_plot_by_emotion(nyt_data)[3]
    nyt_surprise_search_date_div = get_plot_by_emotion(nyt_data)[4]
    nyt_sadness_search_date_div = get_plot_by_emotion(nyt_data)[5]
    nyt_disgust_search_date_div = get_plot_by_emotion(nyt_data)[6]
    nyt_joy_search_date_div = get_plot_by_emotion(nyt_data)[7]

    bbc_fear_search_date_div = get_plot_by_emotion(bbc_data)[0]
    bbc_anger_search_date_div = get_plot_by_emotion(bbc_data)[1]
    bbc_anticip_search_date_div = get_plot_by_emotion(bbc_data)[2]
    bbc_trust_search_date_div = get_plot_by_emotion(bbc_data)[3]
    bbc_surprise_search_date_div = get_plot_by_emotion(bbc_data)[4]
    bbc_sadness_search_date_div = get_plot_by_emotion(bbc_data)[5]
    bbc_disgust_search_date_div = get_plot_by_emotion(bbc_data)[6]
    bbc_joy_search_date_div = get_plot_by_emotion(bbc_data)[7]

    fn_fear_search_date_div = get_plot_by_emotion(fn_data)[0]
    fn_anger_search_date_div = get_plot_by_emotion(fn_data)[1]
    fn_anticip_search_date_div = get_plot_by_emotion(fn_data)[2]
    fn_trust_search_date_div = get_plot_by_emotion(fn_data)[3]
    fn_surprise_search_date_div = get_plot_by_emotion(fn_data)[4]
    fn_sadness_search_date_div = get_plot_by_emotion(fn_data)[5]
    fn_disgust_search_date_div = get_plot_by_emotion(fn_data)[6]
    fn_joy_search_date_div = get_plot_by_emotion(fn_data)[7]


    #below is Compare tab code

    for emotion in overall_data:
        for record in emotion:
            if record['newspaper'] == 1 and record['search_term'] == str(search1.lower()):
                record['search_term'] = 'The New York Times - ' + str(search1.lower())
            elif record['newspaper'] == 2 and record['search_term'] == str(search1.lower()):
                record['search_term'] = 'BBC News - ' + str(search1.lower())
            elif record['newspaper'] == 3 and record['search_term'] == str(search1.lower()):
                record['search_term'] = 'Fox News - ' + str(search1.lower())

            elif record['newspaper'] == 1 and record['search_term'] == str(search2.lower()):
                record['search_term'] = 'The New York Times - ' + str(search2.lower())
            elif record['newspaper'] == 2 and record['search_term'] == str(search2.lower()):
                record['search_term'] = 'BBC News - ' + str(search2.lower())
            elif record['newspaper'] == 3 and record['search_term'] == str(search2.lower()):
                record['search_term'] = 'Fox News - ' + str(search2.lower())



    compare_fear_search_date_div = get_plot_by_emotion(overall_data)[0]
    compare_anger_search_date_div = get_plot_by_emotion(overall_data)[1]
    compare_anticip_search_date_div = get_plot_by_emotion(overall_data)[2]
    compare_trust_search_date_div = get_plot_by_emotion(overall_data)[3]
    compare_surprise_search_date_div = get_plot_by_emotion(overall_data)[4]
    compare_sadness_search_date_div = get_plot_by_emotion(overall_data)[5]
    compare_disgust_search_date_div = get_plot_by_emotion(overall_data)[6]
    compare_joy_search_date_div = get_plot_by_emotion(overall_data)[7]


    def get_monthly_query_data_search_term_overall(search_term1, search_term2):
        searched1 = search_term1.lower()
        searched2 = search_term2.lower()
        query_monthly_fear = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(fear__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Fear", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anger = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(anger__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Anger", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_anticip = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(anticip__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Anticipation", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_trust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(trust__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Trust", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_surprise = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(surprise__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Surprise", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_sadness = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(sadness__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Sadness", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_disgust = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(disgust__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Disgust", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))
        query_monthly_joy = Headline_emotion.objects.filter(day_order__lte=25).filter(headline__icontains=searched1).filter(joy__gt=0).annotate(Date=TruncMonth("date")).values("Date").annotate(mycolumn=Value("Joy", output_field=CharField())).annotate(search_term=Value(str(searched1), output_field=CharField())).annotate(Count=Count("id"))


        querylist = [query_monthly_fear, query_monthly_anger, query_monthly_anticip, query_monthly_trust, query_monthly_surprise, query_monthly_sadness, query_monthly_disgust, query_monthly_joy, ]


        overall_query_data = []


        for query in querylist:
            for record in query:

                    overall_query_data.append(record)




        return overall_query_data



    overall_search_data_sort = sort_query_data_by_emotion(get_monthly_query_data_search_term_overall(search1,search2))









    overall_search_fear_search_date_div = get_plot_by_emotion(overall_search_data_sort)[0]
    overall_search_anger_search_date_div = get_plot_by_emotion(overall_search_data_sort)[1]
    overall_search_anticip_search_date_div = get_plot_by_emotion(overall_search_data_sort)[2]
    overall_search_trust_search_date_div = get_plot_by_emotion(overall_search_data_sort)[3]
    overall_search_surprise_search_date_div = get_plot_by_emotion(overall_search_data_sort)[4]
    overall_search_sadness_search_date_div = get_plot_by_emotion(overall_search_data_sort)[5]
    overall_search_disgust_search_date_div = get_plot_by_emotion(overall_search_data_sort)[6]
    overall_search_joy_search_date_div = get_plot_by_emotion(overall_search_data_sort)[7]


    return render(request, 'custom_scraper/emotion_search_compare_result_single.html',{'form1':form1, 'search1':search1, 'search2':search2, 'html_div_compare_emotions': html_div_compare_emotions, 'html_div_compare_emotions_overall': html_div_compare_emotions_overall, 'html_div_compare_emotions_nyt': html_div_compare_emotions_nyt, 'html_div_compare_emotions_bbc': html_div_compare_emotions_bbc, 'html_div_compare_emotions_fn': html_div_compare_emotions_fn, 'compare_fear_search_date_div': compare_fear_search_date_div, 'compare_anger_search_date_div': compare_anger_search_date_div, 'compare_anticip_search_date_div': compare_anticip_search_date_div, 'compare_trust_search_date_div': compare_trust_search_date_div, 'compare_surprise_search_date_div': compare_surprise_search_date_div, 'compare_joy_search_date_div': compare_joy_search_date_div, 'compare_sadness_search_date_div': compare_sadness_search_date_div, 'compare_disgust_search_date_div': compare_disgust_search_date_div, 'compare_fear_search_date_div': compare_fear_search_date_div, 'nyt_anger_search_date_div': nyt_anger_search_date_div, 'nyt_anticip_search_date_div': nyt_anticip_search_date_div, 'nyt_trust_search_date_div': nyt_trust_search_date_div, 'nyt_surprise_search_date_div': nyt_surprise_search_date_div, 'nyt_joy_search_date_div': nyt_joy_search_date_div, 'nyt_sadness_search_date_div': nyt_sadness_search_date_div, 'nyt_disgust_search_date_div': nyt_disgust_search_date_div, 'nyt_fear_search_date_div': nyt_fear_search_date_div, 'overall_search_fear_search_date_div': overall_search_fear_search_date_div, 'overall_search_anger_search_date_div': overall_search_anger_search_date_div, 'overall_search_anticip_search_date_div': overall_search_anticip_search_date_div, 'overall_search_trust_search_date_div': overall_search_trust_search_date_div, 'overall_search_surprise_search_date_div': overall_search_surprise_search_date_div, 'overall_search_joy_search_date_div': overall_search_joy_search_date_div, 'overall_search_sadness_search_date_div': overall_search_sadness_search_date_div, 'overall_search_disgust_search_date_div': overall_search_disgust_search_date_div, 'overall_search_fear_search_date_div': overall_search_fear_search_date_div,'bbc_anger_search_date_div': bbc_anger_search_date_div, 'bbc_anticip_search_date_div': bbc_anticip_search_date_div, 'bbc_trust_search_date_div': bbc_trust_search_date_div, 'bbc_surprise_search_date_div': bbc_surprise_search_date_div, 'bbc_joy_search_date_div': bbc_joy_search_date_div, 'bbc_sadness_search_date_div': bbc_sadness_search_date_div, 'bbc_disgust_search_date_div': bbc_disgust_search_date_div, 'bbc_fear_search_date_div': bbc_fear_search_date_div, 'fn_anger_search_date_div': fn_anger_search_date_div, 'fn_anticip_search_date_div': fn_anticip_search_date_div, 'fn_trust_search_date_div': fn_trust_search_date_div, 'fn_surprise_search_date_div': fn_surprise_search_date_div, 'fn_joy_search_date_div': fn_joy_search_date_div, 'fn_sadness_search_date_div': fn_sadness_search_date_div, 'fn_disgust_search_date_div': fn_disgust_search_date_div, 'fn_fear_search_date_div': fn_fear_search_date_div, } )



def emotion_search_compare_single(request):
    form1 = CompareSearchSingle()


    form2 = CompareSearch2()


    import plotly.graph_objects as go

    from datetime import datetime

    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today = str(today)[:10]
    yesterday = str(yesterday)[:10]


    if not Headline.objects.filter(date__contains=today).values('headline'):
        today = yesterday


    top_10_words_terms = word_count_general.objects.filter(newspaper=4).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:9]
    test_terms = []
    test_overall_values_list = []
    for i in top_10_words_terms:
        test_terms.append(i['word'])
        test_overall_values_list.append(i['word_count'])



    test_values_list = []

    for i in range(1,4):
        newspaper_values = []
        for y in test_terms:
            all_test_values = word_count_general.objects.filter(date__contains=today).filter(newspaper=i).filter(word=y).values('word_count')
            for record in all_test_values:
                newspaper_values.append(record['word_count'])
        test_values_list.append(newspaper_values)






    test_ny_values_list = test_values_list[0]
    test_bbc_values_list = test_values_list[1]
    test_fn_values_list = test_values_list[2]




    values_fig = go.Figure(data=[
        go.Bar(name='New York Times', y=test_terms, x=test_ny_values_list, orientation='h', marker_color="#2d2e30"),
        go.Bar(name='BBC News', y=test_terms, x=test_bbc_values_list, orientation = 'h', marker_color="#bb1919"),
        go.Bar(name='Fox News', y=test_terms, x=test_fn_values_list, orientation = 'h', marker_color="rgba(0,51,102,.99)"),
    ], )
    values_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), height=400, plot_bgcolor='white', orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))


    return render(request, 'custom_scraper/emotion_search_compare_single.html',{'form1':form1, 'form2':form2, 'html_div_values': html_div_values,   } )





def wc_search_compare_result(request):
    form1 = CompareSearch1()


    form2 = CompareSearch2()

    search1 = request.GET.get('compare1')


    search2 = request.GET.get('compare2')


    key1data = Headline.objects.filter(headline__icontains=search1)
    key2data = Headline.objects.filter(headline__icontains=search2)

    from django.shortcuts import redirect
    if not key1data or len(key1data) < 3 or not key2data or len(key2data) < 3:
        request.session['search1'] = search1
        request.session['search2'] = search2



        return redirect('research_wc_compare')


    from django.db.models import Count

    count_by_newspaper_1 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).values('newspaper').annotate(Search_1=Count('id'))
    count_by_newspaper_2 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).values('newspaper').annotate(Search_2=Count('id'))

    #combine results in one list so easier to parse/edit
    all_counts_by_newspaper_1 = []
    all_counts_by_newspaper_2 = []
    for record in count_by_newspaper_1:
        all_counts_by_newspaper_1.append(record)
    for record in count_by_newspaper_2:
        all_counts_by_newspaper_2.append(record)

    #fill in blank records in case there are no results for one of the newspapers. needs data this way because of how the bar graph is set up
    for i in range(1,4):
        newspaper_check = 0
        for record in all_counts_by_newspaper_1:
            if record['newspaper'] == i:
                newspaper_check += 1
        if newspaper_check == 0:
            all_counts_by_newspaper_1.append({'newspaper': i, 'Search_1': 0 })

    for i in range(1,4):
        newspaper_check = 0
        for record in all_counts_by_newspaper_2:
            if record['newspaper'] == i:
                newspaper_check += 1
        if newspaper_check == 0:
            all_counts_by_newspaper_2.append({'newspaper': i, 'Search_2': 0 })



    #get lists to sort in newspaper order so that does not mess up comparison bar graphs (order matters)
    sorted_1 = []
    for record in all_counts_by_newspaper_1:
        if record['newspaper'] == 1:
            sorted_1.append(record)

    for record in all_counts_by_newspaper_1:
        if record['newspaper'] == 2:
            sorted_1.append(record)

    for record in all_counts_by_newspaper_1:
        if record['newspaper'] == 3:
            sorted_1.append(record)
    all_counts_by_newspaper_1 = sorted_1

    sorted_2 = []
    for record in all_counts_by_newspaper_2:
        if record['newspaper'] == 1:
            sorted_2.append(record)

    for record in all_counts_by_newspaper_2:
        if record['newspaper'] == 2:
            sorted_2.append(record)

    for record in all_counts_by_newspaper_2:
        if record['newspaper'] == 3:
            sorted_2.append(record)
    all_counts_by_newspaper_2 = sorted_2



    search_1_values = []
    for i in all_counts_by_newspaper_1:
        search_1_values.append(i['Search_1'])

    search_2_values = []
    for i in all_counts_by_newspaper_2:
        search_2_values.append(i['Search_2'])




    paper_list = ['The New York Times', 'BBC News', 'Fox News']


    import plotly.graph_objects as go



    fig_bar_graph_compare = go.Figure(data=[
    go.Bar(name=str(search1), x=paper_list, y=search_1_values),
    go.Bar(name=str(search2), x=paper_list, y=search_2_values)])

    fig_bar_graph_compare.update_layout( legend={'traceorder':'normal'}, )
    fig_bar_graph_compare.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )




    html_fig_bar_graph_compare = str(plotly.offline.plot(fig_bar_graph_compare, output_type='div', config = {'displayModeBar': False}))


    #now bargraph for overall
    overall_list = ['All Newspapers']

    overall_search1_values = []
    overall_search1 = 0
    for i in search_1_values:
        overall_search1 += i

    overall_search1_values.append(overall_search1)

    overall_search2_values = []
    overall_search2 = 0
    for i in search_2_values:
        overall_search2 += i

    overall_search2_values.append(overall_search2)

    fig_bar_graph_compare_overall = go.Figure(data=[
    go.Bar(name=str(search1), x=overall_list, y=overall_search1_values),
    go.Bar(name=str(search2), x=overall_list, y=overall_search2_values)])

    fig_bar_graph_compare_overall.update_layout( legend={'traceorder':'normal'}, )
    fig_bar_graph_compare_overall.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )




    html_fig_bar_graph_compare_overall = str(plotly.offline.plot(fig_bar_graph_compare_overall, output_type='div', config = {'displayModeBar': False}))


    #now by newspaper
    def get_graph_by_newspaper(paper_list_var, search_1_values_var, search_2_values_var, search1_var, search2_var):
        output_list = []
        for i in range(0,3):

            fig_bar_graph_compare = go.Figure(data=[
            go.Bar(name=str(search1_var), x=[paper_list_var[i]], y=[search_1_values_var[i]]),
            go.Bar(name=str(search2_var), x=[paper_list_var[i]], y=[search_2_values_var[i]])])

            fig_bar_graph_compare.update_layout( legend={'traceorder':'normal'}, )
            fig_bar_graph_compare.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )




            html_fig_bar_graph_compare = str(plotly.offline.plot(fig_bar_graph_compare, output_type='div', config = {'displayModeBar': False}))

            output_list.append(html_fig_bar_graph_compare)

        return output_list

    html_fig_bar_graph_compare_nyt = get_graph_by_newspaper(paper_list, search_1_values, search_2_values, search1, search2)[0]
    html_fig_bar_graph_compare_bbc = get_graph_by_newspaper(paper_list, search_1_values, search_2_values, search1, search2)[1]
    html_fig_bar_graph_compare_fn = get_graph_by_newspaper(paper_list, search_1_values, search_2_values, search1, search2)[2]


    search1_count_newspaper_month = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).values('newspaper').annotate(Date=TruncMonth('date')).annotate(Count=Count('id'))
    search2_count_newspaper_month = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).values('newspaper').annotate(Date=TruncMonth('date')).annotate(Count=Count('id'))

    search1_count_newspaper_list = []
    for record in search1_count_newspaper_month:
        search1_count_newspaper_list.append(record)

    search2_count_newspaper_list = []
    for record in search2_count_newspaper_month:
        search2_count_newspaper_list.append(record)

    for record in search1_count_newspaper_list:
        if record['newspaper'] == 1:
            record['Search Term'] = 'The New York Times - ' + str(search1)
        elif record['newspaper'] == 2:
            record['Search Term'] = 'BBC News - ' + str(search1)
        elif record['newspaper'] == 3:
            record['Search Term'] = 'Fox News - ' + str(search1)

    for record in search2_count_newspaper_list:
        if record['newspaper'] == 1:
            record['Search Term'] = 'The New York Times - ' + str(search2)
        elif record['newspaper'] == 2:
            record['Search Term'] = 'BBC News - ' + str(search2)
        elif record['newspaper'] == 3:
            record['Search Term'] = 'Fox News - ' + str(search2)


    all_data_count_newspaper = []
    for record in search1_count_newspaper_list:
        all_data_count_newspaper.append(record)

    for record in search2_count_newspaper_list:
        all_data_count_newspaper.append(record)

    comparewc = pd.DataFrame(list(all_data_count_newspaper))




    figcomparewc = px.line(comparewc, x="Date", y="Count", color="Search Term",   )


    figcomparewc.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




    html_div_compare_wc = str(plotly.offline.plot(figcomparewc, output_type='div', config = {'displayModeBar': False}))


    #get count by date by newspaper

    def get_by_date_by_newspaper(all_data_count_newspaper_var):
        output_list = []
        for i in range(1,4):
            this_newspaper_data = []
            for record in all_data_count_newspaper_var:

                if record['newspaper'] == i:
                    this_newspaper_data.append(record)


            comparewc = pd.DataFrame(list(this_newspaper_data))




            figcomparewc = px.line(comparewc, x="Date", y="Count", color="Search Term",   )


            figcomparewc.update_layout(
                font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




            html_div_compare_wc = str(plotly.offline.plot(figcomparewc, output_type='div', config = {'displayModeBar': False}))

            output_list.append(html_div_compare_wc)
        return output_list

    html_div_compare_date_nyt = get_by_date_by_newspaper(all_data_count_newspaper)[0]
    html_div_compare_date_bbc = get_by_date_by_newspaper(all_data_count_newspaper)[1]
    html_div_compare_date_fn = get_by_date_by_newspaper(all_data_count_newspaper)[2]


    #overall by date

    search1_overall = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id')).annotate(Term=Value(str(search1), output_field=CharField()))
    search2_overall = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id')).annotate(Term=Value(str(search2), output_field=CharField()))

    overall_data = []

    for record in search1_overall:
        overall_data.append(record)

    for record in search2_overall:
        overall_data.append(record)




    comparewc_overall = pd.DataFrame(list(overall_data))




    figcomparewc_overall = px.line(comparewc_overall, x="Date", y="Count", color="Term",   )


    figcomparewc_overall.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




    html_div_compare_wc_overall = str(plotly.offline.plot(figcomparewc_overall, output_type='div', config = {'displayModeBar': False}))



    return render(request, 'custom_scraper/wc_search_compare_result.html',{'form1':form1, 'search1':search1, 'search2':search2, 'html_fig_bar_graph_compare': html_fig_bar_graph_compare, 'html_div_compare_wc': html_div_compare_wc, 'html_fig_bar_graph_compare_overall': html_fig_bar_graph_compare_overall, 'html_fig_bar_graph_compare_nyt': html_fig_bar_graph_compare_nyt, 'html_fig_bar_graph_compare_bbc': html_fig_bar_graph_compare_bbc, 'html_fig_bar_graph_compare_fn': html_fig_bar_graph_compare_fn, 'html_div_compare_date_nyt': html_div_compare_date_nyt, 'html_div_compare_date_bbc': html_div_compare_date_bbc, 'html_div_compare_date_fn': html_div_compare_date_fn, 'html_div_compare_wc_overall': html_div_compare_wc_overall  } )



def wc_search_compare(request):
    form1 = CompareSearch1()


    form2 = CompareSearch2()


    import plotly.graph_objects as go

    from datetime import datetime

    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today = str(today)[:10]
    yesterday = str(yesterday)[:10]

    if not Headline.objects.filter(date__contains=today).values('headline'):
        today = yesterday


    top_10_words_terms = word_count_general.objects.filter(newspaper=4).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:9]
    test_terms = []
    test_overall_values_list = []
    for i in top_10_words_terms:
        test_terms.append(i['word'])
        test_overall_values_list.append(i['word_count'])



    test_values_list = []

    for i in range(1,4):
        newspaper_values = []
        for y in test_terms:
            all_test_values = word_count_general.objects.filter(date__contains=today).filter(newspaper=i).filter(word=y).values('word_count')
            for record in all_test_values:
                newspaper_values.append(record['word_count'])
        test_values_list.append(newspaper_values)






    test_ny_values_list = test_values_list[0]
    test_bbc_values_list = test_values_list[1]
    test_fn_values_list = test_values_list[2]




    values_fig = go.Figure(data=[
        go.Bar(name='New York Times', y=test_terms, x=test_ny_values_list, orientation='h', marker_color="#2d2e30"),
        go.Bar(name='BBC News', y=test_terms, x=test_bbc_values_list, orientation = 'h', marker_color="#bb1919"),
        go.Bar(name='Fox News', y=test_terms, x=test_fn_values_list, orientation = 'h', marker_color="rgba(0,51,102,.99)"),
    ], )
    values_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), height=400, plot_bgcolor='white', orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))







    return render(request, 'custom_scraper/wc_search_compare.html',{'form1':form1, 'form2':form2, 'html_div_values': html_div_values,    } )


def research_wc_compare(request):

    form1 = CompareSearch1()

    search1 = request.session['search1']
    search2 = request.session['search2']



    return render(request, 'custom_scraper/research_wc_compare.html',{'form1':form1, 'search1':search1, 'search2':search2},)

def research_wc_compare_single(request):

    form1 = CompareSearchSingle()

    search1 = request.session['search1']
    search2 = request.session['search2']



    return render(request, 'custom_scraper/research_wc_compare_single.html',{'form1':form1, 'search1':search1, 'search2':search2},)


def wc_search_compare_single(request):

    from datetime import datetime
    form1 = CompareSearchSingle()
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today = str(today)[:10]
    yesterday = str(yesterday)[:10]


    if not Headline.objects.filter(date__contains=today).values('headline'):
        today = yesterday


    top_10_words_terms = word_count_general.objects.filter(newspaper=4).filter(date__contains=today).values('word', 'word_count').order_by('-word_count')[:9]
    test_terms = []
    test_overall_values_list = []
    for i in top_10_words_terms:
        test_terms.append(i['word'])
        test_overall_values_list.append(i['word_count'])



    test_values_list = []

    for i in range(1,4):
        newspaper_values = []
        for y in test_terms:
            all_test_values = word_count_general.objects.filter(date__contains=today).filter(newspaper=i).filter(word=y).values('word_count')
            for record in all_test_values:
                newspaper_values.append(record['word_count'])
        test_values_list.append(newspaper_values)






    test_ny_values_list = test_values_list[0]
    test_bbc_values_list = test_values_list[1]
    test_fn_values_list = test_values_list[2]


    import plotly.graph_objects as go


    values_fig = go.Figure(data=[
        go.Bar(name='New York Times', y=test_terms, x=test_ny_values_list, orientation='h', marker_color="#2d2e30"),
        go.Bar(name='BBC News', y=test_terms, x=test_bbc_values_list, orientation = 'h', marker_color="#bb1919"),
        go.Bar(name='Fox News', y=test_terms, x=test_fn_values_list, orientation = 'h', marker_color="rgba(0,51,102,.99)"),
    ], )
    values_fig.update_layout(barmode='stack', legend={'traceorder':'normal'})
    values_fig.update_layout(
       font=dict(family="Roboto",size=15,color="black"), height=400, plot_bgcolor='white', orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))








    return render(request, 'custom_scraper/wc_search_compare_single.html',{'form1':form1, 'html_div_values': html_div_values,   } )



def wc_search_compare_result_single(request):
    form1 = CompareSearchSingle()


    form2 = CompareSearch2()

    search1 = request.GET.get('compare1')


    search2 = "This is an empty search so that can use compare code for single search"


    key1data = Headline.objects.filter(headline__icontains=search1)


    from django.shortcuts import redirect
    if not key1data or len(key1data) < 3:
        request.session['search1'] = search1
        request.session['search2'] = search2



        return redirect('research_wc_compare_single')


    from django.db.models import Count

    count_by_newspaper_1 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).values('newspaper').annotate(Search_1=Count('id'))
    count_by_newspaper_2 = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).values('newspaper').annotate(Search_2=Count('id'))

    #combine results in one list so easier to parse/edit
    all_counts_by_newspaper_1 = []
    all_counts_by_newspaper_2 = []
    for record in count_by_newspaper_1:
        all_counts_by_newspaper_1.append(record)
    for record in count_by_newspaper_2:
        all_counts_by_newspaper_2.append(record)

    #fill in blank records in case there are no results for one of the newspapers. needs data this way because of how the bar graph is set up
    for i in range(1,4):
        newspaper_check = 0
        for record in all_counts_by_newspaper_1:
            if record['newspaper'] == i:
                newspaper_check += 1
        if newspaper_check == 0:
            all_counts_by_newspaper_1.append({'newspaper': i, 'Search_1': 0 })

    for i in range(1,4):
        newspaper_check = 0
        for record in all_counts_by_newspaper_2:
            if record['newspaper'] == i:
                newspaper_check += 1
        if newspaper_check == 0:
            all_counts_by_newspaper_2.append({'newspaper': i, 'Search_2': 0 })

    #get lists to sort in newspaper order so that does not mess up comparison bar graphs (order matters)
    sorted_1 = []
    for record in all_counts_by_newspaper_1:
        if record['newspaper'] == 1:
            sorted_1.append(record)

    for record in all_counts_by_newspaper_1:
        if record['newspaper'] == 2:
            sorted_1.append(record)

    for record in all_counts_by_newspaper_1:
        if record['newspaper'] == 3:
            sorted_1.append(record)
    all_counts_by_newspaper_1 = sorted_1

    sorted_2 = []
    for record in all_counts_by_newspaper_2:
        if record['newspaper'] == 1:
            sorted_2.append(record)

    for record in all_counts_by_newspaper_2:
        if record['newspaper'] == 2:
            sorted_2.append(record)

    for record in all_counts_by_newspaper_2:
        if record['newspaper'] == 3:
            sorted_2.append(record)
    all_counts_by_newspaper_2 = sorted_2





    search_1_values = []
    for i in all_counts_by_newspaper_1:
        search_1_values.append(i['Search_1'])

    search_2_values = []
    for i in all_counts_by_newspaper_2:
        search_2_values.append(i['Search_2'])


    paper_list = ['The New York Times', 'BBC News', 'Fox News']


    import plotly.graph_objects as go



    fig_bar_graph_compare = go.Figure(data=[
    go.Bar(name=str(search1), x=paper_list, y=search_1_values, marker_color=["#2d2e30","#bb1919","rgba(0,51,102,.99)"]),
    ])

    fig_bar_graph_compare.update_layout( legend={'traceorder':'normal'}, )
    fig_bar_graph_compare.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )




    html_fig_bar_graph_compare = str(plotly.offline.plot(fig_bar_graph_compare, output_type='div', config = {'displayModeBar': False}))


    #now bargraph for overall
    overall_list = ['All Newspapers']

    overall_search1_values = []
    overall_search1 = 0
    for i in search_1_values:
        overall_search1 += i

    overall_search1_values.append(overall_search1)

    overall_search2_values = []
    overall_search2 = 0
    for i in search_2_values:
        overall_search2 += i

    overall_search2_values.append(overall_search2)

    """
    fig_bar_graph_compare_overall = go.Figure(data=[
    go.Bar(name=str(search1), x=overall_list, y=overall_search1_values),
    ])

    fig_bar_graph_compare_overall.update_layout( legend={'traceorder':'normal'}, )
    fig_bar_graph_compare_overall.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )




    html_fig_bar_graph_compare_overall = str(plotly.offline.plot(fig_bar_graph_compare_overall, output_type='div', config = {'displayModeBar': False}))

    """
    html_fig_bar_graph_compare_overall = overall_search1_values[0]

    #now by newspaper
    def get_graph_by_newspaper(paper_list_var, search_1_values_var, search_2_values_var, search1_var, search2_var):
        output_list = []
        for i in range(0,3):
            """
            fig_bar_graph_compare = go.Figure(data=[
            go.Bar(name=str(search1_var), x=[paper_list_var[i]], y=[search_1_values_var[i]]),
            ])

            fig_bar_graph_compare.update_layout( legend={'traceorder':'normal'}, )
            fig_bar_graph_compare.update_layout( font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='white', orientation=90, margin=dict(t=10,pad=10), )




            html_fig_bar_graph_compare = str(plotly.offline.plot(fig_bar_graph_compare, output_type='div', config = {'displayModeBar': False}))

            output_list.append(html_fig_bar_graph_compare)
            """
            output_list.append(search_1_values_var[i])
        return output_list

    html_fig_bar_graph_compare_nyt = get_graph_by_newspaper(paper_list, search_1_values, search_2_values, search1, search2)[0]
    html_fig_bar_graph_compare_bbc = get_graph_by_newspaper(paper_list, search_1_values, search_2_values, search1, search2)[1]
    html_fig_bar_graph_compare_fn = get_graph_by_newspaper(paper_list, search_1_values, search_2_values, search1, search2)[2]


    search1_count_newspaper_month = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).values('newspaper').annotate(Date=TruncMonth('date')).annotate(Count=Count('id'))
    search2_count_newspaper_month = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).values('newspaper').annotate(Date=TruncMonth('date')).annotate(Count=Count('id'))

    search1_count_newspaper_list = []
    for record in search1_count_newspaper_month:
        search1_count_newspaper_list.append(record)

    search2_count_newspaper_list = []
    for record in search2_count_newspaper_month:
        search2_count_newspaper_list.append(record)

    for record in search1_count_newspaper_list:
        if record['newspaper'] == 1:
            record['Search Term'] = 'The New York Times - ' + str(search1)
        elif record['newspaper'] == 2:
            record['Search Term'] = 'BBC News - ' + str(search1)
        elif record['newspaper'] == 3:
            record['Search Term'] = 'Fox News - ' + str(search1)

    for record in search2_count_newspaper_list:
        if record['newspaper'] == 1:
            record['Search Term'] = 'The New York Times - ' + str(search2)
        elif record['newspaper'] == 2:
            record['Search Term'] = 'BBC News - ' + str(search2)
        elif record['newspaper'] == 3:
            record['Search Term'] = 'Fox News - ' + str(search2)


    all_data_count_newspaper = []
    for record in search1_count_newspaper_list:
        all_data_count_newspaper.append(record)

    for record in search2_count_newspaper_list:
        all_data_count_newspaper.append(record)

    comparewc = pd.DataFrame(list(all_data_count_newspaper))




    figcomparewc = px.line(comparewc, x="Date", y="Count", color="Search Term", color_discrete_map={'The New York Times - ' + str(search1):"#8e949e",'BBC News - ' + str(search1):"#e61e1e",'Fox News - '+str(search1):"#006edb" }  )

    figcomparewc.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300,  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




    html_div_compare_wc = str(plotly.offline.plot(figcomparewc, output_type='div', config = {'displayModeBar': False}))


    #get count by date by newspaper

    def get_by_date_by_newspaper(all_data_count_newspaper_var):
        output_list = []
        for i in range(1,4):
            this_newspaper_data = []
            for record in all_data_count_newspaper_var:

                if record['newspaper'] == i:
                    this_newspaper_data.append(record)

            if len(this_newspaper_data) < 2:
                html_div_compare_wc = '<div class="plotly-graph-div js-plotly-plot">Not enough occurrences of "'+ search1 + '" to plot line</div>'
            else:
                comparewc = pd.DataFrame(list(this_newspaper_data))




                figcomparewc = px.line(comparewc, x="Date", y="Count", color="Search Term",   )


                figcomparewc.update_layout(
                    font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




                html_div_compare_wc = str(plotly.offline.plot(figcomparewc, output_type='div', config = {'displayModeBar': False}))

            output_list.append(html_div_compare_wc)
        return output_list

    html_div_compare_date_nyt = get_by_date_by_newspaper(all_data_count_newspaper)[0]
    html_div_compare_date_bbc = get_by_date_by_newspaper(all_data_count_newspaper)[1]
    html_div_compare_date_fn = get_by_date_by_newspaper(all_data_count_newspaper)[2]


    #overall by date

    search1_overall = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search1).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id')).annotate(Term=Value(str(search1), output_field=CharField()))
    search2_overall = Headline.objects.filter(day_order__lte=25).filter(headline__icontains=search2).annotate(Date=TruncMonth('date')).values('Date').annotate(Count=Count('id')).annotate(Term=Value(str(search2), output_field=CharField()))

    overall_data = []

    for record in search1_overall:
        overall_data.append(record)

    for record in search2_overall:
        overall_data.append(record)




    comparewc_overall = pd.DataFrame(list(overall_data))




    figcomparewc_overall = px.line(comparewc_overall, x="Date", y="Count", color="Term",   )


    figcomparewc_overall.update_layout(
        font=dict(family="Roboto",size=15,color="black"), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',xaxis_title='', yaxis_title='', margin=dict(l=5, r=5, t=5, b=5, pad=10))




    html_div_compare_wc_overall = str(plotly.offline.plot(figcomparewc_overall, output_type='div', config = {'displayModeBar': False}))



    return render(request, 'custom_scraper/wc_search_compare_result_single.html',{'form1':form1, 'search1':search1, 'search2':search2, 'html_fig_bar_graph_compare': html_fig_bar_graph_compare, 'html_div_compare_wc': html_div_compare_wc, 'html_fig_bar_graph_compare_overall': html_fig_bar_graph_compare_overall, 'html_fig_bar_graph_compare_nyt': html_fig_bar_graph_compare_nyt, 'html_fig_bar_graph_compare_bbc': html_fig_bar_graph_compare_bbc, 'html_fig_bar_graph_compare_fn': html_fig_bar_graph_compare_fn, 'html_div_compare_date_nyt': html_div_compare_date_nyt, 'html_div_compare_date_bbc': html_div_compare_date_bbc, 'html_div_compare_date_fn': html_div_compare_date_fn, 'html_div_compare_wc_overall': html_div_compare_wc_overall  } )

def hl_search_compare_single(request):
    form1 = CompareSearchSingle()


    form2 = CompareSearch2()


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
            if key != "s" and key != "’" and key != "‘" and key != "t" and key != "i":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list




    allheadlines = Headline.objects.all()


    allkeywords = find_keywords(allheadlines)



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
                if key == "us":
                    counter += 1
                    continue
                if key == "virus":
                    counter += 1
                    continue
                counter += 1
                key_count_by_paper = Headline.objects.filter(headline__contains=key).filter(day_order__lte=25).values("newspaper").annotate(Count=Count('id')).order_by("newspaper")
                keylist = []
                keylist.append(key)

                nytimescount = key_count_by_paper[0]['Count']
                bbccount = key_count_by_paper[1]['Count']
                fncount = key_count_by_paper[2]['Count']
                keylist.append(nytimescount)
                keylist.append(bbccount)
                keylist.append(fncount)
                keylist.append(nytimescount + bbccount + fncount)
                all_terms_list.append(keylist)

        return all_terms_list



    terms_nums = produce_data_list_of_freq_by_newspaper(all_wf_keys, 10)
    terms_nums.sort(key = lambda x: x[4], reverse=True)




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
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))


    most_variance_words = []

    today_var_word = date.today()
    from custom_scraper.models import variance_table_word

    variance_words = variance_table_word.objects.filter(graphid=10).filter(date__contains=today_var_word).values('word', 'count', 'news1', 'news2', 'sentiment')

    for i in variance_words:
        interlist = []
        interlist.append(i['word'])
        interlist.append(i['count'])
        interlist.append(i['news1'])
        interlist.append(i['news2'])
        interlist.append(round(i['sentiment'],2))
        most_variance_words.append(interlist)

    most_popular_words = []
    for i in allkeywords[:100]:
        most_popular_words.append(i)






    return render(request, 'custom_scraper/hl_search_compare_single.html',{'form1':form1, 'form2':form2, 'html_div_values': html_div_values, 'most_variance_words': most_variance_words, 'most_popular_words': most_popular_words   } )

def hl_search_compare_result_single(request):
    date_picked_check = False
    form1 = CompareSearchSingle()


    form2 = CompareSearch2()

    search1 = request.GET.get('compare1')

    date_picked = request.GET.get('date')
    print(date_picked)
    search2 = "This is an empty search so that can use compare code for single search"

    current_tab = request.GET.get('tab_to')
    print(current_tab)

    date_range1 = request.GET.get('date1')
    date_range2 = request.GET.get('date2')

    key1data = Headline.objects.filter(headline__contains=search1)


    from django.shortcuts import redirect
    if not key1data or len(key1data) < 3:
        request.session['search1'] = search1
        request.session['search2'] = search2



        return redirect('research_hl_compare_single')


    from django.db.models import Count


    nyt_articles = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search1).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
    bbc_articles = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search1).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
    fn_articles = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search1).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')

    for i in nyt_articles:
        i['Date'] = i['Date'].date()

    for i in bbc_articles:
        i['Date'] = i['Date'].date()

    for i in fn_articles:
        i['Date'] = i['Date'].date()

    form = DateForm()


    return_dict = {'form': form, 'form1':form1, 'search1':search1, 'search2':search2, 'nyt_articles': nyt_articles, 'bbc_articles': bbc_articles, 'fn_articles': fn_articles,    }



    if current_tab == 'single_date' :
        date_range_heading_check = True
        nyt_articles_date = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search1).filter(date__icontains=date_picked).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
        bbc_articles_date = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search1).filter(date__icontains=date_picked).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
        fn_articles_date = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search1).filter(date__icontains=date_picked).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')

        for i in nyt_articles_date:
            i['Date'] = i['Date'].date()

        for i in bbc_articles_date:
            i['Date'] = i['Date'].date()

        for i in fn_articles_date:
            i['Date'] = i['Date'].date()

        if len(bbc_articles_date) < 1:
            bbc_articles_date = [{'headline':'No data for this date'}]

        if len(nyt_articles_date) < 1:
            nyt_articles_date = [{'headline':'No data for this date'}]

        if len(fn_articles_date) < 1:
            fn_articles_date = [{'headline':'No data for this date'}]

        return_dict['nyt_articles_date'] = nyt_articles_date
        return_dict['bbc_articles_date'] = bbc_articles_date
        return_dict['fn_articles_date'] = fn_articles_date

        navigate_to_tab = 'Date0'

        import datetime

        display_date = datetime.date(int(date_picked[:4]), int(date_picked[5:7]), int(date_picked[8:]))
        return_dict['display_date'] = display_date
        return_dict['navigate_to_tab'] = navigate_to_tab
        return_dict['date_range_heading_check'] = date_range_heading_check

    elif current_tab == 'date_range':
        date_range_heading_check = False
        nyt_articles_date = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search1).filter(date__range=[str(date_range1), str(date_range2)]).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
        bbc_articles_date = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search1).filter(date__range=[str(date_range1), str(date_range2)]).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
        fn_articles_date = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search1).filter(date__range=[str(date_range1), str(date_range2)]).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')

        for i in nyt_articles_date:
            i['Date'] = i['Date'].date()

        for i in bbc_articles_date:
            i['Date'] = i['Date'].date()

        for i in fn_articles_date:
            i['Date'] = i['Date'].date()

        if len(bbc_articles_date) < 1:
            bbc_articles_date = [{'headline':'No data for this date'}]

        if len(nyt_articles_date) < 1:
            nyt_articles_date = [{'headline':'No data for this date'}]

        if len(fn_articles_date) < 1:
            fn_articles_date = [{'headline':'No data for this date'}]

        return_dict['nyt_articles_date'] = nyt_articles_date
        return_dict['bbc_articles_date'] = bbc_articles_date
        return_dict['fn_articles_date'] = fn_articles_date

        navigate_to_tab = 'Date0'
        import datetime

        display_date_range1 = datetime.date(int(date_range1[:4]), int(date_range1[5:7]), int(date_range1[8:]))
        display_date_range2 = datetime.date(int(date_range2[:4]), int(date_range2[5:7]), int(date_range2[8:]))

        return_dict['display_date_range1'] = display_date_range1
        return_dict['display_date_range2'] = display_date_range2
        divider_string = " - "
        return_dict['navigate_to_tab'] = navigate_to_tab
        return_dict['date_range_heading_check'] = date_range_heading_check
        return_dict['divider_string'] = divider_string




    return render(request, 'custom_scraper/hl_search_compare_result_single.html',return_dict )








def research_hl_compare_single(request):

    form1 = CompareSearchSingle()

    search1 = request.session['search1']
    search2 = request.session['search2']



    return render(request, 'custom_scraper/research_hl_compare_single.html',{'form1':form1, 'search1':search1, 'search2':search2},)



def hl_search_compare(request):
    form1 = CompareSearch1()


    form2 = CompareSearch2()


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
            if key != "s" and key != "’" and key != "‘" and key != "t" and key != "i":
                interlist.append(value)
                interlist.append(key)
                nytimes_word_count_list.append(interlist)
        return nytimes_word_count_list




    allheadlines = Headline.objects.all()


    allkeywords = find_keywords(allheadlines)



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
                keylist.append(nytimescount + bbccount + fncount)
                print(keylist)
                all_terms_list.append(keylist)

        return all_terms_list



    terms_nums = produce_data_list_of_freq_by_newspaper(all_wf_keys, 10)
    terms_nums.sort(key = lambda x: x[4], reverse=True)




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
       font=dict(family="Roboto",size=15,color="black"), plot_bgcolor='white', orientation=90, yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=0, b=0, pad=10), )




    html_div_values = str(plotly.offline.plot(values_fig, output_type='div', config = {'displayModeBar': False}))


    most_variance_words = []

    today_var_word = date.today()
    from custom_scraper.models import variance_table_word

    variance_words = variance_table_word.objects.filter(graphid=10).filter(date__contains=today_var_word).values('word', 'count', 'news1', 'news2', 'sentiment')

    for i in variance_words:
        interlist = []
        interlist.append(i['word'])
        interlist.append(i['count'])
        interlist.append(i['news1'])
        interlist.append(i['news2'])
        interlist.append(round(i['sentiment'],2))
        most_variance_words.append(interlist)

    most_popular_words = []
    for i in allkeywords[:100]:
        most_popular_words.append(i)






    return render(request, 'custom_scraper/hl_search_compare.html',{'form1':form1, 'form2':form2, 'html_div_values': html_div_values, 'most_variance_words': most_variance_words, 'most_popular_words': most_popular_words   } )

def hl_search_compare_result(request):
    date_picked_check = False
    form1 = CompareSearch1()


    form2 = CompareSearch2()

    search1 = request.GET.get('compare1')

    date_picked = request.GET.get('date')
    print(date_picked)
    search2 = request.GET.get('compare2')

    current_tab = request.GET.get('tab_to')
    print(current_tab)

    date_range1 = request.GET.get('date1')
    date_range2 = request.GET.get('date2')

    key1data = Headline.objects.filter(headline__contains=search1)


    from django.shortcuts import redirect
    if not key1data or len(key1data) < 3:
        request.session['search1'] = search1
        request.session['search2'] = search2



        return redirect('research_hl_compare')


    from django.db.models import Count


    nyt_articles = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search1).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
    bbc_articles = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search1).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
    fn_articles = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search1).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')

    nyt_articles_2 = Headline.objects.filter(day_order__lte=25).filter(newspaper=1).filter(headline__icontains=search2).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
    bbc_articles_2 = Headline.objects.filter(day_order__lte=25).filter(newspaper=2).filter(headline__icontains=search2).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')
    fn_articles_2 = Headline.objects.filter(day_order__lte=25).filter(newspaper=3).filter(headline__icontains=search2).annotate(Date=TruncDay('date')).values('Date', 'headline', 'link')

    for i in nyt_articles:
        i['Date'] = i['Date'].date()

    for i in bbc_articles:
        i['Date'] = i['Date'].date()

    for i in fn_articles:
        i['Date'] = i['Date'].date()

    for i in nyt_articles_2:
        i['Date'] = i['Date'].date()

    for i in bbc_articles_2:
        i['Date'] = i['Date'].date()

    for i in fn_articles_2:
        i['Date'] = i['Date'].date()

    form = DateForm()


    return_dict = {'form': form, 'form1':form1, 'search1':search1, 'search2':search2, 'nyt_articles': nyt_articles, 'bbc_articles': bbc_articles, 'fn_articles': fn_articles, 'nyt_articles_2': nyt_articles_2, 'bbc_articles_2': bbc_articles_2, 'fn_articles_2': fn_articles_2,   }







    return render(request, 'custom_scraper/hl_search_compare_result.html',return_dict )


def research_hl_compare(request):

    form1 = CompareSearch1()

    search1 = request.session['search1']
    search2 = request.session['search2']



    return render(request, 'custom_scraper/research_hl_compare.html',{'form1':form1, 'search1':search1, 'search2':search2},)

def about(request):





    return render(request, 'custom_scraper/about.html',{},)
