from rest_framework import serializers
from .models import Producto, BodegaStock

class BodegaStockSerializer(serializers.ModelSerializer):
    nombre_bodega = serializers.CharField(source='bodega.nombre')

    class Meta:
        model = BodegaStock
        fields = ['nombre_bodega', 'stock']

class ProductoStockSerializer(serializers.ModelSerializer):
   
    bodegas = BodegaStockSerializer(many=True, source='existencias', read_only=True)
    disponible = serializers.BooleanField(source='tiene_stock', read_only=True)

    class Meta:
        model = Producto
        fields = ['codigo_producto', 'nombre', 'descripcion', 'precio_unitario', 'stock_total', 'bodegas', 'disponible']