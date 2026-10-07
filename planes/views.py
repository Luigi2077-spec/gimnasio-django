
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plan
from .forms import PlanForm


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
