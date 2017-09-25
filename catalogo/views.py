# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from django import forms

from .models import Especie, UserForm, Usuario, Categoria, Comentario
# Create your views here.
def index(request):
    lista_especies = Especie.objects.all()
    if (request.POST):
        filter = FilterForm(request.POST)
        if filter.is_valid():
            data = filter.cleaned_data
            if data.get('listaCategorias') is not None:
                lista_especies = Especie.objects.filter(categoria=data.get('listaCategorias'))
    lista_categorias = FilterForm()
    page = request.GET.get('page', 1)
    paginator = Paginator(lista_especies, 4)

    try:
        especies = paginator.page(page)
    except PageNotAnInteger:
        especies = paginator.page(1)
    except EmptyPage:
        especies = paginator.page(paginator.num_pages)

    return render(request, 'catalogo/index.html', {'especies':especies, 'filtro':lista_categorias})

def login_view(request):
    if request.user.is_authenticated():
        return redirect(reverse('index'))
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
        else:
            mensaje = 'Nombre de usuario o clave invalido'

    return render(request,'catalogo/login.html',{'mensaje':mensaje})

@csrf_exempt
def isLogged_view(request):
    if request.user.is_authenticated():
        mensaje = 'Ok'
    else:
        mensaje = 'No'

    return JsonResponse({'mensaje':mensaje})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    lista_especies = Especie.objects.all()
    context = {'lista_especies':lista_especies}
    return render(request, 'catalogo/register.html',context)

def registro (request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('nombre_usuario')
            first_name = data.get('nombre')
            last_name = data.get('apellido')
            password = data.get('clave')
            email = data.get('email')

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email

            user_app = Usuario (foto = data.get('foto'),
                                comentario_interes = data.get('comentario_interes'),
                                pais_origen = data.get('pais_origen'),
                                ciudad = data.get('ciudad'),
                                auth_user_id = user_model);
            user_model.save()
            user_app.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserForm()
        context = {'form' : form}
    return render(request, 'catalogo/register.html', context)

def editar_perfil (request):

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('nombre_usuario')
            first_name = data.get('nombre')
            last_name = data.get('apellido')
            password = data.get('clave')
            email = data.get('email')

            user_model = request.user
            user_model.username = username
            #user_model.password = password
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email

            user_app = Usuario.objects.get(auth_user_id=request.user)
            user_app.foto = data.get('foto')
            user_app.comentario_interes = data.get('comentario_interes')
            user_app.pais_origen = data.get('pais_origen')
            user_app.ciudad = data.get('ciudad')

            #user_app = Usuario(foto=data.get('foto'),
            #                   comentario_interes=data.get('comentario_interes'),
            #                   pais_origen=data.get('pais_origen'),
            #                   ciudad=data.get('ciudad'),
            #                   auth_user_id=user_model);

            user_model.save()
            user_app.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        usuario = Usuario.objects.get(auth_user_id=request.user)
        print(usuario.foto)
        data = {'nombre': usuario.auth_user_id.first_name,
                 'apellido': usuario.auth_user_id.last_name,
                 'foto': usuario.foto,
                 'pais_origen': usuario.pais_origen,
                 'ciudad': usuario.ciudad,
                 'comentario_interes': usuario.comentario_interes,
                 'email': usuario.auth_user_id.email,
                 'nombre_usuario': usuario.auth_user_id.username,
                 'clave': usuario.auth_user_id.password,
                 'confirme_clave': usuario.auth_user_id.password}
        form = UserForm(data)
        context = {'userForm': form}
    return render(request, 'catalogo/edit.html', context)

class FilterForm (forms.Form):
    listaCategorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),
                                             empty_label='Todas...',
                                             required = False)

def detalleEspecie(request,id=None):
    especie = Especie.objects.get(id=id)
    lista_comentarios = Comentario.objects.filter(especie_id=id)
    context = {'especie': especie,
               'lista_comentarios':lista_comentarios}
    return render(request, 'catalogo/detalle_especie.html', context)