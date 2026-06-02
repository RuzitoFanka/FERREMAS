from django.contrib import admin
from django.urls import path
from catalogo.views import ConsultaStockAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    
   
    path('api/v1/productos/<str:codigo_producto>/', ConsultaStockAPIView.as_view(), name='consulta-stock'),
]
