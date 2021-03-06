# Generated by Django 3.0.6 on 2020-10-21 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_scraper', '0022_style_wc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style_wc',
            name='ahrl',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name='style_wc',
            name='ahwl',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name='style_wc',
            name='awc',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name='style_wc',
            name='percent_exclam',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name='style_wc',
            name='percent_quest',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name='style_wc',
            name='uw',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name='style_wc',
            name='wd',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
    ]
