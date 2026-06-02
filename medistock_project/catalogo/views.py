import random
import requests
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Producto
from .serializers import ProductoStockSerializer


class ConsultaStockAPIView(APIView):
    def get(self, request, codigo_producto):
        producto = get_object_or_404(Producto, codigo_producto=codigo_producto)
        alerta_pedido = False
        
        if producto.requiere_reabastecimiento:
            alerta_pedido = True
            try:
                payload = {"sku": producto.codigo_producto, "cantidad_automatica": 500}
                requests.post("https://httpbin.org/post", json=payload, timeout=3)
            except requests.exceptions.RequestException:
                pass

        serializer = ProductoStockSerializer(producto)
        data_respuesta = serializer.data
        data_respuesta['stock_minimo_requerido'] = producto.stock_minimo
        data_respuesta['alerta_reabastecimiento_automatica'] = alerta_pedido
        return Response(data_respuesta, status=status.HTTP_200_OK)


class ProcesarPagoAPIView(APIView):
    def post(self, request):
        monto = request.data.get("monto")
        producto_id = request.data.get("producto_id")
        if not monto or not producto_id:
            return Response({"error": "Parámetros de conciliación ausentes"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = {"amount": float(monto), "currency": "CLP"}
            response = requests.post("https://httpbin.org/post", json=payload, timeout=3)
            if response.status_code == 200:
                return Response({
                    "status": "APPROVED",
                    "authorization_code": f"AUTH-{random.randint(100000, 999999)}",
                    "monto_procesado": monto
                }, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException:
            return Response({"error": "Servicio de adquirencia no disponible"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class GenerarTrackingAPIView(APIView):
    def post(self, request):
        pedido_id = request.data.get("pedido_id")
        comuna_destino = request.data.get("comuna_destino")
        if not pedido_id or not comuna_destino:
            return Response({"error": "Parámetros de distribución incorrectos"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = {"carrier": "CHILEXPRESS", "destination": comuna_destino}
            response = requests.post("https://httpbin.org/post", json=payload, timeout=3)
            if response.status_code == 200:
                return Response({
                    "proveedor_logistica": "Chilexpress S.A.",
                    "numero_seguimiento": f"CHI-{random.randint(10000000, 99999999)}",
                    "estado_envio": "Confirmado - En centro de distribución"
                }, status=status.HTTP_201_CREATED)
        except requests.exceptions.RequestException:
            return Response({"error": "Gateway de transportista fuera de línea"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


def vista_tienda(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo/tienda.html', {'productos': productos})