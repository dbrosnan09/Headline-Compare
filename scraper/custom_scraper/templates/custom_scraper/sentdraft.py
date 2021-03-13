from django.db.models import Avg
    import plotly.express as px
    import plotly
    from django.db.models import Count
    
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
    print(best3_nyt[0][1])