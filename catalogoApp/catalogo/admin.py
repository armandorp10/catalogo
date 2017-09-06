# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Categoria,Taxonomia,Especie,Usuario,Comentario

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Taxonomia)
admin.site.register(Especie)
admin.site.register(Usuario)
admin.site.register(Comentario)