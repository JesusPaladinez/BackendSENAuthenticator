from app_senauthenticator.models import Objeto
from app_senauthenticator.serializers.objeto import ObjetoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def objeto_controlador(request, pk=None):
    if pk:
        try:
            objeto = Objeto.objects.get(pk=pk)
        except Objeto.DoesNotExist:
            return Response({'error': 'Objeto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if request.method == 'GET':
            try:
                serializer = ObjetoSerializer(objeto)
                return Response(serializer.data)                
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'PUT':
            try:
                serializer = ObjetoSerializer(objeto, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        elif request.method == 'DELETE':
            try:
                objeto.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        if request.method == 'GET':
            try:
                objetos = Objeto.objects.all()
                serializer = ObjetoSerializer(objetos, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'POST':
            try:
                serializer = ObjetoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

