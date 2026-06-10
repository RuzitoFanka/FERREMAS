import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producto, BodegaStock

# =========================================================================
# VISTAS DE LAS APIs REST FRAMEWORK
# =========================================================================

class ConsultaStockAPIView(APIView):
    def get(self, request, codigo_producto):
        try:
            producto = Producto.objects.get(codigo_producto=codigo_producto)
            return Response({'codigo': producto.codigo_producto, 'stock': producto.stock_total}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class ProcesarPagoAPIView(APIView):
    def post(self, request):
        return Response({'status': 'pago aprobado'}, status=status.HTTP_200_OK)

class GenerarTrackingAPIView(APIView):
    def post(self, request):
        return Response({'tracking_id': 'MS-123456'}, status=status.HTTP_200_OK)


# =========================================================================
# VISTAS DE LAS PÁGINAS WEB (TEMPLATES HTML)
# =========================================================================

def vista_tienda(request):
    """ Muestra la tienda/catálogo comercial """
    productos = Producto.objects.all()
    return render(request, 'catalogo/tienda.html', {'productos': productos})


def resumen_orden_view(request):
    """ Muestra la nueva pantalla con la lista de productos agregados """
    return render(request, 'catalogo/resumen_orden.html')


def procesar_compra_view(request):
    """ Ejecuta el descuento lógico real sobre las bodegas en la base de datos """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])

            for item in items:
                producto_id = item['id']
                cantidad_comprada = int(item['cantidad'])
                producto = Producto.objects.get(id=producto_id)
                if producto.stock_total < cantidad_comprada:
                    return JsonResponse({'status': 'error', 'message': f"El insumo '{producto.nombre}' no tiene suficiente stock."})

            for item in items:
                producto_id = item['id']
                cantidad_comprada = int(item['cantidad'])
                existencias_bodega = BodegaStock.objects.filter(producto_id=producto_id).order_by('-stock')
                
                por_descontar = cantidad_comprada
                for registro in existencias_bodega:
                    if registro.stock >= por_descontar:
                        registro.stock -= por_descontar
                        registro.save()
                        break
                    else:
                        por_descontar -= registro.stock
                        registro.stock = 0
                        registro.save()

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=400)