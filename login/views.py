import hashlib
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .forms import LoginForm
from account.models import Users

def index(request):

    data = {'error': ""}
    if request.method == 'POST':
        info = request.POST
        form = LoginForm(request.POST)
        user = Users.objects.filter(email=info['email']).values()
        if form.is_valid() and len(user) > 0 and user[0]['status'] == 1 and user[0]['password'] == hashlib.md5(
                info['password'].encode()).hexdigest():
            request.session['user_id'] = user[0]['id']
            request.session['name'] = user[0]['name']
            request.session['api_key'] = user[0]['api_key']
            request.session['client_id'] = user[0]['client_id']
            request.session['avatar'] = user[0]['profile_picture']
            return redirect('home')
        else:
            data['error'] = "Неправильный логин или пароль"

    form = LoginForm()
    data['form'] = form

    return render(request, 'login/index.html', data)

