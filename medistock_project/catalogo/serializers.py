from rest_framework import serializers
from .models import Producto, BodegaStock

class BodegaStockSerializer(serializers.ModelSerializer):
    nombre_bodega = serializers.CharField(source='bodega.nombre')

    class Meta:
        model = BodegaStock
        fields = ['nombre_bodega', 'stock']

class ProductoStockSerializer(serializers.ModelSerializer):
    bodegas = BodegaStockSerializer(source='existencias', many=True, read_only=True)

    disponible = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'codigo_producto', 
            'nombre', 
            'descripcion', 
            'precio_unitario', 
            'stock_total', 
            'stock_minimo',  
            'bodegas', 
            'disponible'
        ]

    def get_disponible(self, obj):
     
        return obj.stock_total > 0