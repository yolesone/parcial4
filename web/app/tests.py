from django.test import TestCase
from django.db import models
from django.conf import settings

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
        return self.idProducto+", "+self.nombreProducto+", "+str(self.stock)\
            + ", "+str(self.precio)+", "+str(self.activo) + \
            ", "+self.foto.__str__()