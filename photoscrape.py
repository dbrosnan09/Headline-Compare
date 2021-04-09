#!/usr/bin/env python

import os
import sys
import django

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/scraper/')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()
from custom_scraper.models import Headline
from custom_scraper.models import Headline_photo

from datetime import datetime
from datetime import date, timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)
today = str(today)[:10]
yesterday = str(yesterday)[:10]




from requests_html import HTMLSession



def nyt_hl_photo_link(hl_link):


    session = HTMLSession()




    google_image_search_url = 'https://www.google.com/search?q=' + hl_link + '&tbm=isch'

    r = session.get(google_image_search_url)


    img_search_html = r.text


    image_start_index = img_search_html.find("static01") - 8

    img_link_chunk = img_search_html[image_start_index:image_start_index+1000]

    jpg_check = img_link_chunk.find(".jpg")
    png_check = img_link_chunk.find(".png")

    print(jpg_check)
    print(png_check)

    if jpg_check < png_check:
        img_link_end = jpg_check

    if png_check < jpg_check:
        img_link_end = png_check

    if jpg_check == -1:
        img_link_end = png_check

    if png_check == -1:
        img_link_end = jpg_check

    if png_check == -1 and jpg_check == -1:
        image_start_index = img_search_html.find("static01") - 8
        img_search_html = img_search_html[image_start_index+50]
        image_start_index = img_search_html.find("static01") - 8
        print("got here")
        img_link_chunk = img_search_html[image_start_index:image_start_index+1000]

        jpg_check = img_link_chunk.find(".jpg")
        png_check = img_link_chunk.find(".png")

        print(jpg_check)
        print(png_check)

        if jpg_check < png_check:
            img_link_end = jpg_check

        if png_check < jpg_check:
            img_link_end = png_check

        if jpg_check == -1:
            img_link_end = png_check

        if png_check == -1:
            img_link_end = jpg_check

        if jpg_check == -1 and png_check == -1:


            session = HTMLSession()




            google_image_search_url = 'https://www.google.com/search?q=' + headline_record.headline + '&tbm=isch'

            r = session.get(google_image_search_url)



            img_search_html = r.text

            image_start_index = img_search_html.find("static01") - 8

            img_link_chunk = img_search_html[image_start_index:image_start_index+1000]

            jpg_check = img_link_chunk.find(".jpg")
            png_check = img_link_chunk.find(".png")

            print(jpg_check)
            print(png_check)

            if jpg_check < png_check:
                img_link_end = jpg_check

            if png_check < jpg_check:
                img_link_end = png_check

            if jpg_check == -1:
                img_link_end = png_check

            if png_check == -1:
                img_link_end = jpg_check

            if jpg_check == -1 and png_check == -1:
                print("Oh noooooooo no picture found for this nyt headline!")
                return "https://static01.nyt.com/images/2015/02/06/admin/the-new-york-times-masthead-1423244159624/the-new-york-times-masthead-1423244159624-facebookJumbo.png"



    print(img_link_chunk[:img_link_end+4])
    return img_link_chunk[:img_link_end+4]


todays_nyt_hls = Headline.objects.filter(date__icontains=today).filter(newspaper=1).order_by('day_order')

for headline_record in todays_nyt_hls:
    nyt_img_url = nyt_hl_photo_link(headline_record.link)

    nytimes_img = Headline_photo(newspaper=headline_record.newspaper,day_order=headline_record.day_order, headline_link=headline_record.link, img_link=nyt_img_url)
    nytimes_img.save()



def bbc_hl_photo_link(hl_link):


    session = HTMLSession()




    google_image_search_url = 'https://www.google.com/search?q=' + hl_link + '&tbm=isch'

    r = session.get(google_image_search_url)



    img_search_html = r.text

    image_start_index = img_search_html.find("ichef")

    img_link_chunk = img_search_html[image_start_index:image_start_index+1000]

    jpg_check = img_link_chunk.find(".jpg")
    png_check = img_link_chunk.find(".png")

    print(jpg_check)
    print(png_check)
    print(img_link_chunk)
    if jpg_check < png_check:
        img_link_end = jpg_check

    if png_check < jpg_check:
        img_link_end = png_check

    if jpg_check == -1:
        img_link_end = png_check

    if png_check == -1:
        img_link_end = jpg_check

    if png_check == -1 and jpg_check == -1:
        image_start_index = img_search_html.find("ichef")
        img_search_html = img_search_html[image_start_index+50]
        image_start_index = img_search_html.find("ichef")

        img_link_chunk = img_search_html[image_start_index:image_start_index+1000]
        print(img_link_chunk)
        jpg_check = img_link_chunk.find(".jpg")
        png_check = img_link_chunk.find(".png")

        print(jpg_check)
        print(png_check)

        if jpg_check < png_check:
            img_link_end = jpg_check

        if png_check < jpg_check:
            img_link_end = png_check

        if jpg_check == -1:
            img_link_end = png_check

        if png_check == -1:
            img_link_end = jpg_check

        if png_check == -1 and jpg_check == -1:

                session = HTMLSession()




                google_image_search_url = 'https://www.google.com/search?q=' + headline_record.headline + '&tbm=isch'

                r = session.get(google_image_search_url)



                img_search_html = r.text

                image_start_index = img_search_html.find("ichef")

                img_link_chunk = img_search_html[image_start_index:image_start_index+1000]

                jpg_check = img_link_chunk.find(".jpg")
                png_check = img_link_chunk.find(".png")

                print(jpg_check)
                print(png_check)
                print(img_link_chunk)
                if jpg_check < png_check:
                    img_link_end = jpg_check

                if png_check < jpg_check:
                    img_link_end = png_check

                if jpg_check == -1:
                    img_link_end = png_check

                if png_check == -1:
                    img_link_end = jpg_check

                if png_check == -1 and jpg_check == -1:
                    print("OOhhhhh nOoooooooo no photo for this headline for bbc news")
                    return "https://m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/5.1.0/bbc_news_logo.png"

    print(img_link_chunk[:img_link_end+4])
    return "https://" + img_link_chunk[:img_link_end+4]




todays_bbc_hls = Headline.objects.filter(date__icontains=today).filter(newspaper=2).order_by('day_order')

for headline_record in todays_bbc_hls:
    bbc_img_url = bbc_hl_photo_link(headline_record.link)


    bbc_img = Headline_photo(newspaper=headline_record.newspaper,day_order=headline_record.day_order, headline_link=headline_record.link, img_link=bbc_img_url)
    bbc_img.save()




def fn_hl_photo_link(hl_link):


    session = HTMLSession()

    if "video.foxnews.com" in hl_link:

        google_image_search_url = 'https://www.google.com/search?q=' + hl_link + '&tbm=isch'

        r = session.get(google_image_search_url)



        img_search_html = r.text

        image_start_index = img_search_html.find("https://cf-images")


        img_link_chunk = img_search_html[image_start_index:image_start_index+1000]
        print(img_link_chunk)
        jpg_check = img_link_chunk.find(".jpg")
        png_check = img_link_chunk.find(".png")

        print(jpg_check)
        print(png_check)

        if jpg_check < png_check:
            img_link_end = jpg_check

        if png_check < jpg_check:
            img_link_end = png_check

        if jpg_check == -1:
            img_link_end = png_check

        if png_check == -1:
            img_link_end = jpg_check

        if png_check == -1 and jpg_check == -1:
            image_start_index = img_search_html.find("https://cf-images")
            img_search_html = img_search_html[image_start_index+50]
            image_start_index = img_search_html.find("https://cf-images")

            img_link_chunk = img_search_html[image_start_index:image_start_index+1000]
            print(img_link_chunk)
            jpg_check = img_link_chunk.find(".jpg")
            png_check = img_link_chunk.find(".png")

            print(jpg_check)
            print(png_check)

            if jpg_check < png_check:
                img_link_end = jpg_check

            if png_check < jpg_check:
                img_link_end = png_check

            if jpg_check == -1:
                img_link_end = png_check

            if png_check == -1:
                img_link_end = jpg_check

            if png_check == -1 and jpg_check == -1:
                google_image_search_url = 'https://www.google.com/search?q=' + headline_record.headline + '&tbm=isch'

                r = session.get(google_image_search_url)



                img_search_html = r.text

                image_start_index = img_search_html.find("https://cf-images")


                img_link_chunk = img_search_html[image_start_index:image_start_index+1000]
                print(img_link_chunk)
                jpg_check = img_link_chunk.find(".jpg")
                png_check = img_link_chunk.find(".png")

                print(jpg_check)
                print(png_check)

                if jpg_check < png_check:
                    img_link_end = jpg_check

                if png_check < jpg_check:
                    img_link_end = png_check

                if jpg_check == -1:
                    img_link_end = png_check

                if png_check == -1:
                    img_link_end = jpg_check

                if png_check == -1 and jpg_check  == -1:
                    google_image_search_url = 'https://www.google.com/search?q=' + headline_record.headline + '&tbm=isch'

                    r = session.get(google_image_search_url)

                    r.html.render()

                    img_search_html = r.html.text

                    image_start_index = img_search_html.find("https://a57.foxnews")


                    img_link_chunk = img_search_html[image_start_index:image_start_index+1000]
                    print(img_link_chunk)
                    jpg_check = img_link_chunk.find(".jpg")
                    png_check = img_link_chunk.find(".png")

                    print(jpg_check)
                    print(png_check)

                    if jpg_check < png_check:
                        img_link_end = jpg_check

                    if png_check < jpg_check:
                        img_link_end = png_check

                    if jpg_check == -1:
                        img_link_end = png_check

                    if png_check == -1:
                        img_link_end = jpg_check

                    if png_check == -1 and jpg_check == 1:
                        print("oohh noo can't find fox news photo for this headline")
                        return "https://theme.zdassets.com/theme_assets/63348/e7cb70c951f61aabc336eb96db1f6e7788f9241e.png"



        print(img_link_chunk[:img_link_end+4])
        return img_link_chunk[:img_link_end+4]



    else:
        google_image_search_url = 'https://www.google.com/search?q=' + hl_link + '&tbm=isch'

        r = session.get(google_image_search_url)



        img_search_html = r.text

        image_start_index = img_search_html.find("https://a57.foxnews")


        img_link_chunk = img_search_html[image_start_index:image_start_index+1000]
        print(img_link_chunk)
        jpg_check = img_link_chunk.find(".jpg")
        png_check = img_link_chunk.find(".png")

        print(jpg_check)
        print(png_check)

        if jpg_check < png_check:
            img_link_end = jpg_check

        if png_check < jpg_check:
            img_link_end = png_check

        if jpg_check == -1:
            img_link_end = png_check

        if png_check == -1:
            img_link_end = jpg_check

        if png_check == -1 and jpg_check == 1:
            image_start_index = img_search_html.find("https://a57.foxnews")
            img_search_html = img_search_html[image_start_index+50]
            image_start_index = img_search_html.find("https://a57.foxnews")

            img_link_chunk = img_search_html[image_start_index:image_start_index+1000]
            print(img_link_chunk)
            jpg_check = img_link_chunk.find(".jpg")
            png_check = img_link_chunk.find(".png")

            print(jpg_check)
            print(png_check)

            if jpg_check < png_check:
                img_link_end = jpg_check

            if png_check < jpg_check:
                img_link_end = png_check

            if jpg_check == -1:
                img_link_end = png_check

            if png_check == -1:
                img_link_end = jpg_check


        print(img_link_chunk[:img_link_end+4])
        return img_link_chunk[:img_link_end+4]




todays_fn_hls = Headline.objects.filter(date__icontains=today).filter(newspaper=3).order_by('day_order')

for headline_record in todays_fn_hls:
    fn_img_url = fn_hl_photo_link(headline_record.link)


    fn_img = Headline_photo(newspaper=headline_record.newspaper,day_order=headline_record.day_order, headline_link=headline_record.link, img_link=fn_img_url)
    fn_img.save()


