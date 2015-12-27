from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', views.index),
    url(r'^home$', views.index),
    url(r'^index$', views.index),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^test$', views.test),
    url(r'^navbar$', views.testnavbar),
    url(r'^register$', views.Register.as_view()),
    url(r'^login$', views.Login.as_view()),
    url(r'^profile$', login_required(views.Perfil.as_view())),
]
