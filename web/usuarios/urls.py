from . import views

from django.urls import path, include
from .views import vRegistro,adminRegistro

urlpatterns=[
    path('usuarios/',views.usuarios,name="usuarios"),
    path('registro/',vRegistro.as_view(),name="registro"),
    path('adminAdd',adminRegistro.as_view(),name="adminAdd"),
    path('logear', views.logear, name='logear'),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('usuarios_edit/<id>/',views.modificar_usuario, name='usuarios_edit'),
    path('usuarios_eliminar/<id>/',views.eliminar_usuario, name='usuarios_eliminar'),
]