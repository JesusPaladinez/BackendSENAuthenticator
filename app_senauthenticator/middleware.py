from django.utils.deprecation import MiddlewareMixin

# Este middleware extrae el token jwt-access de las cookies y lo coloca en la 
# cabecera de autorización para que Django lo procese como si hubiera sido enviado desde el frontend en el encabezado Authorization.
class JWTAuthFromCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('jwt-access')
        if access_token:
            # Si hay un token de acceso en las cookies, añadirlo a la cabecera de autorización
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
