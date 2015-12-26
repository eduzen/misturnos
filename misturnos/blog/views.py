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
from django.core import serializers

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
        data = request.POST
        if not data:
            return redirect('/register')

        try:
            success = False
            form = UserForm(data)
            # print "form : {}".format(form)
            if not form.is_valid():
                error = 'Sorry this is an invalid form'
                ajax_vars = {'success': success, 'error': error}
                return HttpResponse(
                    json.dumps(ajax_vars),
                    content_type='application/javascript'
                )

            print form.cleaned_data.keys()
            print form.cleaned_data.values()

            userName = form.cleaned_data.get('username', None)
            userMail = form.cleaned_data.get('email', None)
            userPass = form.cleaned_data.get('password', None)

            if User.objects.filter(username=userName).exists():
                error = _('Sorry this username is already taken')
                print 'this username {0} already exists'.format(userName)
            if User.objects.filter(email=userMail).exists():
                error = _('Sorry this email is already taken')
                print 'this email ({0}) already exists'.format(userMail)
            else:
                success = True
                user = User.objects.create_user(
                    username=userName,
                    email=userMail,
                    password=userPass
                )
                user.save()

            ajax_vars = {'success': success, 'error': error}
            return HttpResponse(
                json.dumps(ajax_vars),
                content_type='application/javascript'
            )
        except Exception as e:
            print e
            ajax_vars = {'success': success, 'error': e.message}
            print ajax_vars
            return HttpResponse(
                json.dumps(ajax_vars),
                content_type='application/javascript'
            )

    def get(self, request, *args, **kwargs):
        print "\n Register"

        form = UserForm()

        return render(request, 'blog/register.html', {'form': form})


def logout(request):
    return render(request, 'blog/index.html')


def change_password(request):
    return render(request, 'blog/change-password.html')
