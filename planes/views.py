from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Plan
from .forms import PlanForm
from .serializers import PlanSerializer


# ==========================================
# VISTAS WEB DE PLANES
# ==========================================

@login_required

def lista_planes(request):
    planes = Plan.objects.all()

    return render(request, 'planes/lista_planes.html', {
        'planes': planes
    })


def crear_plan(request):
    if request.method == 'POST':
        formulario = PlanForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_planes')
    else:
        formulario = PlanForm()

    return render(request, 'planes/formulario_plan.html', {
        'formulario': formulario
    })


def editar_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    if request.method == 'POST':
        formulario = PlanForm(request.POST, instance=plan)

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_planes')
    else:
        formulario = PlanForm(instance=plan)

    return render(request, 'planes/formulario_plan.html', {
        'formulario': formulario
    })


def eliminar_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    if request.method == 'POST':
        plan.delete()
        return redirect('lista_planes')

    return render(request, 'planes/eliminar_plan.html', {
        'plan': plan
    })


# ==========================================
# API REST DE PLANES
# ==========================================

@api_view(['GET', 'POST'])
def api_lista_planes(request):

    # GET: listar todos los planes
    if request.method == 'GET':
        planes = Plan.objects.all()
        serializer = PlanSerializer(planes, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST: crear un nuevo plan
    elif request.method == 'POST':
        serializer = PlanSerializer(data=request.data)

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
def api_detalle_plan(request, pk):

    # Buscar el plan por su ID
    try:
        plan = Plan.objects.get(pk=pk)

    except Plan.DoesNotExist:
        return Response(
            {'error': 'El plan no existe.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET: consultar un plan
    if request.method == 'GET':
        serializer = PlanSerializer(plan)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # PUT: actualizar un plan
    elif request.method == 'PUT':
        serializer = PlanSerializer(
            plan,
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

    # DELETE: eliminar un plan
    elif request.method == 'DELETE':
        plan.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
