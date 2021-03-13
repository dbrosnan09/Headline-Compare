from django import forms

class WordCountSearch(forms.Form):
    word_count = forms.CharField(label='',max_length=120, widget=forms.TextInput(attrs={'placeholder':'Search Headlines'}))

class SentimentWordSearch(forms.Form):
    sentiment_word_search = forms.CharField(max_length=120, label = '', widget=forms.TextInput(attrs={'placeholder':'Enter Search Term Here'}))

class SentimentDateSearch(forms.Form):
    sentiment_date_search = forms.DateField(label = '', widget=forms.TextInput(attrs={'placeholder':'Enter Date Here'}))

class DateForm(forms.Form):
    date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'placeholder':'Enter Date'}))

class CompareSearch1(forms.Form):
    compare1 = forms.CharField(label='',max_length=120, widget=forms.TextInput(attrs={'placeholder':'First Term'}))
    compare2 = forms.CharField(label='',max_length=120, widget=forms.TextInput(attrs={'placeholder':'Second Term'})) 

class CompareSearch2(forms.Form):
    compare2 = forms.CharField(label='',max_length=120, widget=forms.TextInput(attrs={'placeholder':'Second Term'}))

class CompareSearchSingle(forms.Form):
    compare1 = forms.CharField(label='',max_length=120, widget=forms.TextInput(attrs={'placeholder':'Enter Term'}))
