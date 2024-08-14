from app_senauthenticator.models import RegistroFacial
from app_senauthenticator.serializers.registro_facial import RegistroFacialSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 


@api_view(['GET', 'POST', 'PUT', 'DELETE']) 
def registro_facial_controlador(request, pk=None): 
    if pk:
        try:            
            registro_facial = RegistroFacial.objects.get(pk=pk) 
        except RegistroFacial.DoesNotExist:
            return Response({'error': 'Registro facial no encontrado'}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if request.method == 'GET':
            try:
                serializer = RegistroFacialSerializer(registro_facial)
                return Response(serializer.data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        elif request.method == 'PUT':
            try:
                serializer = RegistroFacialSerializer(registro_facial, data=request.data) 
                if serializer.is_valid(): 
                    serializer.save() 
                    return Response(serializer.data, status=status.HTTP_200_OK) 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        elif request.method == 'DELETE':
            try:
                registro_facial.delete() 
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

    else:
        if request.method == 'GET':
            try:
                registros_faciales = RegistroFacial.objects.all() 
                serializer = RegistroFacialSerializer(registros_faciales, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'POST':
            try:
                serializer = RegistroFacialSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)