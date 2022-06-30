from django.urls import path
from . import views

app_name = "carro"

urlpatterns = [

    path("agregar/<str:idProducto>", views.agregar_producto, name="agregar"),
    path("agregar2/<str:idProducto>", views.agregar2, name="agregar2"),
    path("eliminar/<str:idProducto>/", views.eliminar_producto, name="eliminar"),
    path("restar/<str:idProducto>/", views.restar_producto, name="restar"),
    path("limpiar/", views.limpiar_carro, name="limpiar"),
    path('add/', views.carro_add, name='carro_add'),
    
]