from django.shortcuts import render
from .models import TipoMascota, Mascota, Galeria

# importar el modelo de usuarios (User)
from django.contrib.auth.models import User
# importar librerias de validacion de login
from django.contrib.auth import authenticate,logout, login as login_aut
# importar la libreria de decoradores que permite evitar el ingreso a paginas restringidas
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def index(request):
    mascotas = Mascota.objects.filter(publicar=True).order_by('-edad')[:3]
    categorias = TipoMascota.objects.all()
    contexto = {"mascotas":mascotas,"categorias":categorias}
    return render(request, "core/index.html",contexto)

def galeria(request):
    mascotas = Mascota.objects.filter(publicar=True)
    tipos = TipoMascota.objects.all()
    contexto = {"mascotas":mascotas,"tipos":tipos}
    return render(request, "core/galeria.html",contexto)

def formulario(request):
    return render(request, "core/formulario.html")

def mostrar_mascota(request,id):
    mascota = Mascota.objects.get(nombre=id)
    galeria = Galeria.objects.filter(mascota=mascota)
    contexto = {"mascota":mascota,"galeria":galeria}
    return render(request, "core/ficha.html",contexto)

def filtrar_tipo_mascota(request):
    mascotas = Mascota.objects.filter(publicar=True)
    cantidad = Mascota.objects.filter(publicar=True).count()

    if request.POST:
        nombre = request.POST.get("cboTipo")
        tipo = TipoMascota.objects.get(nombre=nombre)
        mascotas = Mascota.objects.filter(tipo=tipo).filter(publicar=True)
        cantidad = Mascota.objects.filter(tipo=tipo).filter(publicar=True).count()
    tipos = TipoMascota.objects.all()
    contexto = {"mascotas":mascotas,"tipos":tipos,"cant":cantidad}

    return render(request, "core/galeria.html",contexto)

def filtrar_por_categoria(request,id):
    obj_cate = TipoMascota.objects.get(nombre=id)
    mascotas = Mascota.objects.filter(publicar=True).filter(tipo=obj_cate)

    tipos = TipoMascota.objects.all()
    contexto = {"mascotas":mascotas,"tipos":tipos}
    return render(request, "core/galeria.html",contexto)


def filtro_mascota_pc(request):
    mascotas = Mascota.objects.filter(publicar=True)
    
    if request.POST:
        texto = request.POST.get("txtFiltrar")
        mascotas = Mascota.objects.filter(descripcion__contains=texto).filter(publicar=True)
        cantidad = Mascota.objects.filter(descripcion__contains=texto).filter(publicar=True).count()
    tipos = TipoMascota.objects.all()
    contexto = {"mascotas":mascotas,"tipos":tipos,"cant":cantidad}

    return render(request, "core/galeria.html",contexto)

def filtro_mascota_nombre(request):
    mascotas = Mascota.objects.filter(publicar=True)
    
    if request.POST:
        texto = request.POST.get("txtNombre")
        mascotas = Mascota.objects.filter(nombre=texto).filter(publicar=True)
        cantidad = Mascota.objects.filter(nombre=texto).filter(publicar=True).count()
    tipos = TipoMascota.objects.all()
    contexto = {"mascotas":mascotas,"tipos":tipos,"cant":cantidad}

    return render(request, "core/galeria.html",contexto)

def cerrar_sesion(request):
    logout(request)

    mascotas = Mascota.objects.filter(publicar=True).order_by('-edad')[:3]
    categorias = TipoMascota.objects.all()
    contexto = {"mascotas":mascotas,"categorias":categorias}
    return render(request, "core/index.html",contexto)

def login(request):
    if request.POST:
        usuario = request.POST.get("txtNombre")
        password = request.POST.get("txtPass")
        us = authenticate(request,username=usuario,password=password)
        if us is not None and us.is_active:
            login_aut(request,us)

            cant = Mascota.objects.filter(usuario=usuario).filter(publicar=False).count()
            mascotas = Mascota.objects.filter(publicar=True).order_by('-edad')[:3]
            categorias = TipoMascota.objects.all()
            contexto = {"cant":cant,"mascotas":mascotas,"categorias":categorias}
            return render(request,"core/index.html",contexto)
        else:
            contexto = {"mensaje":"no existe usuario o contraseña"}
            return render(request, "core/login.html",contexto)        
    return render(request, "core/login.html")

@login_required(login_url='/login/')
@permission_required('misPerris.add_mascota',login_url='/login/')
def registro(request):
    tipos = TipoMascota.objects.all() # select * from TipoMascota
    nom_user = request.user.username # recuperar el nombre del usuario actual
    mensaje=""
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        tipo = request.POST.get("cboTipo")
        imagen = request.FILES.get("txtImg")
        obj_tipo = TipoMascota.objects.get(nombre=tipo) # select * from TipoMascota where nombre=''
        
        mas = Mascota()
        
        mas.nombre=nombre
        mas.edad=edad
        mas.descripcion=desc
        
        if imagen is not None:
            mas.imagen=imagen
        
        mas.tipo=obj_tipo
        mas.usuario = nom_user
        
        mas.save()
        mensaje="grabo"

    mascotas = Mascota.objects.filter(usuario=nom_user)
    cant =  Mascota.objects.filter(usuario=nom_user).count()
    contexto = {"tipos":tipos,"mensaje":mensaje,"masc":mascotas,"cantidad":cant}
    return render(request, "core/registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.delete_mascota',login_url='/login/')
def eliminar_mascota(request,id):
    mensaje=""
    try:
        masc = Mascota.objects.get(nombre=id)
        masc.delete()
        mensaje="elimino mascota"
    except:
        mensaje="no elimino mascota"
    
    tipos = TipoMascota.objects.all() # select * from TipoMascota
    nom_user = request.user.username # recuperar el nombre del usuario actual
    mascotas = Mascota.objects.filter(usuario=nom_user)
    cant =  Mascota.objects.filter(usuario=nom_user).count()
    contexto = {"tipos":tipos,"mensaje":mensaje,"masc":mascotas,"cantidad":cant}
    return render(request, "core/registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.view_mascota',login_url='/login/')
def modificar_mascota(request,id):
    tipos = TipoMascota.objects.all()   
    masc = Mascota.objects.get(nombre=id)
    contexto = {"mascota":masc,"tipos":tipos}
    return render(request,"core/modificar.html",contexto)

def creacion_usuario(request):
    if request.POST:
        nom_usuario = request.POST.get("txtUsuario")
        nombre = request.POST.get("txtNombre")
        apellido = request.POST.get("txtApellido")
        email = request.POST.get("txtEmail")
        pass1 = request.POST.get("txtPass1")
        pass2 = request.POST.get("txtPass2")
        if pass1!=pass2:
            contexto ={"mensaje":"password no son iguales"}
            return render(request,"core/creacion_usuario.html",contexto)        

        try:
            # buscara ese nombre de usuario en la tabla de User
            usu = User.objects.get(username=nom_usuario)
            contexto = {"mensaje":"nombre de usuario ya existe, seleccione otro"}
            return render(request,"core/creacion_usuario.html",contexto)
        except:
            usu = User()
            usu.first_name= nombre
            usu.last_name = apellido
            usu.email= email
            usu.set_password(pass1)
            usu.username = nom_usuario
            usu.save()

            us = authenticate(request,username=nom_usuario,password=pass1)
            login_aut(request,us)

            mascotas = Mascota.objects.filter(publicar=True).order_by('-edad')[:3]
            categorias = TipoMascota.objects.all()
            contexto = {"mascotas":mascotas,"categorias":categorias}
            return render(request, "core/index.html",contexto)


    return render(request,"core/creacion_usuario.html")

@login_required(login_url='/login/')
@permission_required('misPerris.change_mascota',login_url='/login/')
def modificar(request):
    tipos = TipoMascota.objects.all() # select * from TipoMascota
    mensaje=""
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        tipo = request.POST.get("cboTipo")
        imagen = request.FILES.get("txtImg")
        obj_tipo = TipoMascota.objects.get(nombre=tipo) # select * from TipoMascota where nombre=''
        
        try:
            mas = Mascota.objects.get(nombre=nombre)
            mas.nombre=nombre
            mas.edad=edad
            mas.descripcion=desc
            mas.tipo=obj_tipo

            if imagen is not None:
                mas.imagen=imagen
            
            mas.comentario='--'
            mas.save()
            mensaje="modifico"
        except:
            mensaje="no modifico"

    tipos = TipoMascota.objects.all() # select * from TipoMascota
    nom_user = request.user.username # recuperar el nombre del usuario actual
    mascotas = Mascota.objects.filter(usuario=nom_user)
    cant =  Mascota.objects.filter(usuario=nom_user).count()
    contexto = {"tipos":tipos,"mensaje":mensaje,"masc":mascotas,"cantidad":cant}
    return render(request, "core/registro.html",contexto)

def adoptar(request,id):
    try:
        mas = Mascota.objects.filter(publicar=True).get(nombre=id)
        nom_user = request.user.username
        mas.dueno = nom_user
        mas.publicar = False
        mas.save()
        mensaje = "Adoptada"
    except:
        mensaje = "No Pudo Adoptar"
    
    mascota = Mascota.objects.get(nombre=id)
    contexto = {"mascota":mascota,"mensaje":mensaje}
    return render(request, "core/ficha.html",contexto)

def adm_adoptar(request):
    nom_user = request.user.username
    mascotas = Mascota.objects.filter(dueno=nom_user)
    cant = Mascota.objects.filter(dueno=nom_user).count()
    contexto = {"cant":cant,"mascotas":mascotas}
    return render(request,"core/adm_adoptar.html",contexto)

def devolver(request,id):
    try:
        mas = Mascota.objects.filter(publicar=False).get(nombre=id)
        mas.dueno = '--'
        mas.comentario = '--'
        mas.save()
        mensaje = "se devolvio la mascota "+ id
    except:
        mensaje ='No se pudo devolver'
    
    nom_user = request.user.username
    mascotas = Mascota.objects.filter(dueno=nom_user)
    cant = Mascota.objects.filter(dueno=nom_user).count()
    contexto = {"cant":cant,"mascotas":mascotas}
    return render(request,"core/adm_adoptar.html",contexto)

def insertar_galeria(request):
    mensaje=""
    if request.POST:
        nom_mascota = request.POST.get("txtMascota")
        imagen = request.FILES.get("txtImg")
        obj_mascota = Mascota.objects.get(nombre=nom_mascota)

        gale = Galeria()
        gale.imagen = imagen
        gale.mascota = obj_mascota
        gale.save()
        mensaje = "Imagen Agregada a mascota "+nom_mascota

    tipos = TipoMascota.objects.all() # select * from TipoMascota
    nom_user = request.user.username # recuperar el nombre del usuario actual
    mascotas = Mascota.objects.filter(usuario=nom_user)
    cant =  Mascota.objects.filter(usuario=nom_user).count()
    contexto = {"tipos":tipos,"mensaje":mensaje,"masc":mascotas,"cantidad":cant}
    return render(request, "core/registro.html",contexto)
   


