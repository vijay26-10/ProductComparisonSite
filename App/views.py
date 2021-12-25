from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.utils import html
from .models import amazonProduct, flipkartProduct, search
import requests
from bs4 import BeautifulSoup
import lxml
from urllib.parse import urlencode
import csv
import os
import time
import pandas as pd
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def get_html_content(request):
    global list
    product = request.POST.get('product')
    product = product.replace(' ', '+')
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    api_key = 'Enter Scraper Api key'
    url = f'https://www.amazon.in/s?k={product}&ref=nb_sb_noss_1'
    print(url)
    params = {'api_key': api_key, 'url': url}
    try:
        html_content = session.get(
            'http://api.scraperapi.com/', params=urlencode(params)).text
    except requests.exceptions.ConnectionError:
        print("Error@@@@@@@@@@")
    return html_content

def get_html_contentflp(request):
    global list
    product = request.POST.get('product')
    product = product.replace(' ', '%20')
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    api_key = 'Enter Scraper api key'
    url = f'https://www.flipkart.com/search?q={product}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    print("flipakrt url:", url)
    params = {'api_key': api_key, 'url': url}
    try:
        html_content1 = session.get(
            'http://api.scraperapi.com/', params=urlencode(params)).text
    except requests.exceptions.ConnectionError:
        print("Error@@@@@@@@@@")
    return html_content1

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    Amazonlink = 'https://www.amazon.in'+atag.get('href')
    img = item.find('img', 's-image')['src']
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
        price = str(price)
        price = price.replace(',', '')
        price = price.replace('₹', '')
        price = int(float(price))
    except AttributeError:
        return
    result = (description, price, Amazonlink, img)
    return result

def flipkartextract(a):
    name = a.find('div', attrs={'class': '_4rR01T'})
    name = name.text
    price = a.find('div', attrs={'class': '_30jeq3 _1_WHN1'}).text
    price = str(price)
    price = price.replace(',', '')
    price = price.replace('₹', '')
    price = int(float(price))
    link = a.find('a', '_1fQZEK')['href']
    img = a.find('img', '_396cs4 _3exPp9')['src']
    flpresult = (name, price, link, img)
    return flpresult

def flipkartextract1(a):
    name1 = a.find('a', attrs={'class': 'IRpwTa'})
    name1 = name1.text
    price1 = a.find('div', attrs={'class': '_30jeq3'}).text
    price1 = str(price1)
    price1 = price1.replace(',', '')
    price1 = price1.replace('₹', '')
    price1 = int(float(price1))
    link1 = a.find('a', 'IRpwTa')['href']
    img1 = a.find('img', '_2r_T1I')['src']
    flpresult1 = (name1, price1, link1, img1)
    return flpresult1

def flipkartextract2(a):
    name2 = a.find('a', attrs={'class': 's1Q9rs'})
    name2 = name2.text
    price2 = a.find('div', attrs={'class': '_30jeq3'}).text
    price2 = str(price2)
    price2 = price2.replace(',', '')
    price2 = price2.replace('₹', '')
    price2 = int(float(price2))
    link2 = a.find('a', 's1Q9rs')['href']
    img2 = a.find('img', '_396cs4 _3exPp9')['src']
    flpresult2 = (name2, price2, link2, img2)
    return flpresult2

def flipkartextract3(a):
    name3 = a.find('a', attrs={'class': 'IRpwTa _2-ICcC'})
    name3 = name3.text
    price3 = a.find('div', attrs={'class': '_30jeq3'}).text
    price3 = str(price3)
    price3 = price3.replace(',', '')
    price3 = price3.replace('₹', '')
    price3 = int(float(price3))
    link3 = a.find('a', 'IRpwTa _2-ICcC')['href']
    img3 = a.find('img', '_2r_T1I')['alt src']
    flpresult3 = (name3, price3, link3, img3)
    return flpresult3

def AmazonScraper(request):
    if request.method == 'POST':
        product = request.POST['product']
        records = []
        Ar = get_html_content(request)
        amazonSoup = BeautifulSoup(Ar, "lxml")
        results = amazonSoup.find_all(
            'div', {'data-component-type': 's-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
            else:
                print('Append Failed')
        sortedrecords = sorted(records, key=lambda x: int(x[1]))
        if os.path.isfile('result1.csv'):
            os.remove('result1.csv')
            with open('result1.csv', 'w', newline='', encoding='utf-8')as f:
                writer = csv.writer(f)
                writer.writerow(['AmazonProductName', 'AmazonProductprice',
                                'AmazonProductlink', 'AmazonProductImg'])
                writer.writerows(sortedrecords)
        else:
            with open('result1.csv', 'w', newline='', encoding='utf-8')as f:
                writer = csv.writer(f)
                writer.writerow(['AmazonProductName', 'AmazonProductprice',
                                'AmazonProductlink', 'AmazonProductImg'])
                writer.writerows(sortedrecords)
        if os.path.isfile('result1.csv'):
            with open('result1.csv', 'r', encoding="utf8") as f:
                reader = csv.reader(f, delimiter=",")
                header = next(reader)
                for row in reader:
                    AmazonProductName = row[0]
                    AmazonProductprice = row[1]
                    AmazonProductlink = row[2]
                    AmazonProductImg = row[3]
                    new_product = amazonProduct(
                        amzProductName=AmazonProductName,
                        amzProductPrice=AmazonProductprice,
                        amzProductLink=AmazonProductlink,
                        amzImageLink=AmazonProductImg,
                    )
                    new_product.save()
        time.sleep(6)
        flprecords = []
        r = get_html_contentflp(request)
        flipkartSoup = BeautifulSoup(r, "lxml")
        flpresults = flipkartSoup.findAll('div', {'class': '_2kHMtA'})
        flpresults1 = flipkartSoup.findAll('div', {'class': '_1xHGtK _373qXS'})
        flpresults2 = flipkartSoup.findAll('div', {'class': '_4ddWXP'})
        flpresults3 = flipkartSoup.findAll('div', {'class': '_13oc-S'})
        if flpresults:
            for a in flpresults:
                flprecord = flipkartextract(a)
                if flprecord:
                    flprecords.append(flprecord)
                else:
                    print('Append Failed')
        elif flpresults1:
            for a in flpresults1:
                flprecord = flipkartextract1(a)
                if flprecord:
                    flprecords.append(flprecord)
                else:
                    print('Append Failed')
        elif flpresults2:
            for a in flpresults2:
                flprecord = flipkartextract2(a)
                if flprecord:
                    flprecords.append(flprecord)
                else:
                    print('Append Failed')
        elif flpresults3:
            for a in flpresults3:
                flprecord = flipkartextract3(a)
                if flprecord:
                    flprecords.append(flprecord)
                else:
                    print('Append Failed')
        else:
            print("Products Not found")
        sortedrecords1 = sorted(flprecords, key=lambda x: int(x[1]))
        if os.path.isfile('flipkartresult1.csv'):
            os.remove('result1.csv')
            with open('result1.csv', 'w', newline='', encoding='utf-8')as f:
                writer = csv.writer(f)
                writer.writerow(['FlipkartProductName', 'FlipkartProductPrice',
                                'FlipkartProductLink', 'FlipkartProductImg'])
                writer.writerows(sortedrecords1)
        else:
            with open('flipkartresult1.csv', 'w', newline='', encoding='utf-8')as f:
                writer = csv.writer(f)
                writer.writerow(['FlipkartProductName', 'FlipkartProductPrice',
                                'FlipkartProductLink', 'FlipkartProductImg'])
                writer.writerows(sortedrecords1)
        if os.path.isfile('flipkartresult1.csv'):
            with open('result1.csv', 'r', encoding="utf8") as f:
                reader = csv.reader(f, delimiter=",")
                header = next(reader)
                for row in reader:
                    FlipkartProductName = row[0]
                    FlipkartProductPrice = row[1]
                    FlipkartProductLink = row[2]
                    FlipkartProductImg = row[3]
                    new_product1 = flipkartProduct(
                        flpProductName=FlipkartProductName,
                        flpProductPrice=FlipkartProductPrice,
                        flpProducLink='https://www.flipkart.com'+FlipkartProductLink,
                        flpProductImg=FlipkartProductImg
                    )
                    new_product1.save()
                return redirect('fetchProducts')
        else:
            print("File not Present")
    return render(request, 'App/index.html')
def fetchProducts(request):
    records_list = "None"
    flprecords_list = "None"
    products = []
    if request.method == "GET":
        amzproductname = request.GET.get('search')
        emailId = request.GET.get('email')
        if amzproductname != '' and amzproductname is not None:
            lookup = (Q(amzProductName__icontains=amzproductname))
            lookup1 = (Q(flpProductName__icontains=amzproductname))
            records_list = amazonProduct.objects.filter(lookup)
            flprecords_list = flipkartProduct.objects.filter(lookup1)
            context1 = {
                'records_list': records_list,
                'flprecords_list': flprecords_list,
                'amzproductname': amzproductname,
            }
            html_content = render_to_string("App/product.html", context1)
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Products",
                text_content,
                settings.EMAIL_HOST_USER,
                [emailId]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            return render(request, 'App/product.html', context1)
        else:
            print('none')
    amzproduct = amazonProduct.objects.all()
    flpproduct = flipkartProduct.objects.all()
    context = {
        'amzproduct': amzproduct,
        'flpproduct': flpproduct
    }
    return render(request, 'App/fetch.html', context)

def delete(request):
    amzproduct = amazonProduct.objects.all()
    flpproduct = flipkartProduct.objects.all()
    amzproduct.delete()
    flpproduct.delete()
    return redirect('index')
