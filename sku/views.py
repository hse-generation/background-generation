from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect
import cloudinary.uploader
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import os
from dotenv import load_dotenv

load_dotenv(override=True)

OZON_CLIENT_ID = os.getenv("OZON_CLIENT_ID")
OZON_API_KEY = os.getenv("OZON_API_KEY")

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

host = "https://api-seller.ozon.ru/"

headers_ozon = {
    'Content-Type': 'application/json',
    'Client-Id': OZON_CLIENT_ID,
    'Api-Key': OZON_API_KEY,
}

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

@csrf_exempt
def index(request, item_id):
    if request.method == 'POST' and request.FILES:
        # Получаем файл из запроса
        image_content = request.FILES['image_content']

        # Загружаем изображение на Cloudinary
        upload_result = cloudinary.uploader.upload(image_content)
        uploaded_image_url = upload_result['secure_url']

        # Сохраняем ссылку в сессии
        request.session[f"product_{item_id}"] = uploaded_image_url

        # Формируем URL для редиректа
        redirect_url = reverse('generate', args=(item_id,))
        return JsonResponse({'redirect_url': redirect_url})

    data = {'good': get_good_info(item_id)}
    return render(request, 'sku/index.html', data)


def edit_image(request, item_id):
    if request.method == 'POST':
        data = get_good_info(item_id)

        image_src = request.POST.get('image_src')
        image_position = data['images'].index(image_src)

        request.session[f"product_{item_id}"] = image_src
        request.session[f"position_{item_id}"] = image_position

        redirect_url = reverse('generate', args=(item_id,))

        return redirect(redirect_url)

    data = {'good': get_good_info(item_id)}
    return render(request, 'sku/index.html', data)


def get_good_info(product_id):
    endpoint = 'v2/product/info'
    payload = {
        "offer_id": "",
        "product_id": product_id,
        "sku": 0
    }

    info = requests.post(host + endpoint, headers=headers_ozon, json=payload)
    info = info.json()
    result = {'id': product_id, 'name': info['result']['name'], 'primary_image': info['result']['primary_image'],
              "description": 0, 'images': [info['result']['primary_image']] + info['result']['images']}

    payload = {
        "offer_id": "",
        "product_id": product_id,
    }
    endpoint = 'v1/product/info/description'
    info = requests.post(host + endpoint, headers=headers_ozon, json=payload)
    info = info.json()
    result['description'] = info['result']['description']
    return result
