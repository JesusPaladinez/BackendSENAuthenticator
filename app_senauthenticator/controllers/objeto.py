from app_senauthenticator.models import Objeto
from app_senauthenticator.serializers.objeto import ObjetoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 
import pyrebase

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
  "databaseURL":"https://projectstoragesenauthenticator-default-rtdb.firebaseio.com/"
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def objeto_controlador(request, pk=None):
    if pk:
        try:
            objeto = Objeto.objects.get(pk=pk)
        except Objeto.DoesNotExist:
            return Response({'error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ObjetoSerializer(objeto)
            return Response(serializer.data)

        elif request.method == 'PUT':
            if 'foto_objeto' in request.FILES:
                foto = request.FILES['foto_objeto']
                file_bytes = foto.read()  # Leer el archivo directamente

                # Subir el archivo a Firebase Storage directamente
                storage_path = f"objetos/{foto.name}"
                storage.child(storage_path).put(file_bytes)  # Subir los bytes del archivo
                image_url = storage.child(storage_path).get_url(None)  # Obtener la URL

                # Actualizar el campo de imagen en la solicitud
                request.data['foto_objeto'] = image_url
            
            serializer = ObjetoSerializer(objeto, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            objeto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        if request.method == 'GET':
            objetos = Objeto.objects.all()
            serializer = ObjetoSerializer(objetos, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            try:
                if 'foto_objeto' in request.FILES:
                    foto = request.FILES['foto_objeto']
                    file_bytes = foto.read()  # Leer el archivo directamente

                    # Subir el archivo a Firebase Storage
                    storage_path = f"objetos/{foto.name}"
                    storage.child(storage_path).put(file_bytes)  # Subir los bytes del archivo
                    image_url = storage.child(storage_path).get_url(None)  # Obtener la URL

                    # Agregar la URL de la imagen al request data
                    request.data['foto_objeto'] = image_url

                # Serializar y guardar los datos
                serializer = ObjetoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'error': f'Error general: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
