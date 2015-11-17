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
from .isbn_list import isbns
@celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=1))
#def myfunc():
#    print 'periodic_task'
def flipkart():
	if len(isbn) == 10:
		f_link = "http://www.flipkart.com/search?q="+pyisbn.Isbn10(isbn).convert(code='978')
	else:
		f_link = "http://www.flipkart.com/search?q="+isbn
		
	f_link = f_link +"&affid=sriteja96" # Affliate ID
	br = mechanize.Browser()
	br.set_handle_robots(False)   # Ignore robots.txt
	br.set_handle_refresh(False)  
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	try:
		response = br.open(f_link)

	except Exception, e:
		f_title = "NA"
		f_price = "NA"
		f_author = "NA"
		f_img = "NA"
		f_desc = "NA"
		f_status = "error_connecting"
		flip_dict = {'name':f_title,'price':f_price,'author':f_author,'image_url':f_img,'desc':f_desc,'url':f_link, 'status':f_status}
		return json.dumps(flip_dict)
	f_soup = BeautifulSoup(response.read())
        for i in range(0,5):
            for na in f_soup.find_all('p',{'class':'review-userName'})[i+5]:
                n= f_soup.find_all('span',{'class':'review-text-short'})[i]
                username = na.string
                revtext = n.text
	f_title_temp =(f_soup.find(itemprop="name"))
	if(f_title_temp):
		f_title = f_title_temp.string

		f_price_temp = f_soup.find_all("span",class_="selling-price omniture-field")[0]
		if(f_price_temp):
			f_price=(f_price_temp.string).replace('Rs. ','')
		else:
			f_price="NA"

		f_author_temp = (f_soup.find_all(href=re.compile("/author/[\w\s,.$><?@#$%^&*()_:-]+"))[0])
		if(f_author_temp):
			f_author = f_author_temp.string
		else:
			f_author="NA"

		f_img_temp = (f_soup.find_all("img",class_="productImage  current")[0])['data-src']
		if(f_img_temp):
			f_img=f_img_temp
		else:
			f_img = "NA"

		f_desc_temp = f_soup.find_all("div",class_="description-text")

		if(f_desc_temp):
			f_desc = f_desc_temp[0].decode_contents(formatter="html")
			soup = BeautifulSoup(f_desc)
			f_desc = soup.get_text()
		else:
			f_desc="NA"

		f_status = "success"

	else:
		f_title = "NA"
		f_price = "NA"
		f_author = "NA"
		f_img = "NA"
		f_desc = "NA"
		f_status =  "invalid_isbn"

        flip_dict = {'name':f_title,'price':f_price,'author':f_author,'image_url':f_img,'desc':f_desc,'url':f_link,'status':f_status,'reviewUser':username,'review-short-text':revtext,}

	return json.dumps(flip_dict)

def amazon(isbn):
	# isbn = '9789380501932'
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
	a_class = a_soup.findAll('span',class_="price3P")
	if not a_class:
		return {'price':'NA','url':a_link}
	else:
		a_class = a_class[0]
		a_price = re.findall(r'</span> (.*?)</span>',str(a_class))[0]
        for na in a_soup.findAll('div',class_="a-section"):
             if not na:
                 return {'price':'NA','url':a_link,'review':'NA'}
             else:
                  review = na.text

        for title in a_soup.find_all('span',{'id':"productTitle"}):
             if not title:
                 return {'title':'N.A','price':'NA','url':a_link,'review':'NA'}
             else:
                 tit=title.text
        return json.dumps({'title':tit,'price':a_price.replace('.00',''),'url':a_link,'review':review.replace('\n','')})
