# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Post
from crispy_forms.bootstrap import StrictButton
# from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class UserForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'email',
        'password',
        'remember_me',
        StrictButton('Sign in', css_class="btn btn-lg btn-primary btn-block"),
        Field('text_input', css_class='form-control'),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

'''
class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(
        widget=forms.widget.TextInput,
        label="Email"
    )
    password1 = forms.CharField(
        widget=forms.widget.PasswordInput,
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.widget.PasswordInput,
        label="Password (confirme)"
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
'''
