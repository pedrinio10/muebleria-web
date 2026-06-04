from .models import Producto
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required


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
    ordenar = request.GET.get('ordenar')
    oferta = request.GET.get('oferta')
    tipo_colchon = request.GET.get('tipo_colchon')

    productos = Producto.objects.all().order_by("-precio")

    if categoria:
        productos = productos.filter(categoria=categoria)

    if tipo_colchon:
        productos = productos.filter(tipo_colchon=tipo_colchon)

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    if oferta:
        productos = productos.filter(en_oferta=True)

    if ordenar == "menor":
        productos = productos.order_by("precio")
    elif ordenar == "mayor":
        productos = productos.order_by("-precio")
    else:
        productos = productos.order_by("-precio")

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

@staff_member_required
def panel_admin(request):
    total_productos = Producto.objects.count()
    productos_stock = Producto.objects.filter(stock__gt=0).count()
    productos_sin_stock = Producto.objects.filter(stock=0).count()
    productos_oferta = Producto.objects.filter(en_oferta=True).count()

    contexto = {
        'total_productos': total_productos,
        'productos_stock': productos_stock,
        'productos_sin_stock': productos_sin_stock,
        'productos_oferta': productos_oferta,
    }

    return render(request, 'tienda/panel.html', contexto)

@staff_member_required
def panel_productos(request):
    buscar = request.GET.get('buscar', '')

    productos = Producto.objects.all().order_by('nombre')

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    return render(request, 'tienda/panel_productos.html', {
        'productos': productos,
        'buscar': buscar,
    })


@staff_member_required
def sumar_stock_panel(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.stock += 1
    producto.save()
    return redirect(request.META.get('HTTP_REFERER', 'panel_productos'))


@staff_member_required
def restar_stock_panel(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if producto.stock > 0:
        producto.stock -= 1
        producto.save()

    return redirect(request.META.get('HTTP_REFERER', 'panel_productos'))
