from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Producto

class MediStockCompletoTestCase(APITestCase):

    def setUp(self):
    
        self.user = User.objects.create_user(username='tester', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        

        self.producto = Producto.objects.create(
            codigo_producto='MED-TEST-99',
            nombre='Catéter de Prueba',
            precio_unitario=2500.00,
            stock_minimo=15
        )

    def test_01_consulta_stock_api_propia(self):
        """Valida que el endpoint propio retorne los datos del stock en tiempo real"""
        url = reverse('consulta-stock', kwargs={'codigo_producto': self.producto.codigo_producto})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['codigo_producto'], 'MED-TEST-99')

    def test_02_integracion_pasarela_pagos(self):
        """Valida el consumo simulado del WebService de pagos (Integración 1)"""
        url = reverse('procesar-pago')
        data = {"monto": 50000, "producto_id": self.producto.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'APPROVED')

    def test_03_integracion_logistica_tracking(self):
        """Valida el consumo simulado del servicio de Chilexpress/Shippo (Integración 2)"""
        url = reverse('generar-tracking')
        data = {"pedido_id": "PED-10024", "comuna_destino": "Santiago"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('numero_seguimiento', response.data)