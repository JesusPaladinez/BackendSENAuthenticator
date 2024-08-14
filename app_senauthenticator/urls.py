from django.urls import path
from app_senauthenticator.controllers import programa, ficha, usuario, registro_facial, objeto, ingreso, tutor
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('programa/', programa.programa_controlador),
    path('programa/<int:pk>/', programa.programa_controlador),
    path('ficha/', ficha.ficha_controlador),
    path('ficha/<int:pk>/', ficha.ficha_controlador),
    path('usuario/', usuario.usuario_controlador),
    path('usuario/<int:pk>/', usuario.usuario_controlador),
    path('registroFacial/', registro_facial.registro_facial_controlador),
    path('registroFacial/<int:pk>/', registro_facial.registro_facial_controlador),
    path('objeto/', objeto.objeto_controlador),
    path('objeto/<int:pk>/', objeto.objeto_controlador),
    path('tutor/', tutor.tutor_controlador),
    path('tutor/<int:pk>/', tutor.tutor_controlador),
    path('ingreso/', ingreso.ingreso_controlador),
    path('ingreso/<int:pk>/', ingreso.ingreso_controlador),
    path('inicioSesion/', usuario.inicio_sesion),
    path('perfil/', usuario.perfil)
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
