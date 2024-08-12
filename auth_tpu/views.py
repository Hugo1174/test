from django.shortcuts import render
import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse

CLIENT_ID = '1080bf552459828267008fe12522455b'
CLIENT_SECRET = '3047ce1b23c12458345ab4bbd82a44e2'


def login(request):
    state = 'hello'  # Замените это на генерацию уникальной строки
    redirect_uri = 'http://localhost:8000/auth/callback'
    return redirect(f'https://oauth.tpu.ru/authorize?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&state={state}')


def callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Ошибка авторизации")

    # Получение access_token
    access_token_response = requests.post('https://oauth.tpu.ru/access_token', data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:8000/auth/callback',
        'code': code,
        'grant_type': 'authorization_code'
    })

    if access_token_response.status_code != 200:
        return HttpResponse("Ошибка получения access_token")

    token_data = access_token_response.json()
    access_token = token_data['access_token']

    # Запрос данных пользователя
    user_data_response = requests.get('https://api.tpu.ru/v2/auth/user', params={
        'apiKey': CLIENT_ID,
        'access_token': access_token,
    })

    if user_data_response.status_code != 200:
        return HttpResponse("Ошибка получения данных пользователя")

    user_data = user_data_response.json()
    # Здесь вы можете сохранить данные пользователя в сессии или базе данных

    return HttpResponse(f"Добро пожаловать, {user_data['lichnost']['imya']} {user_data['lichnost']['familiya']}!")


def logout(request):
    return redirect('https://oauth.tpu.ru/auth/logout?redirect=http://localhost:8000/')

# Create your views here.
