from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):

    usuario = request.data.get('username')
    contrasena = request.data.get('password')

    if not usuario or not contrasena:
        return Response(
            {'error': 'Debes ingresar usuario y contraseña.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(
        request,
        username=usuario,
        password=contrasena
    )

    if user is None:
        return Response(
            {'error': 'Usuario o contraseña incorrectos.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, creado = Token.objects.get_or_create(user=user)

    return Response(
        {
            'mensaje': 'Inicio de sesión exitoso.',
            'token': token.key,
            'usuario': user.username
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):

    request.auth.delete()

    return Response(
        {'mensaje': 'Sesión cerrada correctamente.'},
        status=status.HTTP_200_OK
    )