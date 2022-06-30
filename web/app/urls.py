from . import views
from django.urls import path, include

urlpatterns=[
    path('',views.home,name="home"),
    path('tienda/',views.tienda,name="tienda"),
    path('detail/<str:pk>', views.detail, name='detail'),
    path('carrito/',views.carrito,name="carrito"),
    
    path('mantenedor/',views.mantenedor,name="mantenedor"),
    path("productosAdd", views.productosAdd, name="productosAdd"),
    path("productos_list", views.productos_list, name="productos_list"),
    path('productos_del/<str:pk>', views.productos_del, name='productos_del'),
    path('productos_edit/<str:pk>', views.productos_edit, name='productos_edit'),

    path('procesar_venta/',views.procesar_venta,name="procesar_venta"),
    path("pedidos", views.pedidos, name="pedidos"),
    path('editar_pedido/<int:pk>', views.editar_pedido, name='editar_pedido'),

    path("mis_pedidos/",views.mis_pedidos, name='mis_pedidos'),
    path('det_pedido/<int:pk>', views.detalle_pedido, name='det_pedido'),
]