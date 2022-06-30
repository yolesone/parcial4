from django.shortcuts import render,redirect,get_object_or_404
from .models import Usuario
from django.views.generic import View,UpdateView
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth import logout, authenticate
from .forms import FormularioUsuario,FormularioLogin,FormularioAdmin
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from . forms import Usuario as FormUsuario

# Create your views here.

def usuarios(request):
    print("Estoy en el usuarios")
    usuarios = Usuario.objects.all()
    context={"usuarios":usuarios}
    return render(request,'usuarios/usuarios.html',context)


def editar_usuario(request, pk):
    mensajes=[]
    errores=[]
    usuarios = Usuario.objects.all()
    usuario =  get_object_or_404(Usuario, id=pk)

    if usuario:
        form = FormUsuario(request.POST or None,
                            request.FILES or None, instance=usuario)
        #form = Formalumno(instance=alumno)
        print("estoy en alumno true")
        if request.method == 'POST':
            print("ingresó al POST")


            if form.is_valid():
                print("is valid...")
                usuario = form.save()
                usuario.save()
                mensajes.append("Bien, datos grabados...")
                messages.success(request,"Agregado correctamente")
                print("Bien!, datos grabados...")
                accion = 'tabla'
                context = {'usuarios': usuarios, 'mensajes': mensajes,
                           'errores': errores, 'accion': accion}
            else:
                errores.append("Error!, datos no grabados...del EDIT")
                print("Error!, datos no grabados... form="+str(form.errors))
                accion='tabla'
                context = {'usuarios': usuarios, 'mensajes': mensajes,
                       'errores': errores, 'accion': accion}

            return render(request, 'usuarios/usuarios_edit.html', context)
        else:
            mensajes.append("Bien!, id existe...")
            print("entró al else form=alumno()...")
            accion = 'form_edit'
            context = {'usuarios': usuarios, 'mensajes': mensajes,
                       'errores': errores,'form':form, 'accion': accion}
            return render(request, 'usuarios/usuarios_edit.html', context)

    else:
        print("Error, id_alumno no existe")
        errores.append("Error id no encontrado.")
        accion='tabla'
        context = {'usuarios': usuarios, 'mensajes': mensajes,
                   'errores': errores, 'accion':accion}
        return render(request, 'usuarios/usuarios_edit.html', context)


def cerrar_sesion(request):
    logout(request)
    return redirect('home')

class vRegistro(View):
    def get(self, request):
        form = FormularioUsuario()
        return render(request, 'app/registro.html', {"form": form})

    def post(self, request):
        form = FormularioUsuario(request.POST)

        if form.is_valid():

            usuario = form.save()
            login(request, usuario)
            return redirect('home')

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request, 'app/registro.html', {"form": form})

def logear(request):
    if request.method == "POST":
        form = FormularioLogin(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
            else:
                messages.error(request, "Usuario no válido")
        else:
            messages.error(request, "Información incorrecta")

    form = FormularioLogin()
    return render(request, 'app/login.html', {"form": form})

class adminRegistro(View):
    def get(self, request):
        form = FormularioAdmin()
        return render(request, 'usuarios/agregar_usuarios.html', {"form": form})

    def post(self, request):
        form = FormularioAdmin(request.POST)

        if form.is_valid():

            usuario = form.save()
            login(request, usuario)
            return redirect('home')

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request, 'usuarios/agregar_usuarios.html', {"form": form})

@csrf_protect
def modificar_usuario(request, id):
    

    usuario = get_object_or_404(Usuario, id = id)

    data = {
        'form': FormularioAdmin(instance=usuario)
        }
    if request.method == 'POST':
        formulario = FormularioAdmin(data = request.POST,instance = usuario)
        if formulario.is_valid():
            formulario.save()
            redirect(to='usuarios')
        data["form"] = formulario

    return render(request,'usuarios/usuarios_edit.html',data)

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id = id)
    usuario.delete()
    return redirect(to='usuarios')

