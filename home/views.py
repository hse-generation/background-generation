from django.shortcuts import render, redirect
from account.models import Users
from math import ceil
import requests

import os
from dotenv import load_dotenv

load_dotenv(override=True)

OZON_CLIENT_ID = os.getenv("OZON_CLIENT_ID")
OZON_API_KEY = os.getenv("OZON_API_KEY")
PHOTOROOM_API_KEY = os.getenv("PHOTOROOM_API_KEY")

host = "https://api-seller.ozon.ru/"


def index(request):
    data = {}

    if 'user_id' not in request.session:
        return redirect('login')

    if 'user_id' in request.session:
        account = Users.objects.filter(id=request.session['user_id']).first()
        if not account.client_id or not account.api_key:
            return redirect('account')

    goods_list = get_goods_list()
    goods = get_goods_info(goods_list)
    data['goods'] = goods
    return render(request, 'home/index.html', data)


def get_goods_info(goods_list):
    result = []
    for item in goods_list:
        host = "https://api-seller.ozon.ru/"
        endpoint = 'v2/product/info'
        headers = {
            'Content-Type': 'application/json',
            'Client-Id': OZON_CLIENT_ID,
            'Api-Key': OZON_API_KEY,
        }
        payload = {
            "offer_id": "",
            "product_id": item['product_id'],
            "sku": 0
        }
        info = requests.post(host + endpoint, headers=headers, json=payload)
        info = info.json()
        d = {'id': item['product_id'], 'name': info['result']['name'], 'primary_image': info['result']['primary_image']}
        sku = info['result']['sku']
        endpoint = 'v1/product/rating-by-sku'
        payload = {
            "skus": [info['result']['sku']]
        }
        info = requests.post(host + endpoint, headers=headers, json=payload)
        info = info.json()
        if sku:
            d['rating'] = info['products'][0]['rating']
            result.append(d)

    return result


def get_goods_list():
    host = "https://api-seller.ozon.ru/"
    endpoint = 'v2/product/list'
    headers = {
        'Content-Type': 'application/json',
        'Client-Id': OZON_CLIENT_ID,
        'Api-Key': OZON_API_KEY,
    }

    payload = {
        "last_id": "",
        "limit": 20
    }

    res = requests.post(host + endpoint, headers=headers, json=payload)
    res = res.json()
    return res['result']['items']


def sitemap(request):
    data = {}
    return render(request, 'sitemap.txt', data)
