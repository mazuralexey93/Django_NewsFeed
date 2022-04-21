import common.user_backend
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.urls import reverse
from authapp.models import User
from django.contrib import messages
from django.db import transaction
from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm

from ArticleFeed.settings import AUTHENTICATION_BACKENDS

def login(request, user=None):

    title = 'вход'
    login_form = UserLoginForm(data=request.POST)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():

        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        user = auth.authenticate(username=username, password=password)

        if user.activated:
            if user and user.is_active:
                auth.authenticate()
                auth.login(request, user, backend='common.user_backend.EmailBackend')
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('index'))

            messages.error(request, 'Аккаунт не активирован')


    context = {
        'title': title,
        'login_form': login_form,
        'next': next,
    }

    return render(request, 'authapp/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            messages.success(request, "E-mail с подтверждением отправлен на Вашу элетронную почту")
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = UserRegisterForm()

    context = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', context)

@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, instance=request.user)
        if edit_form.is_valid() :
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = UserEditForm(instance=request.user)


    content = {
        'title': title,
        'edit_form': edit_form,
    }

    return render(request, 'authapp/edit.html', content)

def activate(request, pk):
    user = User.objects.filter(activation_key=pk).first()
    if not user:
        return redirect('/404')
    if not user.is_activation_key_expired():
        user.activated = True
        user.save()
        messages.success(request, "Ваш аккаунт успешно активирован")
        return render(request, 'authapp/login.html')
    messages.error(request, "Данный ключ просрочен")
    return render(request, 'authapp/register.html')