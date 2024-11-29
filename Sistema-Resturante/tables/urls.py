from django.conf import settings 
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "tables"

urlpatterns = [
    path('', views.lista_productos, name='ver'),
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar_carrito/', views.eliminar_producto, name='eliminar_del_carrito'),
    path('disminuir_del_carrito/', views.disminuir_del_carrito, name='disminuir_del_carrito'),
    path('seleccionar_mesa/', views.seleccionar_mesa, name='seleccionar_mesa'),
    path('enviar_carrito/', views.enviar_carrito, name='enviar_carrito'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('atender_carrito/', views.atender_carrito, name='atender_carrito'),
    path('generar_pdf/<int:carrito_id>/', views.generar_pdf, name='generar_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
