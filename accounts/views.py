# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, FormView

from accounts.forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    form_class = RegisterForm
    model = User
    template_name = 'user/register.hdt'

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        user = authenticate(
            username=form.save(commit=False).username,
            password=form.clean_password2()
        )
        login(self.request, user)
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)


class LoginView(FormView):
    form_class = LoginForm
    model = User
    template_name = 'user/login.hdt'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

def logout(request):
    if request.user.is_authenticated():
        user_logout(request)
    return redirect('/')
