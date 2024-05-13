import hashlib
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .forms import RegistrationForm
from account.models import Users


def index(request):
    data = {}
    data['error'] = ""

    if request.method == 'POST': # получили Post запрос? срабатывает, когда нажимаем кнопку и в форму указан метод POST
        info = request.POST
        form = RegistrationForm(request.POST)
        data['error'] = form

        user = Users.objects.filter(email=info['email']).values()
        if len(user) > 0:
            data['error'] = "Пользователь с таким логином уже существует"
        elif form.is_valid():
            new_user = Users(email=info['email'], password=hashlib.md5(info['password'].encode()).hexdigest())
            new_user.save()
            user = Users.objects.filter(email=info['email']).values()
            request.session['user_id'] = user[0]['id']
            request.session['name'] = user[0]['name']
            request.session['avatar'] = user[0]['profile_picture']
            return redirect('home')

    data['title'] = 'Регистрация на сайте genme'

    form = RegistrationForm()
    data['form'] = form
    return render(request, 'register/index.html', data)
