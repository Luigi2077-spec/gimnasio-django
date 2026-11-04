from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class PruebasLoginWeb(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='tester',
            password='clave-segura-123',
        )

    def test_inicio_redirige_sin_sesion(self):
        respuesta = self.client.get('/')
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/login/', respuesta.url)

    def test_socios_redirige_sin_sesion(self):
        respuesta = self.client.get('/socios/')
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/login/', respuesta.url)

    def test_socios_accesible_con_sesion(self):
        self.client.login(username='tester', password='clave-segura-123')
        respuesta = self.client.get('/socios/')
        self.assertEqual(respuesta.status_code, 200)


class PruebasAutenticacionApi(TestCase):

    def setUp(self):
        self.api = APIClient()
        self.usuario = User.objects.create_user(
            username='tester',
            password='clave-segura-123',
        )

    def test_login_correcto_entrega_token(self):
        respuesta = self.api.post(
            '/api/login/',
            {'username': 'tester', 'password': 'clave-segura-123'},
            format='json',
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('token', respuesta.data)

    def test_login_incorrecto_devuelve_401(self):
        respuesta = self.api.post(
            '/api/login/',
            {'username': 'tester', 'password': 'mala-clave'},
            format='json',
        )
        self.assertEqual(respuesta.status_code, 401)

    def test_login_sin_datos_devuelve_400(self):
        respuesta = self.api.post('/api/login/', {}, format='json')
        self.assertEqual(respuesta.status_code, 400)

    def test_api_sin_token_devuelve_401(self):
        respuesta = self.api.get('/planes/api/planes/')
        self.assertEqual(respuesta.status_code, 401)

    def test_logout_con_token_lo_elimina(self):
        token = Token.objects.create(user=self.usuario)
        self.api.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        respuesta = self.api.post('/api/logout/')

        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Token.objects.filter(key=token.key).exists())

    def test_token_revocado_devuelve_401(self):
        token = Token.objects.create(user=self.usuario)
        self.api.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.api.post('/api/logout/')

        respuesta = self.api.get('/planes/api/planes/')

        self.assertEqual(respuesta.status_code, 401)