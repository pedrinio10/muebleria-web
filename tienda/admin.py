from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Producto
from import_export.admin import ImportExportModelAdmin

@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):

    # COLUMNAS DEL LISTADO
    list_display = (
        'miniatura',
        'nombre',
        'categoria',
        'precio',
        'stock_color',
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

        ('🖼 Imagen', {
            'fields': (
                'imagen',
                'preview_imagen',
            )
        }),

        ('🛋 Datos del producto', {
            'fields': (
                'nombre',
                'categoria',
                'tipo_colchon',
                'descripcion',
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