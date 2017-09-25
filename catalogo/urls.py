from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.registro, name='addUser'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'editar_perfil$', views.editar_perfil, name='editar_perfil'),
    url(r'^detalle_especie/(?P<id>.+)/$', views.detalleEspecie, name="detalle_especie"),
    url(r'^admin/', admin.site.urls),
]