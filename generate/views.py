from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import cloudinary.uploader
from PIL import Image
from io import BytesIO
from django.contrib.staticfiles.storage import staticfiles_storage
from PIL import Image, ImageDraw, ImageFont
from django.urls import reverse
import os
from dotenv import load_dotenv

load_dotenv(override=True)

OZON_CLIENT_ID = os.getenv("OZON_CLIENT_ID")
OZON_API_KEY = os.getenv("OZON_API_KEY")
PHOTOROOM_API_KEY = os.getenv("PHOTOROOM_API_KEY")
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


def index(request, item_id):
    data = {}
    data['good'] = get_good_info(item_id)
    if f"product_{item_id}" in request.session:
        data['good']['image'] = request.session[f"product_{item_id}"]

    return render(request, 'generate/index.html', data)


@csrf_exempt
def save_image(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        image_url = data.get('image_url')

        endpoint = 'v1/product/pictures/import'

        data = get_good_info(item_id)
        if f"product_{item_id}" in request.session:
            data['images'][request.session[f"position_{item_id}"]] = image_url
        else:
            data['images'] += [image_url]

        payload = {
            "images": data['images'],
            "product_id": item_id,
        }

        requests.post(host + endpoint, headers=headers_ozon, json=payload)

        redirect_url = reverse('sku', args=(item_id,))
        return JsonResponse({'redirect_url': redirect_url})

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


def get_good_info(product_id):
    endpoint = 'v2/product/info'

    payload = {
        "offer_id": "",
        "product_id": product_id,
        "sku": 0
    }

    info = requests.post(host + endpoint, headers=headers_ozon, json=payload)
    info = info.json()
    result = {'id': product_id, 'name': info['result']['name'], 'image': info['result']['primary_image'],
              'images': [info['result']['primary_image']] + info['result']['images']}
    return result


@csrf_exempt
def generate_image(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        image_url = data.get('image_url')
        text = data.get('prompt')

        url = "https://beta-sdk.photoroom.com/v2/edit"
        querystring = {
            "imageUrl": image_url,
            "background.prompt": text,
            "background.seed": "1000"
        }
        headers = {
            "Accept": "image/jpg, application/json",
            "x-api-key": PHOTOROOM_API_KEY
        }

        # Отправляем запрос и получаем ответ
        response = requests.get(url, headers=headers, params=querystring)
        upload_result = cloudinary.uploader.upload(response.content)
        uploaded_image_url = upload_result['secure_url']

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Возвращаем сгенерированное изображение
            return JsonResponse({'generated_image': uploaded_image_url})
        else:
            return JsonResponse({'error': 'Ошибка при запросе к API'}, status=500)
    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


@csrf_exempt
def flip_image(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        image_url = data.get('image_url')

        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            image = image.convert("RGB")

            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)

            # Создаем буфер для хранения данных изображения
            buffer = BytesIO()
            flipped_image.save(buffer, format='JPEG')
            buffer.seek(0)

            # Загружаем отраженное изображение на Cloudinary
            upload_result = cloudinary.uploader.upload(buffer)
            uploaded_image_url = upload_result['secure_url']

            return JsonResponse({'generated_image': uploaded_image_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


@csrf_exempt
def add_text(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        image_url = data.get('image_url')
        font_name = data.get('font_name')
        color = data.get('color')
        font_size = int(data.get('font_size'))
        placement = data.get('placement')  # Преобразуем строку в кортеж
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            image = image.convert("RGB")
            font_path = staticfiles_storage.path(f'generate/{font_name}')
            font = ImageFont.truetype(font_path, font_size)

            draw = ImageDraw.Draw(image)

            text = data.get('text')
            draw.text(placement, text, fill=color, font=font)

            # Сохраняем изображение в буфер
            buffer = BytesIO()
            image.save(buffer, format='JPEG')
            buffer.seek(0)

            upload_result = cloudinary.uploader.upload(buffer)
            uploaded_image_url = upload_result['secure_url']

            return JsonResponse({'generated_image': uploaded_image_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
