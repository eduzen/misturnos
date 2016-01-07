# -*- coding: utf-8 -*-
import json
import datetime
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import View
from django.utils import timezone
from django.conf import settings
from .models import Post
from .models import Profile
from .models import Address
from .models import Project
from .models import Patient
from .forms import PostForm
from .forms import UserForm
from .forms import LoginForm
from .forms import ProfileForm
from .forms import PatientsForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.core.urlresolvers import reverse


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
                raise ValueError(u'Username invalido')

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

            ajax_vars = {'success': True, 'error': 'Usuario creado!'}
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


def calendar(request):
    date = datetime.datetime(2015, 4, 1)

    return render(request, 'blog/calendar.html', {'date': date})
    return render(request, 'schedule/calendar.html')  # , {'date': date})


class Login(View):
    def post(self, request, *args, **kwargs):
        print 'Algo'
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print 'not none'
            if user.is_active:
                print 'is active'
                auth_login(request, user)
                return redirect('/home')

        return redirect('/login')

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})


class Perfil(View):
    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            usuario = request.user
            files = request.FILES

            if data is None:
                raise ValueError(u'Deben completarse todos los campos')

            nombre = data.get('nombre', None)
            telefono = data.get('telefono', None)
            direccion = data.get('direccion', None)
            profesion = data.get('profesion', None)
            codigopostal = data.get('codigopostal', None)
            apellido = data.get('apellido', None)
            empresa = data.get('empresa', None)
            avatar = files.get('avatar', None)

            # consulta la tabla profile y trae el perfil del usuario logueado
            perfil = Profile.objects.filter(user=usuario)

            if not perfil.exists():
                raise ValueError(u'Problemas con el perfil')

            perfil = perfil[0]

            usuario.first_name = nombre
            usuario.last_name = apellido

            perfil.phone_number = telefono
            perfil.profession = profesion

            if avatar is not None:
                perfil.avatar = avatar

            perfil.save()
            usuario.save()

            direcciones = Address.objects.filter(profile=perfil)

            if direcciones.exists():
                dire = direcciones[0]
                dire.address = direccion
                dire.postal_code = codigopostal
                dire.save()
            else:
                d = Address.objects.create(address=direccion, profile=perfil)
                d.postal_code = codigopostal
                d.save()

            proyecto = Project.objects.filter(user=perfil)

            if proyecto.exists():
                proyecto = proyecto[0]
                proyecto.name = empresa
                proyecto.save()
            else:
                p = Project.objects.create(user=perfil, name=empresa)
                p.save()

            return redirect('/profile')

        except ValueError as error:
            print error
            return redirect('/profile')

    def get(self, request, *args, **kwargs):
        usuario = request.user
        perfil = Profile.objects.filter(user=usuario)

        if not perfil.exists():
            raise ValueError(u'Problemas con el perfil')

        perfil = perfil[0]

        proyecto = Project.objects.filter(user=perfil)

        empresa = ''
        dire = ''
        codigopostal = ''

        if proyecto.exists():
            empresa = proyecto[0].name

        direcciones = Address.objects.filter(profile=perfil)

        if direcciones.exists():
            dire = direcciones[0].address
            codigopostal = direcciones[0].postal_code

        if not perfil.avatar:
            pathtoimage = 'static/img/default.jpg'
        else:
            pathtoimage = "media/%s" % (perfil.avatar.url)

        data = {
            'nombre': usuario.first_name,
            'apellido': usuario.last_name,
            'telefono': perfil.phone_number,
            'direccion': dire,
            'codigopostal': codigopostal,
            'profesion': perfil.profession,
            'empresa': empresa
        }

        form = ProfileForm(data)
        return render(request, 'blog/profile.html', {'form': form,
                      'avatar': pathtoimage})


class Appointment(View):
    """docstring for Appointment"""
    def post(self, request, *args, **kwargs):
        print 'Appointment POST'
        data = request.POST
        print data.values()


class Patients(View):
    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            usuario = request.user

            if data is None:
                raise ValueError(u'Deben completarse todos los campos')

            name = data.get('name', None)
            last_name = data.get('last_name', None)
            phone_number = data.get('phone_number', None)
            email = data.get('email', None)
            medical_coverage = data.get('medical_coverage', None)
            notes = data.get('notes', None)
            born_date = data.get('born_date', None)

            patient = Patient.objects.create(doctor=usuario)
            patient.doctor = usuario
            patient.name = name
            patient.last_name = last_name
            patient.email = email
            patient.phone_number = phone_number
            patient.medical_coverage = medical_coverage
            patient.notes = notes
            patient.born_date = born_date

            patient.save()

            return redirect('/pacientes')

        except ValueError as error:
            print error
            return redirect('/pacientes')

    def get(self, request, *args, **kwargs):
        form = PatientsForm()
        return render(request, 'blog/patients.html', {'form': form})


class PatientsList(View):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user

            patients = Patient.objects.filter(doctor=user)

        except ValueError as error:
            print error
            return redirect('/lista-pacientes')

        return render(request, 'blog/patients_list.html', {'patients': patients})


class PatientsListTest(View):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user

            patients = Patient.objects.filter(doctor=user)

        except ValueError as error:
            print error
            return redirect('/lista-pacientes')

        return render(request, 'blog/patients_list_test.html', {'patients': patients})
