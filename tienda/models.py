from django.db import models


class Producto(models.Model):

    CATEGORIAS = [
        ('Mueble', 'Muebles'),
        ('Colchon', 'Colchones y Sommier'),
        ('Living', 'Living'),
        ('Cocina', 'Cocina'),
        ('Respaldar', 'Respaldares'),
        ('Almohadas', 'Almohadas'),
    ]

    nombre = models.CharField("Nombre", max_length=200)
    mostrar_cuotas = models.BooleanField("Mostrar cuotas", default=False)

    categoria = models.CharField(
        "Categoría",
        max_length=50,
        choices=CATEGORIAS
    )

    precio = models.DecimalField(
        "Precio",
        max_digits=10,
        decimal_places=2
    )

    stock = models.IntegerField(
        "Stock",
        default=0
    )

    descripcion = models.TextField(
        "Descripción"
    )

    imagen = models.ImageField(
        "Imagen",
        upload_to='productos/',
        blank=True,
        null=True
    )

    en_oferta = models.BooleanField(
        "En oferta",
        default=False
    )

    precio_oferta = models.DecimalField(
        "Precio oferta",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre