#non-db code for word_count_general_db page
def word_count_general_db(request):
    today = date.today() 
    yesterday = date.today() - timedelta(days=1)

    today_headline_check = Headline.objects.filter(date__contains=today).values('headline')
    if not today_headline_check:
        today = yesterday
    print(today)
    import plotly.graph_objects as go

    terms = []
    ny_values_list = []
    bbc_values_list = []
    fn_values_list = []

    overall_terms = word_count_general.objects.filter(date__contains=today).filter(newspaper=4).values('word','word_count')
    for i in overall_terms[:9]:
        print(i)
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

    print(terms)
    print(ny_values_list)
    print(bbc_values_list)
    print(fn_values_list)

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

    print(len(base_words))
    
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
