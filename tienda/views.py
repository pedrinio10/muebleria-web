from .models import Producto
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
    categoria = request.GET.get('categoria', '')

    productos = Producto.objects.all().order_by('nombre')

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    if categoria:
        productos = productos.filter(categoria=categoria)

    return render(request, 'tienda/panel_productos.html', {
        'productos': productos,
        'buscar': buscar,
        'categoria_actual': categoria,
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

@staff_member_required
def editar_producto_panel(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.categoria = request.POST.get("categoria")
        producto.tipo_colchon = request.POST.get("tipo_colchon", "")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio") or 0
        producto.stock = request.POST.get("stock") or 0
        producto.en_oferta = request.POST.get("en_oferta") == "on"
        producto.precio_oferta = request.POST.get("precio_oferta") or None
        producto.mostrar_cuotas = request.POST.get("mostrar_cuotas") == "on"

        if request.FILES.get("imagen"):
            producto.imagen = request.FILES.get("imagen")

        if request.FILES.get("imagen_2"):
            producto.imagen_2 = request.FILES.get("imagen_2")

        if request.FILES.get("imagen_3"):
            producto.imagen_3 = request.FILES.get("imagen_3")

        producto.save()

        messages.success(request, "Producto actualizado correctamente.")
        return redirect("panel_productos")

    return render(request, "tienda/panel_editar_producto.html", {
        "producto": producto,
        "categorias": Producto.CATEGORIAS,
        "tipos_colchon": Producto.TIPOS_COLCHON,
    })

@staff_member_required
def agregar_producto_panel(request):
    if request.method == "POST":
        producto = Producto()

        producto.nombre = request.POST.get("nombre")
        producto.categoria = request.POST.get("categoria")
        producto.tipo_colchon = request.POST.get("tipo_colchon", "")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio") or 0
        producto.stock = request.POST.get("stock") or 0
        producto.en_oferta = request.POST.get("en_oferta") == "on"
        producto.precio_oferta = request.POST.get("precio_oferta") or None
        producto.mostrar_cuotas = request.POST.get("mostrar_cuotas") == "on"

        if request.FILES.get("imagen"):
            producto.imagen = request.FILES.get("imagen")

        if request.FILES.get("imagen_2"):
            producto.imagen_2 = request.FILES.get("imagen_2")

        if request.FILES.get("imagen_3"):
            producto.imagen_3 = request.FILES.get("imagen_3")

        producto.save()

        messages.success(request, "Producto agregado correctamente.")
        return redirect("panel_productos")

    return render(request, "tienda/panel_agregar_producto.html", {
        "categorias": Producto.CATEGORIAS,
        "tipos_colchon": Producto.TIPOS_COLCHON,
    })
def ingresar(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("inicio")

        error = "Usuario o contraseña incorrectos."

    return render(
        request,
        "tienda/login.html",
        {"error": error}
    )