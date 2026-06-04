from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path("producto/<int:id>/", views.detalle_producto, name="detalle_producto"),
    path('panel/', views.panel_admin, name='panel_admin'),
]