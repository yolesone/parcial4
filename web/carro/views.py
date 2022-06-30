from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.shortcuts import render
from .carro import Carro
from app.models import Producto
from django.shortcuts import redirect

# Create your views here.

def agregar_producto(request, idProducto):

    if request.POST.get('action') == 'post':
        product_qty = int(request.POST.get('productqty'))
        print(product_qty)
        carro = Carro(request)
        producto = Producto.objects.get(idProducto=idProducto)
        carro.agregar(producto=producto,qty = product_qty)


    return redirect("carrito")


def carro_add(request):
    carro = Carro(request)
    if request.POST.get('action') == 'post':
        idProducto = int(request.POST.get('idProducto'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Producto, id=idProducto)
        carro.add(product=product, qty=product_qty)

        basketqty = carro.__len__()
        response = JsonResponse({'qty': basketqty})
        return redirect("carrito")


def eliminar_producto(request, idProducto):
    carro = Carro(request)
    producto = Producto.objects.get(idProducto=idProducto)
    carro.eliminar(producto=producto)
    return redirect("carrito")


def restar_producto(request, idProducto):
    carro = Carro(request)
    producto = Producto.objects.get(idProducto=idProducto)
    carro.restar_producto(producto=producto)
    return redirect("carrito")

def agregar2(request, idProducto):
    carro = Carro(request)
    producto = Producto.objects.get(idProducto=idProducto)
    carro.agregar2(producto=producto)
    return redirect("carrito")


def limpiar_carro(request, idProducto):
    carro = Carro(request)
    carro.vaciar_carro()
    return redirect("carrito")