from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Desatamos el modelo por defecto para personalizarlo si es necesario en el futuro
admin.site.unregister(User)
admin.site.register(User, UserAdmin)