"""misturnos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('blog.urls')),
]
# Auth urls
urlpatterns += [
    # url(r'^', include('django.contrib.auth.urls')),
    url(
        r'^login/$',
        auth_views.login,
        {'template_name': 'blog/login.html'}
        ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'template_name': 'blog/index.html'}
        ),
    url(
        r'^change-password/$',
        auth_views.password_change,
        {'template_name': 'blog/change-password.html'}
    )
]
