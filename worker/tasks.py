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
from celery.task import task

#file = open('isbn_list.txt', 'r')
#isbns = file.readlines()
#isbns=[i.strip() for i in isbns ]
isbns=[
        "97801414396",
        "9780142000670",
        "9780142437179",
        "9780142437209",
        "9780143039648",
        "9780143058144",
        "9780143064329",
        "9780143333258",
        "9780143414971",
        "9780143423669",
        "9780143424635",
        "9780144001590",
        "9780300190526",
        "9780307265432",
        "9780307269751",
        "9780307720740",
        "9780307743657",
        "9780307743671",
        "9780312997144",
        "9780330517980",
        "9780340977187",
        "9780349138978",
        "9780375751516",
        "9780375831003",
        "9780385333849",
        "9780399155345",
        "9780439023498",
        "9780439023511",
        "9780439139601",
        "9780439358071",
        "9780439655484",
        "9780439785969",
        "9780525478812",
        "9780552169592",
        "9780552170154",
        "9780553588484",
        "9780593072493",
        "9780618346257",
        "9780670086290",
        "9780670086740",
        "9780670087235",
        "9780670087709",
        "9780671041786",
        "9780684830490",
        "9780684833392",
        "9780753541630",
        "9781400032716",
        "9781408704035",
        "9781408853917",
        "9781411469433",
        "9781411469471",
        "9781416524793",
        "9781439192399",
        "9781444712568",
        "9781444723496",
        "9781444723601",
        "9781444727296",
        "9781444731705",
        "9781444789171",
        "9781447268659",
        "9781451658910",
        "9781476754451",
        "9781781162644",
        "9781846147890",
        "9788129113726",
        "9788129123961",
        "9788129124937",
        "978812913552",
        "9788170289111",
        "9788170944935",
        "9788172235307",
        "9788172235390",
        "9788172236298",
        "9788173711466",
        "9788174364449",
        "9788174367082",
        "9788174368942",
        "9788174369383",
        "9788176253437",
        "9788176254151",
        "9788179922231",
        "9788180900310",
        "9788184006094",
        "9788185986241",
        "9788186050828",
        "9788186050880",
        "9788186050897",
        "9788186050941",
        "9788192683508",
        "9789350095836",
        "9789350295441",
        "9789351160090",
        "9789351374770",
        "9789380283777",
        "9789380349305",
        "9789381398517",
        "9789381398548",
        "9789381506431",
        "9789381576052",
        "9789381841167",
        "9789382618348",
        "9789382711476",
        "9789382951001",
        "9789383064755",
        "9789383074846",
        "9789383134403",
        "9789383260126",
        "9789385152146",
        "0060929871",
        "0061120081",
        "0061122416",
        "0140283331",
        "0141345659",
        "0307277674",
        "0316769177",
        "0439023483",
        "0439064864",
        "0439554934",
        "0452284244",
        "0618260307",
        "0679720200",
        "0679783261",
        "0743273567",
        "0751563587",
        "1408701618",
        "1408704005",
        "1473623650",
        "1594480001",
        "789385152146",
        "8129108186",
        "8129115301",
        "8129118807",
        "8129135728",
        "8812910459",
        "9780007490622",
        "9780007491568",
        "9780007520503",
        "9780007773589",
        "9780099282280",
        "9780099586395",
        "9780140107913",
        "9780140236705",
        "9780140298857",
        "9780141439471"
        ]

def flipkart(isbn):
    print "I am in flipkart"
    try:
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
        flip_dict = {'website_name':"flipkart.com",'isbn_number':isbn,'name':f_title,'price':f_price,'author':f_author,'image_url':f_img,'description':f_desc,'url':f_link,'reviews':review_list,'status':1}
        return flip_dict
    except:
        return {'status':0}

def amazon(isbn):
    print "I am in amazon"
    try:
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

        return {'website_name':"amazon.com",'isbn_number':isbn, 'price':a_price,'url':a_link,'status':1}
    except:
        return {'status':0}

def sentiment_analysis(isbn):
    sent_file = open("AFINN-111.txt","r")
    scores ={}
    product=Product.objects.filter(isbn_number=isbn)[0]
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)
    reviews_data=product.p_reviews.all()
    count = 0
    sentiment_rating = 0
    for review in reviews_data:
            count += 1
            terms = review.inside_text.split()
            score = 0
            term_count = 0
            for term in terms:
                if term in scores:
                    score += scores[term]
                    term_count += 1
            try:
                score = score/term_count
            except:
                score = 0
            sentiment_rating += score
    try:
        sentiment_rating = sentiment_rating/count
    except:
        sentiment_rating = 0
    obj=product.available.filter(name="flipkart.com")
    if obj:
        obj[0].sentiment_rating=sentiment_rating
        obj[0].save()
    else:
        return False
    sent_file.close()
    return True


@task(ignore_result=True, max_retries=1, default_retry_delay=10)
def main():
    for d in isbns:
        f_data=flipkart(d)
        a_data=amazon(d)
        if f_data['status']*a_data['status']==0:
            continue
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
        status=sentiment_analysis(f_data['isbn_number'])
    return True
