from django.db import models

class Producto(models.Model):
    codigo_producto = models.CharField(max_length=50, unique=True, verbose_name="Código Crítico (SKU)")
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo_producto} - {self.nombre}"

    @property
    def stock_total(self):
        return sum(item.stock for item in self.existencias.all())

    @property
    def tiene_stock(self):
        return self.stock_total > 0


class Bodega(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre


class BodegaStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="existencias")
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'bodega')

    def __str__(self):
        return f"{self.producto.nombre} en {self.bodega.nombre}: {self.stock} unidades"