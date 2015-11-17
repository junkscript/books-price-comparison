from django.shortcuts import render
from django.http import HttpResponse
import json
import time
from utils import get_query
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .models import ProductPhoto,Tag, Website, Product,Reviews

def home_page(request):
    return render(request,'home.html')

def paginate(posts, page_num=1):
    paginator = Paginator(posts, 10)
    try:
        page = int(page_num)
    except ValueError:
        page = 1
    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)
    return posts

def web_search(request):
    data = request.GET
    keyword = data["keyword"]
    try:
        page_num=data['page_num']
    except:
        page_num=1
    tagval = keyword.strip()
    tagval = str(tagval).split(" ")
    entry_query = get_query(keyword.strip(), ['name','description','isbn_number','available__name'])
    posts = Product.objects.filter(entry_query|Q(tags__name__in=tagval)).distinct().order_by('id').reverse()
    posts = paginate(posts, page_num)
    return render(request, 'blog/blog/index.html',{'data':posts})

def product_detail(request):
    data=request.GET
    product_info=Product.objects.filter(isbn_number=data)
    product_info.visit_count=product_info.visit_count+1
    product_info.save()
    return render(request,'detail.html',{'product_info':product_info})
