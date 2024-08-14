from app_senauthenticator.models import Programa
from app_senauthenticator.serializers.programa import ProgramaSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def programa_controlador(request, pk=None):
    if pk:
        try:            
            programa = Programa.objects.get(pk=pk)
        except Programa.DoesNotExist:
            return Response({'error': 'Programa no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if request.method == 'GET':
            try:
                serializer = ProgramaSerializer(programa)
                return Response(serializer.data)        
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'PUT':
            try:
                serializer = ProgramaSerializer(programa, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'DELETE':
            try:
                programa.delete()                
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        if request.method == 'GET':
            try:
                programas = Programa.objects.all()
                serializer = ProgramaSerializer(programas, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'POST':
            try:
                serializer = ProgramaSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

