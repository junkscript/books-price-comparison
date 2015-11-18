import datetime
import celery
import urllib2
import selenium.webdriver as webdriver
import bs4 as bs
import pyisbn
import re
from bs4 import BeautifulSoup
import mechanize
import json
from webapp.celery import app
from compare.models import Product, Reviews, Website
import string

#file = open('isbn_list.txt', 'r')
#isbns = file.readlines()
#isbns=[i.strip() for i in isbns ]
isbns=[
        "9789385152146",
        "0141345659",
        "9788129135520"
        ]

def flipkart(isbn):
    if len(isbn) == 10:
        f_link = "http://www.flipkart.com/search?q="+pyisbn.Isbn10(isbn).convert(code='978')
    else:
        f_link = "http://www.flipkart.com/search?q="+isbn
    f_link = f_link +"&affid=sriteja96" # Affliate ID
    br = mechanize.Browser()
    br.set_handle_robots(False)   # Ignore robots.txt
    br.set_handle_refresh(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(f_link)
    f_soup = BeautifulSoup(response.read())
    reviews=f_soup.find_all("span",class_="review-text-full")
    review_list=[]
    for r in reviews:
        review_list.append(filter(lambda x: x in string.printable,r.text))
    f_title =f_soup.find(itemprop="name").text
    f_price =int(f_soup.find_all("span",class_="selling-price omniture-field")[0].text.replace("Rs.",""))
    f_author= f_soup.find_all(href=re.compile("/author/[\w\s,.$><?@#$%^&*()_:-]+"))[0].text
    f_img = f_soup.find_all("img",class_="productImage  current")[0]['data-src']
    try:
        f_desc = f_soup.find_all("div",class_="description-text")[0].text
    except:
        f_desc="Not available"
    flip_dict = {'website_name':"flipkart.com",'isbn_number':isbn,'name':f_title,'price':f_price,'author':f_author,'image_url':f_img,'description':f_desc,'url':f_link,'reviews':review_list}
    print "I am in flipkart"
    return flip_dict

def amazon(isbn):
    if len(isbn) == 13:
        a_link = "http://www.amazon.in/dp/"+pyisbn.Isbn(isbn).convert(code='978')
    else:
        a_link = "http://www.amazon.in/dp/"+isbn
    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]           # [('User-agent', 'Firefox')]

    response = br.open(a_link)
    a_soup = BeautifulSoup(response.read())
    a_price=int(a_soup.findAll('span',class_="price3P")[0].text.strip().replace(".00",""))
    print "I am in amazon"
    return {'website_name':"amazon.com",'isbn_number':isbn, 'price':a_price,'url':a_link}


@app.task
def main():
    for d in isbns:
        f_data=flipkart(d)
        a_data=amazon(d)
        product=Product.objects.filter(isbn_number=f_data['isbn_number'])
        if product:
            all_sites=product[0].available.all()
            for i in all_sites:
                if i.name=="amazon.com":
                    i.price=a_data['price']
                else:
                    i.price=f_data['price']
                i.save()
        else:
            product=Product(
                    name=f_data['name'],
                    author=f_data['author'],
                    description=f_data['description'],
                    image_url =f_data['image_url'],
                    isbn_number=f_data['isbn_number']
                    )
            product.save()
            avl_sites=[Website.objects.create(name=i['website_name'],product_url=i['url'],price=i['price']) for i in [f_data, a_data]]
            product.available.add(*avl_sites)
            product.save()
            for i in f_data['reviews']:
                Reviews.objects.create(inside_text=i,product=product)
    return True
