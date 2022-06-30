from doctest import OutputChecker
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import F,Sum, FloatField

# Create your models here.

def cargarFoto(instance, filename):
    return 'fotos/foto_{0}_{1}'.format(instance.idProducto, filename)

class Producto(models.Model):
    idProducto = models.CharField(max_length=5, primary_key=True)
    nombreProducto = models.CharField(max_length=30, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)
    foto = models.ImageField(upload_to=cargarFoto, blank=True, null=True)

    def __str__(self):
        return self.idProducto

class Estado(models.Model):
    id_estado  = models.AutoField(db_column='idEstado', primary_key=True)  
    estado     = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return str(self.estado)

User =get_user_model()

class Venta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    estado = models.ForeignKey(Estado,default=2,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    @property
    def total(self):
        return self.detalleventa_set.aggregate(
            total=Sum(F("precio")*F("cantidad"),output_field=FloatField())

        )["total"]

    class Meta:
        db_table = 'ventas'
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
        ordering = ["id"]

class DetalleVenta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta_id = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f'{self.cantidad} unidades de {self.producto_id.nombreProducto}'

    class Meta:
        db_table = 'detalleventas'
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalle Ventas'
        ordering = ["id"]
