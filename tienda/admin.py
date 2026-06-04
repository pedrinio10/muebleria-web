from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Producto
from import_export.admin import ImportExportModelAdmin
from django.urls import path
from django.shortcuts import redirect

@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):

    # COLUMNAS DEL LISTADO
    list_display = (
        'miniatura',
        'nombre',
        'categoria',
        'precio',
        'botones_stock',
        'oferta_color',
    )

    # CAMPOS EDITABLES DIRECTO
    list_editable = (
        'precio',
    )

    # BÚSQUEDA
    search_fields = (
        'nombre',
        'descripcion',
    )

    # FILTROS LATERALES
    list_filter = (
        'categoria',
        'en_oferta',
    )

    # ORDEN
    ordering = ('nombre',)

    # PAGINACIÓN
    list_per_page = 25

    # CAMPOS DEL FORMULARIO
    fieldsets = (

        ('🛋 Datos del producto', {
            'fields': (
                'nombre',
                'categoria',
                'descripcion',
                'tipo_colchon',
            )
        }),

        ('💰 Ventas', {
            'fields': (
                'precio',
                'stock',
                'mostrar_cuotas',
                'en_oferta',
                'precio_oferta',
            )
        }),

        ('🖼 Imágenes', {
            'fields': (
                'imagen',
                'imagen_2',
                'imagen_3',
                'preview_imagen',
            )
        }),

    )

    readonly_fields = (
        'preview_imagen',
    )

    # ---------- FUNCIONES VISUALES ----------

    def miniatura(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:12px; object-fit:cover;">',
                obj.imagen.url
            )
        return "Sin imagen"

    miniatura.short_description = "Foto"

    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="250" style="border-radius:18px;">',
                obj.imagen.url
            )
        return "Sin imagen cargada"

    preview_imagen.short_description = "Vista previa"

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                '<int:producto_id>/sumar-stock/',
                self.admin_site.admin_view(self.sumar_stock),
                name='sumar_stock',
            ),
            path(
                '<int:producto_id>/restar-stock/',
                self.admin_site.admin_view(self.restar_stock),
                name='restar_stock',
            ),
        ]

        return custom_urls + urls

    def sumar_stock(self, request, producto_id):
        producto = Producto.objects.get(id=producto_id)
        producto.stock += 1
        producto.save()
        return redirect(request.META.get('HTTP_REFERER', '../'))

    def restar_stock(self, request, producto_id):
        producto = Producto.objects.get(id=producto_id)

        if producto.stock > 0:
            producto.stock -= 1
            producto.save()

        return redirect(request.META.get('HTTP_REFERER', '../'))

    def botones_stock(self, obj):
        return format_html(
            '<a class="button" style="background:#dc3545;color:white;padding:4px 9px;border-radius:6px;text-decoration:none;" href="{}">−</a> '
            '<span style="font-weight:bold;margin:0 8px;">{}</span>'
            '<a class="button" style="background:#198754;color:white;padding:4px 9px;border-radius:6px;text-decoration:none;" href="{}">+</a>',
            f'{obj.id}/restar-stock/',
            obj.stock,
            f'{obj.id}/sumar-stock/',
        )

    botones_stock.short_description = "Stock rápido"

    def stock_color(self, obj):
        if obj.stock <= 2:
            return format_html(
                '<span style="color:red; font-weight:bold;">{} ⚠</span>',
                obj.stock
            )
        elif obj.stock <= 5:
            return format_html(
                '<span style="color:orange; font-weight:bold;">{}</span>',
                obj.stock
            )
        return format_html(
            '<span style="color:green; font-weight:bold;">{}</span>',
            obj.stock
        )

    stock_color.short_description = "Stock"

    def oferta_color(self, obj):
        if obj.en_oferta:
            return "🔥 Sí"
        return "—"

    oferta_color.short_description = "Oferta"

    # ---------- VALIDACIONES ----------

    def save_model(self, request, obj, form, change):

        if obj.en_oferta and not obj.precio_oferta:
            messages.warning(
                request,
                "Marcaste oferta pero no pusiste precio oferta."
            )

        super().save_model(request, obj, form, change)

        messages.success(
            request,
            "Producto guardado correctamente ✅"
        )