# -*- coding: utf-8 -*-

from django.forms import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import UserProfile
from berfmk.forms import MyModelForm
from captcha.forms import ReCaptchaForm, ReCaptchaModelForm


class RegisterForm(UserCreationForm, ReCaptchaModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['required'] = ''

    def clean_username(self):
        username = super(RegisterForm, self).clean_username()
        if username and len(username) < 4:
            raise ValidationError(
                u'Длина логина не может быть меньше 4-х символов'
            )

    def clean_password2(self):
        password = super(RegisterForm, self).clean_password2()
        if password and len(password) < 6:
            raise ValidationError(
                u'В целях безопасности, длинна пароля не может быть меньше 6-и '
                u'символов'
            )
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email):
            raise ValidationError(u'Данный адрес уже используется')
        return email

    class Meta(object):
        model   = User
        fields  = ('username', 'email', )


class LoginForm(AuthenticationForm, ReCaptchaForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.error_messages['invalid_login'] = u"Введенные данные некорректны"

        for field in self.fields:
            self.fields[field].widget.attrs['required'] = ''

