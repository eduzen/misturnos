# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import View
from django.utils import timezone
from .models import Post
from .forms import PostForm
from .forms import UserForm
from django.contrib.auth.models import User
from django.http import HttpResponse


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def test(request):
    return render(request, 'blog/test.html')


def testnavbar(request):
    return render(request, 'blog/navbar.html')


def index(request):
    return render(request, 'blog/index.html')


def login(request):
    return render(request, 'blog/login.html')


class Register(View):
    def post(self, request, *args, **kwargs):
        print "\n Register"
        try:
            data = request.POST
            if not data:
                raise ValueError(u"Formulario de registración vacio")

            form = UserForm(data)

            if not form.is_valid():
                raise ValueError(u'Username o password invalido')

            userName = form.cleaned_data.get('username', None)
            userMail = form.cleaned_data.get('email', None)
            userPass = form.cleaned_data.get('password', None)

            if None in (userName, userMail, userPass):
                raise ValueError(u'Deben completarse todos los campos')

            if User.objects.filter(username=userName).exists():
                raise ValueError(
                     u'this username {0} already exists'.format(userName)
                )

            if User.objects.filter(email=userMail).exists():
                raise ValueError(
                     u'email {0} ya registrado'.format(userMail)
                )

            user = User.objects.create_user(
                    username=userName,
                    email=userMail,
                    password=userPass
                )
            user.save()

            ajax_vars = {'success': True, 'results': u'Usuario creado!'}
            return HttpResponse(
                json.dumps(ajax_vars),
                content_type='application/javascript'
            )

        except ValueError as error:
            ajax_vars = {'success': False, 'error': error.message}
            return HttpResponse(
                    json.dumps(ajax_vars),
                    content_type='application/javascript'
            )

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, 'blog/register.html', {'form': form})


def logout(request):
    return render(request, 'blog/index.html')


def change_password(request):
    return render(request, 'blog/change-password.html')
