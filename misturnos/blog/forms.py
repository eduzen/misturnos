# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import PrependedText
from django.contrib.auth.models import User
from .models import Post


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    helper = FormHelper()
    helper.form_id = 'LoginForm'
    helper.form_action = '/login'
    helper.add_input(
        Submit(
               'submit',
               'Registrarse',
               css_class='btn btn-lg btn-primary btn-block'
            )
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    helper = FormHelper()
    helper.form_action = '/register'
    helper.form_method = 'post'
    helper.form_class = 'form-signin'
    helper.help_text_inline = False
    helper.add_input(
        Submit(
               'submit',
               'Registrarse',
               css_class='btn btn-lg btn-primary btn-block'
            )
    )
    helper.form_show_labels = False
    helper.form_tag = False
    helper.layout = Layout(
        PrependedText('username', '@', placeholder="apodo"),
        Field('email', placeholder="email"),
        Field('password', placeholder="password"),
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)
