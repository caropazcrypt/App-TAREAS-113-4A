from django.urls import path
from . import views


urlpatterns = [
    #pagina principal de login
    path('', views.login_pagina, name= 'login_pagina'),

    #lista tareas
    path('tareas/', views.inicio, name ='inicio'),
    path('crear/', views.crear_tarea, name='crear_tarea'),
    path('detalle/<int:id>/', views.detalle_tarea, name='detalle_tarea'),
    path('editar/<int:id>/', views.editar_tarea, name='editar_tarea'),
    path('eliminar/<int:id>/', views.eliminar_tarea, name='eliminar_tarea'),

    #API REST para authenticacion
    path('api/login/', views.LoginAPIView.as_view(), name='login_api'),

    #API REST para listar tareas
    path('api/tareas/', views.TareasApiView.as_view(), name='api_tareas'),

    #API detalle tareas
    path('api/tareas/<int:id>/', views.TareaDetalleApiView.as_view(), name='api_tareas_detalle')
    ]