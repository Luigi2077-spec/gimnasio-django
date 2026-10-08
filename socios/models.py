
from django.db import models


class Socio(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    plan = models.ForeignKey(
        'planes.Plan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='socios'
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
