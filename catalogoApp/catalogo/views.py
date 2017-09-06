# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .models import Especie
# Create your views here.
def index(request):
    lista_especies = Especie.objects.all()
    context = {'lista_especies':lista_especies}
    return render(request, 'catalogo/index.html',context)