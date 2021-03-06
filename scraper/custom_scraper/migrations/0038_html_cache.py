# Generated by Django 3.0.6 on 2021-02-18 09:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('custom_scraper', '0037_top_words_emotions_percent_top_words_emotions_tally'),
    ]

    operations = [
        migrations.CreateModel(
            name='html_cache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('page_num', models.PositiveIntegerField()),
                ('cache_html', models.TextField()),
            ],
        ),
    ]
