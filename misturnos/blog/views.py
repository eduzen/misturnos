from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import View
from django.utils import timezone
from .models import Post
from .forms import PostForm
from .forms import UserForm


# Create your views here.


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
        print "edu"
        print request
        print dir(request)
        data = request.POST
        print data
        userName = request.REQUEST.get('username', None)
        userPass = request.REQUEST.get('password', None)
        userMail = request.REQUEST.get('email', None)

        print userName
        print userPass
        print userMail

        return redirect('/')

    def get(self, request, *args, **kwargs):
        form = UserForm()

        return render(request, 'blog/register.html', {'form': form})


def logout(request):
    return render(request, 'blog/index.html')


def change_password(request):
    return render(request, 'blog/change-password.html')
