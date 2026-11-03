from rest_framework import serializers
from .models import Plan


class PlanSerializer(serializers.ModelSerializer):

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "El precio no puede ser negativo."
            )
        return value

    def validate_duracion_dias(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "La duración debe ser mayor que cero."
            )
        return value

    class Meta:
        model = Plan
        fields = '__all__'