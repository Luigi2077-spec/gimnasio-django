
from django.shortcuts import render, redirect, get_object_or_404
from .models import Socio
from .forms import SocioForm


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
