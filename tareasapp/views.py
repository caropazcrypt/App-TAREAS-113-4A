from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Tarea

# Create your views here.

# def inicio(request):
#     return HttpResponse("Hola, esta es mi App de Tareas")

def inicio(request):

    return render(request, 'tareasapp/inicio.html') 


def crear_tarea(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        completada = 'completa'in request.POST

        Tarea.objects.create(
            titulo = titulo,
            descripcion = descripcion,
            completada = completada
        )
        return redirect('inicio')
    return render (request, 'tareasapp/crear.html')

def detalle_tarea(request, id):

    tarea = Tarea.objects.get(id=id)
    return render(request, 'tareasapp/detalle.html', {'tarea':tarea})

def editar_tarea(request, id):

    tarea = Tarea.objects.get(id=id)

    if request.method == 'POST':
        tarea.titulo = request.POST['titulo']
        tarea.descripcion = request.POST['descripcion']
        tarea.completada = 'completada' in request.POST

        tarea.save()

        return redirect('inicio')

    return render(request, 'tareasapp/editar.html', {'tarea':tarea})

def eliminar_tarea(request, id):

    tarea = Tarea.objects.get(id=id)

    if request.method == 'POST':
        tarea.delete()

        return redirect('inicio')

    return render(request, 'tareasapp/eliminar.html', {'tarea': tarea})

def login_pagina(request):
    return render(request, 'tareasapp/login.html')

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        #recibir las credenciales de json html
        username = request.data.get('username')
        password = request.data.get('password')

        #validar credenciales de usuarios

        usuario = authenticate(
            username=username, 
            password=password
            )

        if usuario is not None:

            token, creado = Token.objects.get_or_create(
                user=usuario
            )

            return Response({
                'mensaje': 'Autenticación correcta',
                'usuario': usuario.username,
                'token': token.key
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Usuario o contraseña incorrecta'
        }, status=status.HTTP_401_UNAUTHORIZED)

class TareasApiView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request):

        tareas = Tarea.objects.all()
        datos = []

        for tarea in tareas:
            datos.append({
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'completada': tarea.completada
            })

        return Response(datos, status.HTTP_200_OK)

    def post(self, request):

        titulo = request.data.get('titulo')
        descripcion = request.data.get('descripcion')
        completada = request.data.get('completada', False)

        #validar que los campos obligaroios tengan datos
        if not titulo or not descripcion:
            return Response({
                'error': 'el título y la descripción son obligatorias'
            }, status = status.HTTP_400_BAD_REQUEST)

        #crear y cuardar la tarea en la BD
        tarea = Tarea.objects.create(
            titulo = titulo,
            descripcion = descripcion,
            completada = completada
        )

        #Devolver la tarea creada

        return Response({
            'mensaje': 'Tarea creada correctamente',
            'tarea': {
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'completada': tarea.completada
            }
        }, status = status.HTTP_201_CREATED)

class TareaDetalleApiView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #GET: consultat una tarea por id
    def get(self, request, id):
        tarea = get_object_or_404(Tarea, id=id)

        return Response({
            'id': tarea.id,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'completada': tarea.completada
        }, status=status.HTTP_200_OK)

    #DELETE eliminar una tarea
    def delete(self, request, id):
        tarea = get_object_or_404(Tarea, id=id)
        tarea.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)