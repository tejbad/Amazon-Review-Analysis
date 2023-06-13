from bs4 import BeautifulSoup
import pandas as pd
from django.shortcuts import render
# from django.conf import settings
# from .models import Data
import json
import requests
from Analysis.views import analysis
    

def scrap_data(request,user_agent,path,pages=5):
    reviewlist = []
    headers = {
        "User-Agent": user_agent}
    def get_soup(url):
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_reviews(soup):
        reviews = soup.find_all('div', {'data-hook': 'review'})
        try:
            for item in reviews:
                review = {
                    'product': soup.title.text.replace('Amazon.co.uk:Customer reviews:', '').strip(),
                    'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                    'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                    'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                }
                reviewlist.append(review)
        except:
            pass


    for x in range(1, pages):
        if '?' in path:
            soup = get_soup(f''+path+'&reviewerType=all_reviews&pageNumber={}'.format(x))
        else:
            soup = get_soup(f''+path+'?reviewerType=all_reviews&pageNumber={}'.format(x))

        print(f'Getting page: {x}')
        get_reviews(soup)
        # print(len(reviewlist))
        if not soup.find('li', {'class': 'a-disabled a-last'}):
            pass
        else:
            break
            
    df = pd.DataFrame(reviewlist)
    json_records = df.reset_index().to_json(orient ='records')
    data = json.loads(json_records)
    

    return data

import re

NON_ALPHANUM = re.compile(r'[\W]')
NON_ASCII = re.compile(r'[^a-z0-1\s]')

# Removing any data other than text
def normalize_texts(data):
    normalized_texts = []
    for i in data:        
        lower = i["body"].lower()
        no_punctuation = NON_ALPHANUM.sub(r' ', lower)
        no_non_ascii = NON_ASCII.sub(r'', no_punctuation)
        i["body"] = no_non_ascii
    return data


def index(request):
    if request.method == "POST":
        user_agent = request.POST.get('user_agent')
        path = request.POST.get('review_path')
        pages = int(request.POST.get('pages'))+1
        data = scrap_data(request,user_agent,path,pages)
        if data:
            data = normalize_texts(data)
        else:
            return render(request, 'index.html',{'msg':"Wrong Link"})    
        data, result , chart_data = analysis(data)
        return render(request, 'index.html', {'data': data,'result':result,'chart_data':chart_data})
    return render(request,'index.html')


