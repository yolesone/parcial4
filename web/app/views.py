from ctypes import resize
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VentaForm
from .models import *
from carro.carro import Carro
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    print("Estoy  en el home")
    context={}
    return render(request,'app/home.html',context)

def mantenedor(request):
    print("Estoy  en el inicio mantenedor")
    context={}
    return render(request,'app/mantenedor.html',context)

def tienda(request):
    print("Estoy en la tienda")
    productos = Producto.objects.all()

    page = request.GET.get('page',1)
    print(page)

    try:
        paginator = Paginator(productos,6)
        productos = paginator.page(page)
    except:
        raise Http404

    context={"entity":productos,
             "paginator":paginator
            }
    return render(request,'app/tienda.html',context)

def productosAdd(request):
    print("Estoy en mantenedor (add)")
    context = {}
    if request.method == "POST":
        print("contralador es un post...")
        opcion = request.POST.get("opcion", "")
        print("opcion="+opcion)
        # Listar
        if opcion == "Volver":
            productos = Producto.objects.all()
            context = {'productos': productos}
            return redirect("productos_list")
        # Agregar
        if opcion == "Agregar":
            idProducto = request.POST["idProducto"]
            nombreProducto = request.POST["nombreProducto"]
            stock = int(request.POST["stock"])
            precio = int(request.POST["precio"])
            activo = int(request.POST["activo"])
            try:
                foto = request.FILES['foto']
            except:
                foto = ""

            if idProducto != "" and nombreProducto != "" and stock != "" and precio != "":
                producto = Producto(idProducto, nombreProducto,
                                    stock, precio, activo, foto)
                producto.save()
                messages.success(request,"Agregado correctamente")

                return redirect("productos_list")
            else:
                context = {
                    'mensaje': "Error, los campos no deben estar vacios"}

           # Actualizar
        if opcion == "Actualizar":
            idProducto = request.POST["idProducto"]
            nombreProducto = request.POST["nombreProducto"]
            stock = request.POST["stock"]
            precio = request.POST["precio"]
            activo = request.POST["activo"]
            foto = request.FILES['foto']

            if idProducto != "" and nombreProducto != "" and stock != "" and precio != "":
                producto = Producto(idProducto, nombreProducto,
                                    stock, precio, activo, foto)
                producto.save()
                context = {'producto': producto}
                messages.success(request,"Modificado correctamente")
            else:
                messages.error(request,"Error. Los campos no deben estar vacios")
                context = {
                    'mensaje': "Error, los campos no deben estar vacios"}
            return render(request, "mantenedor/productos_edit.html", context)

    return render(request, "mantenedor/productos_list.html", context)

def productos_edit(request, pk):

    # try:
    producto = Producto.objects.get(idProducto=pk)

    context = {}
    if producto:
        print("Edit encontró el producto...")

        context = {'producto': producto}

        return render(request, 'mantenedor/productos_edit.html', context)
        messages.success(request,"Modificado correctamente")

    return render(request, 'mantenedor/productos_list.html', context)

def productos_list(request):
    productos = Producto.objects.all()
    context={"productos":productos}
    return render(request,'mantenedor/productos_list.html',context)

def detail(request, pk):
    producto = Producto.objects.get(idProducto=pk)
    context = {
        "producto": producto
    }
    return render(request, 'app/producto_detalle.html', context)

def productos_del(request, pk):
    mensajes = []
    errores = []
    productos = Producto.objects.all()
    try:
        producto = Producto.objects.get(idProducto=pk)
        context = {}
        if producto:
            producto.delete()
            messages.success(request,"Eliminado correctamente correctamente")
            mensajes.append("Bien, datos eliminados...")

            context = {'productos': productos,
                       'mensajes': mensajes, 'errores': errores}

            return render(request, 'mantenedor/productos_list.html', context)

    except:
        print("Error, id no existe")
        errores.append("Error id no encontrado.")
        context = {'productos': productos,
                   'mensajes': mensajes, 'errores': errores}
        return render(request, 'mantenedor/productos_list.html', context)

def carrito(request):
    print('Estoy en carrito')
    context={}
    return render(request,'app/carrito.html',context)

def procesar_venta(request):

    venta = Venta.objects.create(user=request.user)
    carro = Carro(request)
    productos_venta = list()

    for key,value in carro.carro.items():

        producto = Producto.objects.get(idProducto = key)
        nuevoStock = producto.stock - value["cantidad"]
        print(nuevoStock)
        Producto.objects.filter(idProducto= key).update(stock=nuevoStock)
        productos_venta.append(
            DetalleVenta(
                producto_id = producto,
                cantidad=value["cantidad"],
                user = request.user,
                venta_id = venta
            )        
        )

    DetalleVenta.objects.bulk_create(productos_venta)
    carro.vaciar_carro()
    return redirect('mis_pedidos')

def pedidos(request):
    detalleventa = DetalleVenta.objects.all()
    context={"detalleventa":detalleventa
                }
    return render(request,'mantenedor/pedidos.html',context)

def mis_pedidos(request):
    venta = Venta.objects.filter(user= request.user)
    context={"venta":venta}
    return render(request,'app/mis_pedidos.html',context)

def editar_pedido(request, pk):
    mensajes=[]
    errores=[]
    ventas = Venta.objects.all()
    venta =  get_object_or_404(Venta, id=pk)

    if venta:
        form = VentaForm(request.POST or None,
                            request.FILES or None, instance=venta)
        #form = Formalumno(instance=alumno)
        print("estoy en venta")
        if request.method == 'POST':
            print("ingresó al POST")
            #form = Formalumno(request.POST, request.FILES)
           # print("formulario id_persona: " + form.id_persona)
            if form.is_valid():
                print("is valid...")
                venta = form.save()
                venta.save()
                mensajes.append("Bien!, datos grabados...")
                print("Bien!, datos grabados...")
                accion = 'tabla'
                context = {'ventas': ventas, 'mensajes': mensajes,
                           'errores': errores, 'accion': accion}
            else:
                errores.append("Error!, datos no grabados...del EDIT")
                print("Error!, datos no grabados... form="+str(form.errors))
                accion='tabla'
                context = {'ventas': ventas, 'mensajes': mensajes,
                       'errores': errores, 'accion': accion}

            return render(request, 'mantenedor/pedidos.html', context)
        else:
            mensajes.append("Bien!, id existe...")
            print("entró al else form=alumno()...")
            accion = 'form_edit'
            context = {'ventas': ventas, 'mensajes': mensajes,
                       'errores': errores,'form':form, 'accion': accion}
            return render(request, 'mantenedor/pedidos.html', context)

    else:
        print("Error, id_alumno no existe")
        errores.append("Error id no encontrado.")
        accion='tabla'
        context = {'ventas': ventas, 'mensajes': mensajes,
                   'errores': errores, 'accion':accion}
        return render(request, 'mantenedor/pedidos.html', context)

def detalle_pedido(request,pk):
    detalleventa = DetalleVenta.objects.filter(venta_id = pk)
    context={"detalleventa":detalleventa,
                "pk":pk}
    print(context)
    return render(request,'app/det_pedido.html',context)

