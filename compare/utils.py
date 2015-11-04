import urllib2
import selenium.webdriver as webdriver
import bs4 as bs
import pyisbn
import re
from bs4 import BeautifulSoup
import mechanize
import json

def paytm(isbn):
	if len(isbn) == 10:
		p_link = 'https://paytm.com/shop/search/?q='+pyisbn.Isbn10(isbn).convert(code='978')+'&sort_price=1'
	else:
		p_link = 'https://paytm.com/shop/search/?q='+isbn+'&sort_price=1'
	# print p_link
	driver = webdriver.PhantomJS('phantomjs',service_args=['--ssl-protocol=any'])
	# driver = webdriver.Firefox()
	try:
		driver.get(p_link)
		content = driver.page_source
	except:
		content = ''
		return {'price':'NA','url':p_link}
	# print content	
	driver.quit()
	soup = bs.BeautifulSoup(content)
	p_class = soup.findAll('span',class_="border-radius ng-binding")
	# print p_class
	if not p_class:
		return {'price':'NA','url':p_link}	
	else:
		p_class = p_class[0]
	try:
		p_price = re.findall(r'>Rs (.*?)</span>',str(p_class))[0]
		return {'price':p_price,'url':p_link}
	except Exception, e:
		return {'price':'NA','url':p_link}

def uread(isbn):
	if len(isbn) == 10:
		u_link = "http://www.uread.com/search-books/"+pyisbn.Isbn10(isbn).convert(code='978')
	else:
		u_link = "http://www.uread.com/search-books/"+isbn
	br = mechanize.Browser()
	#br.set_all_readonly(False)    # allow everything to be written to
	br.set_handle_robots(False)   # ignore robots
	br.set_handle_refresh(False)  # can sometimes hang without this
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]           # [('User-agent', 'Firefox')]
	try:
		response = br.open(u_link)
	except Exception, e:
		return {'price':'NA','url':u_link}
	u_soup = BeautifulSoup(response.read())
	u_tag = u_soup.select('#ctl00_phBody_ProductDetail_lblourPrice')
	if not u_tag:
		return {'price':'NA','url':u_link}
	else:
		u_tag = u_tag[0]
	try:
		u_price = re.findall(r'</span>(.*?)</label>',str(u_tag))[0]
	except Exception, e:
		return {'price':'NA','url':u_link}
	return {'price':u_price,'url':u_link}

def amazon(isbn):
	# isbn = '9789380501932' 
    if len(isbn) == 13:
        a_link = "http://www.amazon.in/dp/"+pyisbn.Isbn(isbn).convert(code='978')
    else:
        a_link = "http://www.amazon.in/dp/"+isbn
	br = mechanize.Browser()
	#br.set_all_readonly(False)    # allow everything to be written to
	br.set_handle_robots(False)   # ignore robots
	br.set_handle_refresh(False)  # can sometimes hang without this
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]           # [('User-agent', 'Firefox')]
	try:
		response = br.open(a_link)
	except Exception, e:
		return {'price':'NA','url':a_link}
	a_soup = BeautifulSoup(response.read())
	a_class = a_soup.findAll('span',class_="price3P")
	if not a_class:
		return {'price':'NA','url':a_link}
	else:
		a_class = a_class[0]
	try:
		a_price = re.findall(r'</span> (.*?)</span>',str(a_class))[0]
	except Exception, e:
		return {'price':'NA','url':a_link}
	return json.dumps({'price':a_price.replace('.00',''),'url':a_link});

def flipkart(isbn):

	# Getting the Source from the link
    import pdb; pdb.set_trace()

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
        return flip_dict

	#Creating the soup

	f_soup = BeautifulSoup(response.read())

	#Getting the data
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

	flip_dict = {'name':f_title,'price':f_price,'author':f_author,'image_url':f_img,'desc':f_desc,'url':f_link,'status':f_status}

	return flip_dict

def infibeam(isbn):
   # if len(isbn)==13:
	i_link = "http://www.infibeam.com/Books/search?q="+isbn
    #else:
	#i_link = "http://www.infibeam.com/Books/search?q="+pyisbn.Isbn10(isbn).convert(code='978')
	br = mechanize.Browser()
	#br.set_all_readonly(False)    # allow everything to be written to
	br.set_handle_robots(False)   # ignore robots
	br.set_handle_refresh(False)  # can sometimes hang without this
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]           # [('User-agent', 'Firefox')]
	#try:
	response = br.open(i_link)
	#except Exception, e:
            #return json.dumps({'url':i_link,'price':'N.A','title':'N.A','description':'N.A'})
	i_soup = BeautifulSoup(response.read(),"html.parser")
	i_class = i_soup.findAll('span',class_='final-price')
	if not i_class:
             return json.dumps({'url':i_link,'price':'N.A','title':'N.A','description':'N.A'})
	try:
	    i_price = re.findall(r'</span> (.*?)</span>',str(i_class))[0]
	except Exception, e:
		return json.dumps({'price':'NA','url':i_link})
        for names in i_soup.find_all('div',{'class':'title'}):
              if not names:
                  return {'price':'N.A','url':i_link}
              else:
                  title=names.text.replace("\n"," ")
        for desc in i_soup.find_all('div',{'class':'snippet hidden-xs'}):
             if not desc:
                 return json.dumps({'url':i_link,'price':'N.A','title':'N.A','description':'N.A'})
             else:
                 description=desc.text.replace('\n',' ')
        return json.dumps({'price':i_price,'url':i_link,'title':str(title),'Description':str(description)})
