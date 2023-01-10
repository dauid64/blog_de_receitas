from django.shortcuts import render, redirect
from authors.forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from django.utils.translation import gettext as _


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create')
        })


def register_create(request):
    if not request.POST:
        raise Http404
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        msg_translate = _('Your user is created, please log in.')
        messages.success(request, msg_translate)
        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            msg_transalte = _('Your are logged in.')
            messages.success(request, msg_transalte)
            login(request, authenticated_user)
        else:
            msg_transalte = _('Invalid credentials')
            messages.error(request, msg_transalte)
    else:
        msg_transalte = _('Invalid username or password')
        messages.error(request, msg_transalte)

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        msg_translate = _('Invalid logout request')
        messages.error(request, msg_translate)
        return redirect(reverse('authors:login'))
    if request.POST.get('username') != request.user.username:
        msg_translate = _('Invalid Logout user')
        messages.error(request, msg_translate)
        return redirect(reverse('authors:login'))
    msg_translate = _('Logged out successfully')
    messages.success(request, msg_translate)
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(request, 'authors/pages/dashboard.html', context={
        'recipes': recipes,
    }
    )
