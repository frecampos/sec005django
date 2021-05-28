from django.contrib import admin
from django.urls import path, include
from .views import filtrar_por_categoria, insertar_galeria, devolver, adm_adoptar, adoptar, filtro_mascota_nombre, modificar,modificar_mascota, eliminar_mascota, creacion_usuario,cerrar_sesion,index,galeria,formulario, registro, mostrar_mascota,filtrar_tipo_mascota,filtro_mascota_pc,login

urlpatterns = [
    path('',index,name='INDEX'),
    path('galeria/',galeria,name='GALE'),
    path('formu/',formulario,name='FORMU'),
    path('registro/', registro,name='REG'),
    path('mostrar_mascota/<id>/',mostrar_mascota,name='MOSTRAR'),
    path('filtrar_tipo/',filtrar_tipo_mascota,name='FILTROT'),
    path('filtro_palabras/',filtro_mascota_pc,name='FILTROPC'),
    path('login/',login,name='LOGIN'),
    path('logout/',cerrar_sesion,name='LOGOUT'),
    path('creacion_usuario/',creacion_usuario,name='CREARUSUARIO'),
    path('eliminar_mascota/<id>/',eliminar_mascota,name='ELIMINARM'),
    path('modificar_mascota/<id>/',modificar_mascota,name='MODIFICARM'),
    path('modificar/',modificar,name='MODI'),
    path('buscar_nombre/',filtro_mascota_nombre,name='BUSCARNOMBRE'),
    path('adoptar/<id>/',adoptar,name='ADOPTAR'),
    path('adm_adoptar/',adm_adoptar,name='ADMADOPTAR'),
    path('devolver/<id>/',devolver,name='DEVOLVER'),
    path('insertar_galeria/',insertar_galeria,name='INSERTARG'),
    path('filtro_categoria/<id>/',filtrar_por_categoria,name='FILTROC'),
]