from .models import Producto
from django.shortcuts import render, get_object_or_404


def inicio(request):
    categoria = request.GET.get('categoria')

    if categoria:
        productos = Producto.objects.filter(categoria=categoria)
    else:
        productos = Producto.objects.all()[:6]

        ofertas = Producto.objects.filter(en_oferta=True)[:3]

    return render(request, 'tienda/inicio.html', {
        'productos': productos,
        'ofertas': ofertas
    })


def catalogo(request):
    categoria = request.GET.get('categoria')
    buscar = request.GET.get('buscar')

    productos = Producto.objects.all()

    if categoria:
        productos = productos.filter(categoria=categoria)

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    return render(request, 'tienda/catalogo.html', {
        'productos': productos
    })

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    relacionados = Producto.objects.filter(
        categoria=producto.categoria
    ).exclude(id=producto.id)[:3]

    return render(request, 'tienda/detalle.html', {
        'producto': producto,
        'relacionados': relacionados
    })