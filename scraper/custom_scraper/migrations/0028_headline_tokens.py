# Generated by Django 3.0.6 on 2020-11-11 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_scraper', '0027_emotion_associated'),
    ]

    operations = [
        migrations.CreateModel(
            name='headline_tokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline_id', models.PositiveIntegerField()),
                ('word', models.CharField(max_length=500)),
            ],
        ),
    ]
