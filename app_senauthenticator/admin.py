from django.contrib import admin
from .models import RegistroFacial, Programa, Ficha, Usuario, Objeto, Tutor, Ingreso

# Register your models here.
admin.site.register(RegistroFacial)
admin.site.register(Programa)
admin.site.register(Ficha)
admin.site.register(Usuario)
admin.site.register(Objeto)
admin.site.register(Tutor)
admin.site.register(Ingreso)