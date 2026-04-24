from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('Mueble', 'Mueble'),
        ('Colchon', 'Colchón'),
        ('Somier', 'Somier'),
        ('Living', 'Living'),
        ('Cocina', 'Cocina'),
    ]

    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    en_oferta = models.BooleanField(default=False)
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.nombre