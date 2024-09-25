# Librerías para registrar los datos del usuario
from rest_framework_simplejwt.tokens import RefreshToken  # Importar JWT
from app_senauthenticator.models import UsuarioExterno
from app_senauthenticator.serializers.usuario_externo import UsuarioExternoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def usuario_externo_controlador(request, pk=None):
    try:
        # Si existe la pk se manejan los métodos GET, PUT, DELETE
        if pk:
            usuario = UsuarioExterno.objects.get(pk=pk)  # Se intenta obtener el objeto por su pk

            # Solicitud para obtener un objeto
            if request.method == 'GET':
                serializer = UsuarioExternoSerializer(usuario)  # Serializar el objeto
                return Response(serializer.data)  # Devolver el objeto serializado

            # Solicitud para actualizar un objeto
            elif request.method == 'PUT':
                serializer = UsuarioExternoSerializer(usuario, data=request.data)  # Serializar los datos actualizados
                if serializer.is_valid():
                    serializer.save()  # Guardar los datos actualizados
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Solicitud para eliminar un objeto
            elif request.method == 'DELETE':
                usuario.delete()  # Eliminar el objeto
                return Response(status=status.HTTP_204_NO_CONTENT)

        # Si no existe la pk se manejan los métodos GET, POST
        else:
            # Solicitud para obtener todos los objetos
            if request.method == 'GET':
                usuarios = UsuarioExterno.objects.all()  # Obtener todos los objetos
                serializer = UsuarioExternoSerializer(usuarios, many=True)  # Serializar múltiples objetos
                return Response(serializer.data)

            # Solicitud para crear un nuevo objeto
            elif request.method == 'POST':
                usuario_serializer = UsuarioExternoSerializer(data=request.data)
                if usuario_serializer.is_valid():
                    # Guardar el usuario
                    usuario = usuario_serializer.save()
                    usuario.set_password(request.data['password'])  # Encriptar la contraseña
                    usuario.save()

                    # Generar los tokens JWT
                    refresh = RefreshToken.for_user(usuario)
                    access_token = str(refresh.access_token)

                    # Crear la respuesta con los tokens en cookies
                    response = Response({'usuario': usuario_serializer.data}, status=status.HTTP_201_CREATED)
                    response.set_cookie(
                        key='jwt-access',
                        value=access_token,
                        httponly=True,
                        secure=True,
                        samesite='None'
                    )

                    # Procesar el registro facial si se proporciona una imagen

                    return response
                return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except UsuarioExterno.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error en el controlador de usuario: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
