# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cities_light.models import City, Country
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django import forms
from django.forms import ModelForm

# Create your models here.

class Categoria (models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Taxonomia (models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Especie(models.Model):
    nombre = models.CharField(max_length=50)
    nombre_cientifico = models.CharField(max_length=60)
    desc_corta = models.CharField(max_length=150)
    desc_larga = models.CharField(max_length=500)
    foto = models.ImageField(upload_to='images',null=True)
    categoria = models.ForeignKey(Categoria, null=False)
    taxonomia = models.ForeignKey(Taxonomia, null=False)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    foto = models.ImageField(upload_to='images/user',null=True)
    pais_origen = models.ForeignKey(Country)
    ciudad = models.ForeignKey(City)
    comentario_interes = models.CharField(max_length=1000)
    auth_user_id = models.ForeignKey(User, null = False)

class Comentario(models.Model):
    especie_id = models.ForeignKey(Especie, null=False)
    email = models.CharField(max_length=500,null=True)
    fecha = models.DateTimeField(auto_now_add= True, editable=False)
    comentario = models.CharField(max_length=1000, blank=False, null=True)

class UserForm (ModelForm):

    class Meta :
        model = Usuario
        fields = ['foto', 'pais_origen', 'ciudad', 'comentario_interes']

    nombre = forms.CharField(max_length=20)
    apellido = forms.CharField(max_length=20)
    email = forms.EmailField()
    nombre_usuario = forms.CharField(max_length=50)
    clave = forms.CharField(widget=forms.PasswordInput())
    confirme_clave = forms.CharField(widget=forms.PasswordInput())


    def clean_username(self):
        username = self.cleaned_data['nombre_usuario']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado')
        return username

    #def clean_email(self):
    #    email = self.cleaned_data['email']
    #    if User.objects.filter(email=email):
    #        raise forms.ValidationError('Ya existe un email igual registrado')
    #    return email

    def clean_password2(self):
        password = self.cleaned_data['clave']
        password2 = self.cleaned_data['confirme_clave']

        if password != password2:
            raise forms.ValidationError('Las claves no coinciden')
        return password2
