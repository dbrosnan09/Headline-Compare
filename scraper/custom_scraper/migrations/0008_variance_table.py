# Generated by Django 3.0.6 on 2020-07-29 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_scraper', '0007_superlative_table_word_sentiment'),
    ]

    operations = [
        migrations.CreateModel(
            name='variance_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('graphid', models.PositiveIntegerField()),
                ('date', models.DateTimeField()),
                ('newspaper', models.PositiveIntegerField()),
                ('news1', models.CharField(max_length=10)),
                ('news2', models.CharField(max_length=10)),
                ('word', models.CharField(max_length=100)),
                ('count', models.PositiveIntegerField()),
                ('sentiment', models.DecimalField(decimal_places=10, max_digits=12)),
            ],
        ),
    ]
