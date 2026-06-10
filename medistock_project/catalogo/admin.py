from django.contrib import admin
from django.db import models
from django import forms
from .models import Producto, Bodega, BodegaStock

# 🛡️ Configuración avanzada para el panel de Administración de Productos
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Sobreescribe el cuadro de texto visual en el navegador.
    # Fuerza a que el mínimo permitido sea 0, impidiendo bajar a negativos con las flechas.
    formfield_overrides = {
        models.DecimalField: {
            'widget': forms.NumberInput(attrs={
                'min': '0', 
                'step': '1',
                'style': 'width: 150px;'
            })
        },
    }
    
    # Columnas visibles en el listado del administrador
    list_display = ('codigo_producto', 'nombre', 'precio_unitario', 'stock_minimo')
    search_fields = ('codigo_producto', 'nombre')

# 🏢 Registro del resto de tus modelos para la gestión de inventarios y sucursales
@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(BodegaStock)
class BodegaStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'bodega', 'stock')
    list_filter = ('bodega',)