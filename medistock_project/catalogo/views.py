from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Producto
from .serializers import ProductoStockSerializer

class ConsultaStockAPIView(APIView):
    def get(self, request, codigo_producto):
  
        producto = get_object_or_404(Producto, codigo_producto=codigo_producto)
        serializer = ProductoStockSerializer(producto)

        return Response(serializer.data, status=status.HTTP_200_OK)