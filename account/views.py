from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import AccountForm
from .models import Users
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from account.models import Users
from math import ceil



@csrf_exempt
def index(request):
    if 'user_id' not in request.session:  # если пользователь не авторизован, отправляем на страницу входа
        return redirect('login')
    else:
        user = Users.objects.filter(id=request.session['user_id']).values()
        if len(user) == 0 or user[0]['status'] == 0:
            return redirect('logout')

    data = {}  # дата (данные), которая отправляется в view



    if 'deactivate-account' in request.POST:
        Users.objects.filter(id=request.session['user_id']).update(status=0)
        return redirect("account")
    if 'save_account_info' in request.POST:  # проверяем была ли нажата кнопочка с name = save_account_info в post запросе
        info = request.POST
        info_pic = AccountForm(request.POST, request.FILES)
        Users.objects.filter(id=request.session['user_id']).update(name=info['name'],
                                                                   client_id=info['client_id'],
                                                                   email=info['email'],
                                                                   api_key=info['api_key'])
        request.session['name'] = info['name']
        if info_pic.is_valid() and len(request.FILES) > 0:
            info_pic.save()
            profile_picture = Users.objects.latest('id').profile_picture
            Users.objects.latest('id').delete()
            Users.objects.filter(id=request.session['user_id']).update(profile_picture=profile_picture)
            request.session['avatar'] = Users.objects.filter(id=request.session['user_id']).values()[0][
                'profile_picture']

        return redirect("account")

    user = Users.objects.filter(
        id=request.session['user_id']).values()  # берем из accounts вссех юзеров с id равный id пользака из сессии
    form = AccountForm(data=user[0])  # указываем в data значение из базы, чтобы автоматом выставлялись в поля
    data['form'] = form

    data['profile_picture'] = user[0]['profile_picture']
    return render(request, 'account/index.html', data)


def logout(request):
    if 'user_id' in request.session.keys():
        del request.session['user_id']
    return redirect('home')
