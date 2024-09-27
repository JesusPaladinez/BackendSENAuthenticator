from app_senauthenticator.models import Objeto
from app_senauthenticator.serializers.objeto import ObjetoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pyrebase
import json


# Configuración de Firebase
config = {
    "apiKey": "AIzaSyAq7WwHvbgox2xJQHqK9yPYfrK3gpPt4K4",
    "authDomain": "projectstoragesenauthenticator.firebaseapp.com",
    "projectId": "projectstoragesenauthenticator",
    "storageBucket": "projectstoragesenauthenticator.appspot.com",
    "messagingSenderId": "371522976959",
    "appId": "1:371522976959:web:f99bc5b20a440aaac5da0a",
    "measurementId": "G-5TEEM4Y3P3",
    "service_account": "clave_cuenta_servicio.json",
    "databaseURL": "https://projectstoragesenauthenticator-default-rtdb.firebaseio.com/"
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()


@api_view(['GET', 'POST'])
def objetos_controlador(request):
    if request.method == 'GET':
        return obtener_objetos(request._request)
    elif request.method == 'POST':
        return crear_objeto(request._request)


@api_view(['GET', 'PUT', 'DELETE'])
def objetos_detalle_controlador(request, pk):
    if request.method == 'GET':
        return obtener_objeto(request._request, pk)
    elif request.method == 'PUT':
        return actualizar_objeto(request._request, pk)
    elif request.method == 'DELETE':
        return eliminar_objeto(request._request, pk)


@api_view(['GET'])
def obtener_objetos(request):
    try:
        objetos = Objeto.objects.all()
        serializer = ObjetoSerializer(objetos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': f'Error al obtener objetos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def crear_objeto(request):
    try:
        if 'foto_objeto' in request.FILES:
            foto = request.FILES['foto_objeto']
            file_bytes = foto.read()

            # Subir el archivo a Firebase Storage
            storage_path = f"objetos/{foto.name}"
            storage.child(storage_path).put(file_bytes)

            # Obtener la URL pública del archivo subido (sin token)
            image_metadata = storage.child(storage_path).get_url(None)

            # Obtener la metadata del archivo almacenado
            metadata = storage.child(storage_path).get_metadata()

            # El token de descarga se encuentra en 'downloadTokens' en los metadatos
            token = json.loads(metadata['downloadTokens'])[0]  # Obtener el token de la metadata
            image_url = f"{image_metadata}&token={token}"  # Construir la URL con el token

            # Asignar la URL de la imagen al campo 'foto_objeto' en el request
            request.data['foto_objeto'] = image_url

        # Serializar y guardar los datos
        serializer = ObjetoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': f'Error general: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def obtener_objeto(request, pk):
    try:
        objeto = Objeto.objects.get(pk=pk)
        serializer = ObjetoSerializer(objeto)
        return Response(serializer.data)
    except Objeto.DoesNotExist:
        return Response({'error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error al obtener objeto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def actualizar_objeto(request, pk):
    try:
        objeto = Objeto.objects.get(pk=pk)

        if 'foto_objeto' in request.FILES:
            foto = request.FILES['foto_objeto']
            file_bytes = foto.read()

            # Subir el archivo a Firebase Storage
            storage_path = f"objetos/{foto.name}"
            storage.child(storage_path).put(file_bytes)

            # Obtener la metadata del archivo, incluyendo el token
            image_metadata = storage.child(storage_path).get_url(None)
            token = storage.child(storage_path).get('downloadTokens')
            image_url = f"{image_metadata}&token={token}"

            request.data['foto_objeto'] = image_url

        serializer = ObjetoSerializer(objeto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Objeto.DoesNotExist:
        return Response({'error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error al actualizar objeto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def eliminar_objeto(request, pk):
    try:
        objeto = Objeto.objects.get(pk=pk)
        objeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Objeto.DoesNotExist:
        return Response({'error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error al eliminar objeto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
