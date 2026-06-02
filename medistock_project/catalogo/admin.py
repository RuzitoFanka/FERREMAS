from django.contrib import admin
from .models import Producto, Bodega, BodegaStock

class BodegaStockInline(admin.TabularInline):
    model = BodegaStock
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_producto', 'nombre', 'precio_unitario', 'stock_total')
    search_fields = ('codigo_producto', 'nombre')
    inlines = [BodegaStockInline]

admin.site.register(Bodega)