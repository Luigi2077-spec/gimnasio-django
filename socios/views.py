from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Socio
from .forms import SocioForm
from .serializers import SocioSerializer


# ==========================================
# VISTAS WEB DE SOCIOS
# ==========================================
@login_required

def lista_socios(request):
    socios = Socio.objects.select_related('plan').all()

    return render(request, 'socios/lista_socios.html', {
        'socios': socios
    })


def crear_socio(request):
    if request.method == 'POST':
        formulario = SocioForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_socios')
    else:
        formulario = SocioForm()

    return render(request, 'socios/crear_socio.html', {
        'form': formulario,
        'formulario': formulario
    })


def editar_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk)

    if request.method == 'POST':
        formulario = SocioForm(request.POST, instance=socio)

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_socios')
    else:
        formulario = SocioForm(instance=socio)

    return render(request, 'socios/editar_socio.html', {
        'form': formulario,
        'formulario': formulario,
        'socio': socio
    })


def eliminar_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk)

    if request.method == 'POST':
        socio.delete()
        return redirect('lista_socios')

    return render(request, 'socios/eliminar_socio.html', {
        'socio': socio
    })


# ==========================================
# API REST DE SOCIOS
# ==========================================

@api_view(['GET', 'POST'])
def api_lista_socios(request):

    # GET: listar todos los socios
    if request.method == 'GET':
        socios = Socio.objects.select_related('plan').all()
        serializer = SocioSerializer(socios, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST: registrar un nuevo socio
    elif request.method == 'POST':
        serializer = SocioSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'DELETE'])
def api_detalle_socio(request, pk):

    # Buscar socio por su ID
    try:
        socio = Socio.objects.get(pk=pk)

    except Socio.DoesNotExist:
        return Response(
            {'error': 'El socio no existe.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET: consultar un socio
    if request.method == 'GET':
        serializer = SocioSerializer(socio)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # PUT: actualizar un socio
    elif request.method == 'PUT':
        serializer = SocioSerializer(
            socio,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: eliminar un socio
    elif request.method == 'DELETE':
        socio.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
