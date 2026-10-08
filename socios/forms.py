
from django import forms
from .models import Socio


class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio

        fields = [
            'nombre',
            'apellido',
            'rut',
            'correo',
            'telefono',
            'activo',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del socio',
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del socio',
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12.345.678-5',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678',
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        
    def clean_rut(self):
        rut = self.cleaned_data['rut']

        # Eliminar puntos, guiones y espacios
        rut = rut.replace('.', '').replace('-', '').replace(' ', '').upper()

        # Comprobar que tenga al menos 2 caracteres
        if len(rut) < 2:
            raise forms.ValidationError('El RUT ingresado no es válido.')

        numero = rut[:-1]
        digito_verificador = rut[-1]

        # Verificar que el cuerpo del RUT sea numérico
        if not numero.isdigit():
            raise forms.ValidationError('El RUT debe contener números válidos.')

        # Calcular dígito verificador mediante módulo 11
        suma = 0
        multiplicador = 2

        for digito in reversed(numero):
            suma += int(digito) * multiplicador
            multiplicador += 1

            if multiplicador > 7:
                multiplicador = 2

        resultado = 11 - (suma % 11)

        if resultado == 11:
            digito_calculado = '0'
        elif resultado == 10:
            digito_calculado = 'K'
        else:
            digito_calculado = str(resultado)

        if digito_verificador != digito_calculado:
            raise forms.ValidationError('El dígito verificador del RUT es incorrecto.')

        # Guardar el RUT en formato normalizado
        return f'{numero}-{digito_verificador}'
    
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']

        # Eliminar espacios y guiones
        telefono = telefono.replace(' ', '').replace('-', '')

        # Comprobar formato de celular chileno
        if not telefono.startswith('+569'):
            raise forms.ValidationError(
                'El teléfono debe comenzar con +569.'
            )

        # Comprobar que tenga exactamente 12 caracteres
        if len(telefono) != 12:
            raise forms.ValidationError(
                'El teléfono debe tener el formato +569XXXXXXXX.'
            )

        # Comprobar que después del + sean solo números
        if not telefono[1:].isdigit():
            raise forms.ValidationError(
                'El teléfono solo debe contener números.'
            )

        return telefono


