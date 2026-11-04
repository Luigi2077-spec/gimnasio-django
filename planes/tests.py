from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Plan


class PruebasApiPlanes(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='tester_planes',
            password='clave-segura-123',
        )
        token = Token.objects.create(user=self.usuario)
        self.api = APIClient()
        self.api.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        self.plan = Plan.objects.create(
            nombre='Plan Mensual',
            precio=20000,
            duracion_dias=30,
        )

    def test_listar_planes_con_token(self):
        respuesta = self.api.get('/planes/api/planes/')
        self.assertEqual(respuesta.status_code, 200)

    def test_detalle_plan_existente(self):
        respuesta = self.api.get(f'/planes/api/planes/{self.plan.pk}/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['nombre'], 'Plan Mensual')

    def test_detalle_plan_inexistente_devuelve_404(self):
        respuesta = self.api.get('/planes/api/planes/999999/')
        self.assertEqual(respuesta.status_code, 404)