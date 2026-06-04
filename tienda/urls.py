from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path("producto/<int:id>/", views.detalle_producto, name="detalle_producto"),
    path('panel/', views.panel_admin, name='panel_admin'),
    path('panel/productos/', views.panel_productos, name='panel_productos'),
    path('panel/productos/<int:producto_id>/sumar-stock/', views.sumar_stock_panel, name='sumar_stock_panel'),
    path('panel/productos/<int:producto_id>/restar-stock/', views.restar_stock_panel, name='restar_stock_panel'),
    path('panel/productos/<int:producto_id>/editar/', views.editar_producto_panel, name='editar_producto_panel'),
    path('panel/productos/agregar/', views.agregar_producto_panel, name='agregar_producto_panel'),
]