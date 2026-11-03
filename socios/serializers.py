
from rest_framework import serializers
from django import forms

from .models import Socio
from .forms import validar_rut, validar_telefono


class SocioSerializer(serializers.ModelSerializer):

    def validate_rut(self, value):
        try:
            return validar_rut(value)
        except forms.ValidationError as error:
            raise serializers.ValidationError(error.messages)

    def validate_telefono(self, value):
        try:
            return validar_telefono(value)
        except forms.ValidationError as error:
            raise serializers.ValidationError(error.messages)

    class Meta:
        model = Socio
        fields = '__all__'
