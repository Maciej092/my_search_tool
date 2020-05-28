import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models


BASE         = 'https://www.gumtree.pl{}'
BASE_URL     = 'https://www.gumtree.pl/s-krakow/v1l3200208p1?q={}'
BASE_IMG_URL = 'https://i.ebayimg.com/images/g/{}/s-l140.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response  = requests.get(final_url)
    data      = response.text
    soup      = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('div', {'class': 'tileV1'})
    print(post_listings)
    final_postings = []

    for post in post_listings:

        post_titles = post.find(class_='tile-title-text').text
        post_url    = post.find('a').get('href')
        post_url    = BASE.format(post_url)

        if post.find(class_='ad-price'):
            post_price  = post.find(class_='ad-price').text
        else:
            post_price  = 'N/A'

        if post.img:
            post_image_url = post.img['data-src']
        else:
            post_image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1200px-No_image_available.svg.png'

        final_postings.append((post_titles, post_url, post_price, post_image_url))

    to_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', to_frontend)
