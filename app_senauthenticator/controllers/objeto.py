import os
import json
import firebase_admin
from firebase_admin import credentials, storage as admin_storage
from app_senauthenticator.models import Objeto
from app_senauthenticator.serializers.objeto import ObjetoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pyrebase


def initialize_firebase():
    try:
        # Obtener las credenciales desde la variable de entorno
        firebase_credential = os.getenv('FIREBASE_CREDENTIALS')

        # Verificar si las credenciales están presentes
        if not firebase_credential:
            raise Exception("Firebase credentials not found in environment variables")

        # Convertir la cadena JSON de credenciales en un diccionario
        cred_dict = json.loads(firebase_credential)
        cred = credentials.Certificate(cred_dict)

        # Inicializar la aplicación de Firebase con el bucket de almacenamiento
        try:
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'projectstoragesenauthenticator.appspot.com'
            })
        except ValueError as e:
            if 'The default Firebase app already exists' in str(e):
                pass  # La aplicación ya está inicializada, continuar
            else:
                raise e

    except Exception as e:
        # Manejar cualquier otra excepción
        raise e

initialize_firebase()


# Configuración de Firebase con pyrebase
config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": "projectstoragesenauthenticator.firebaseapp.com",
    "projectId": "projectstoragesenauthenticator",
    "storageBucket": "projectstoragesenauthenticator.appspot.com", 
    "messagingSenderId": "371522976959",
    "appId": "1:371522976959:web:f99bc5b20a440aaac5da0a",
    "measurementId": "G-5TEEM4Y3P3",
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

            # Subir el archivo a Firebase Storage usando pyrebase
            storage_path = f"objetos/{foto.name}"
            storage.child(storage_path).put(file_bytes)

            # Obtener la URL pública del archivo subido
            image_metadata = storage.child(storage_path).get_url(None)

            # Obtener el bucket de Firebase Storage con Admin SDK
            bucket = admin_storage.bucket()

            # Obtener el blob (archivo) y los metadatos
            blob = bucket.blob(storage_path)
            blob.reload()  # Cargar los metadatos actuales

            # Verificar si existe el token de descarga en los metadatos
            token = blob.metadata.get('firebaseStorageDownloadTokens')
            if not token:
                raise Exception("Download token not found in blob metadata")

            # Construir la URL completa con el token
            image_url = f"{image_metadata}&token={token}"

            # Asignar la URL de la imagen al campo 'foto_objeto'
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
            bucket = admin_storage.bucket()
            blob = bucket.blob(storage_path)
            blob.reload()  # Cargar los metadatos actuales

            token = blob.metadata.get('firebaseStorageDownloadTokens')
            if not token:
                raise Exception("Download token not found in blob metadata")

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
