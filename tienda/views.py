from .models import Producto
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

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
    productos = Producto.objects.all()

    categoria = request.GET.get('categoria')
    buscar = request.GET.get('buscar')
    ordenar = request.GET.get('ordenar')
    oferta = request.GET.get('oferta')

    if categoria:
        productos = productos.filter(categoria=categoria)

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    if oferta:
        productos = productos.filter(en_oferta=True)

    if ordenar == "menor":
        productos = productos.order_by("precio")
    elif ordenar == "mayor":
        productos = productos.order_by("-precio")

    paginator = Paginator(productos, 9)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    return render(request, "tienda/catalogo.html", {
        "productos": productos,
        "categorias": Producto.CATEGORIAS,
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
