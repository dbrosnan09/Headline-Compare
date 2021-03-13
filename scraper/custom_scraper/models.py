from django.db import models
import datetime
from django.utils import timezone
from django import forms
# Create your models here.
class Headline(models.Model):
    headline = models.CharField(max_length=500)
    newspaper = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=1000)
    day_order = models.PositiveIntegerField()
    sentiment = models.DecimalField(max_digits=12, decimal_places=10)

    def __str__(self):
        return self.headline

class Photos(models.Model):
    newspaper = models.PositiveIntegerField()
    keyword = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.link

class word_sentiment(models.Model):
    date = models.DateTimeField(default=timezone.now)
    word = models.CharField(max_length=500)
    count = models.PositiveIntegerField()
    sentiment = models.DecimalField(max_digits=12, decimal_places=10)
    word_type = models.PositiveIntegerField()

    def __str__(self):
        return self.overall_word


class superlative_table(models.Model):
    graphid = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    newspaper = models.PositiveIntegerField()
    news1 = models.CharField(max_length=10)
    news2 = models.CharField(max_length=10)
    
    word = models.CharField(max_length=100)
    count = models.PositiveIntegerField()
    sentiment = models.DecimalField(max_digits=12, decimal_places=10)


    def __str__(self):
        return self.word


class variance_table(models.Model):
    
    graphid = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    variance_date = models.DateTimeField(null=True, blank=True)
    word = models.CharField(max_length=100)
    news1 = models.CharField(max_length=10)
    news2 = models.CharField(max_length=10)
    sentiment = models.DecimalField(max_digits=12, decimal_places=10)


    def __str__(self):
        return self.word

class variance_table_word(models.Model):
    
    graphid = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    word = models.CharField(max_length=100)
    count = models.PositiveIntegerField()
    news1 = models.CharField(max_length=10)
    news2 = models.CharField(max_length=10)
    sentiment = models.DecimalField(max_digits=12, decimal_places=10)
    
    
    


    def __str__(self):
        return self.word

class Headlinewrl(models.Model):
    headline = models.CharField(max_length=500)
    newspaper = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=1000)
    day_order = models.PositiveIntegerField()
    sentiment = models.DecimalField(max_digits=12, decimal_places=10)
    reading_level = models.DecimalField(max_digits=5, decimal_places=1)


class Headlinewc(models.Model):
    headline = models.CharField(max_length=500)
    newspaper = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=1000)
    day_order = models.PositiveIntegerField()
    sentiment = models.DecimalField(max_digits=12, decimal_places=10)
    reading_level = models.DecimalField(max_digits=5, decimal_places=1)
    headline_wc = models.PositiveIntegerField()

class word_count(models.Model):
    date = models.DateTimeField(default=timezone.now)
    word = models.CharField(max_length=500)
    nyt = models.PositiveIntegerField()
    bbc = models.PositiveIntegerField()
    fn = models.PositiveIntegerField()
    overall = models.PositiveIntegerField()
    


class cooc(models.Model):
    date = models.DateTimeField(default=timezone.now)
    base_word = models.CharField(max_length=500)
    co_word = models.CharField(max_length=500)
    newspaper = models.PositiveIntegerField()
    co_word_count = models.PositiveIntegerField()
    

class total_word_count(models.Model):
    date = models.DateTimeField(default=timezone.now)
    word = models.CharField(max_length=500)
    nyt = models.PositiveIntegerField()
    bbc = models.PositiveIntegerField()
    fn = models.PositiveIntegerField()
    overall = models.PositiveIntegerField()

class word_count_general(models.Model):
    date = models.DateTimeField(default=timezone.now)
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)
    word_count = models.PositiveIntegerField()

class style_wc(models.Model):
    date = models.DateTimeField(default=timezone.now)
    newspaper = models.PositiveIntegerField()
    awc = models.DecimalField(max_digits=12, decimal_places=4)
    ahrl = models.DecimalField(max_digits=12, decimal_places=4)
    percent_quest = models.DecimalField(max_digits=12, decimal_places=4)
    percent_exclam = models.DecimalField(max_digits=12, decimal_places=4)
    ahwl = models.DecimalField(max_digits=12, decimal_places=4)
    uw = models.DecimalField(max_digits=12, decimal_places=4)
    wd = models.DecimalField(max_digits=12, decimal_places=4)

class cooc_wc(models.Model):
    date = models.DateTimeField(default=timezone.now)
    newspaper = models.PositiveIntegerField()
    base_word = models.CharField(max_length=500)
    cooc = models.CharField(max_length=500)
    coocc = models.PositiveIntegerField()

class emotion(models.Model):
    date = models.DateTimeField(default=timezone.now)
    word = models.CharField(max_length=500)
    fear = models.PositiveIntegerField()
    anger = models.PositiveIntegerField()
    anticip = models.PositiveIntegerField()
    trust = models.PositiveIntegerField()
    surprise = models.PositiveIntegerField()
    positive = models.PositiveIntegerField()
    negative = models.PositiveIntegerField()
    sadness = models.PositiveIntegerField()
    disgust = models.PositiveIntegerField()
    joy = models.PositiveIntegerField()


class Headline_emotion(models.Model):
    headline = models.CharField(max_length=500)
    newspaper = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=1000)
    day_order = models.PositiveIntegerField()
    sentiment = models.DecimalField(max_digits=12, decimal_places=10)
    reading_level = models.DecimalField(max_digits=5, decimal_places=1)
    headline_wc = models.PositiveIntegerField()
    fear = models.PositiveIntegerField()
    anger = models.PositiveIntegerField()
    anticip = models.PositiveIntegerField()
    trust = models.PositiveIntegerField()
    surprise = models.PositiveIntegerField()
    positive = models.PositiveIntegerField()
    negative = models.PositiveIntegerField()
    sadness = models.PositiveIntegerField()
    disgust = models.PositiveIntegerField()
    joy = models.PositiveIntegerField()

class emotion_associated(models.Model):
    date = models.DateTimeField(default=timezone.now)
    newspaper = models.PositiveIntegerField()
    emotion = models.CharField(max_length=500)
    word = models.CharField(max_length=500)
    word_count = models.PositiveIntegerField()
    


    
class headline_tokenized(models.Model):
    headline_id = models.PositiveIntegerField()
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)



class tokenized_headlines(models.Model):
    headline_id = models.PositiveIntegerField()
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)

class headline_id_tokens(models.Model):
    headline_id = models.PositiveIntegerField()
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)

class hl_tokenized_id(models.Model):
    headline_id = models.PositiveIntegerField()
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)


class hl_tokens(models.Model):
    headline_id = models.PositiveIntegerField()
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=1000)
    day_order = models.PositiveIntegerField()


class hl_tokens_emotions(models.Model):
    headline_id = models.PositiveIntegerField()
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=1000)
    day_order = models.PositiveIntegerField()
    fear = models.PositiveIntegerField()
    anger = models.PositiveIntegerField()
    anticip = models.PositiveIntegerField()
    trust = models.PositiveIntegerField()
    surprise = models.PositiveIntegerField()
    positive = models.PositiveIntegerField()
    negative = models.PositiveIntegerField()
    sadness = models.PositiveIntegerField()
    disgust = models.PositiveIntegerField()
    joy = models.PositiveIntegerField()


class top_words_emotions(models.Model):
    date = models.DateTimeField(default=timezone.now)
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)
    fear = models.PositiveIntegerField()
    anger = models.PositiveIntegerField()
    anticip = models.PositiveIntegerField()
    trust = models.PositiveIntegerField()
    surprise = models.PositiveIntegerField()
    sadness = models.PositiveIntegerField()
    disgust = models.PositiveIntegerField()
    joy = models.PositiveIntegerField()
    fear_percent = models.DecimalField(max_digits=5, decimal_places=2)
    anger_percent = models.DecimalField(max_digits=5, decimal_places=2)
    anticip_percent = models.DecimalField(max_digits=5, decimal_places=2)
    trust_percent = models.DecimalField(max_digits=5, decimal_places=2)
    surprise_percent = models.DecimalField(max_digits=5, decimal_places=2)
    sadness_percent = models.DecimalField(max_digits=5, decimal_places=2)
    disgust_percent = models.DecimalField(max_digits=5, decimal_places=2)
    joy_percent = models.DecimalField(max_digits=5, decimal_places=2)


class top_words_emotions_tally(models.Model):
    date = models.DateTimeField(default=timezone.now)
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)
    fear = models.PositiveIntegerField()
    anger = models.PositiveIntegerField()
    anticip = models.PositiveIntegerField()
    trust = models.PositiveIntegerField()
    surprise = models.PositiveIntegerField()
    sadness = models.PositiveIntegerField()
    disgust = models.PositiveIntegerField()
    joy = models.PositiveIntegerField()

class top_words_emotions_percent(models.Model):
    date = models.DateTimeField(default=timezone.now)
    newspaper = models.PositiveIntegerField()
    word = models.CharField(max_length=500)
    fear_percent = models.DecimalField(max_digits=5, decimal_places=2)
    anger_percent = models.DecimalField(max_digits=5, decimal_places=2)
    anticip_percent = models.DecimalField(max_digits=5, decimal_places=2)
    trust_percent = models.DecimalField(max_digits=5, decimal_places=2)
    surprise_percent = models.DecimalField(max_digits=5, decimal_places=2)
    sadness_percent = models.DecimalField(max_digits=5, decimal_places=2)
    disgust_percent = models.DecimalField(max_digits=5, decimal_places=2)
    joy_percent = models.DecimalField(max_digits=5, decimal_places=2)

class html_cache(models.Model):
    date = models.DateTimeField(default=timezone.now)
    page_num = models.PositiveIntegerField()
    cache_html = models.TextField()
