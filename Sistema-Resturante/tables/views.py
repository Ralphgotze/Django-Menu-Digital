from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Table, Carrito, Categoria

def lista_productos(request):
    # Verificar si se ha seleccionado una mesa
    num_table = request.session.get("num_table")
    if not num_table:
        return redirect("tables:seleccionar_mesa")  # Redirigir si no hay mesa seleccionada

    # Obtener productos, mesa, carrito y categorías
    productos = Product.objects.all()
    table = Table.objects.get(num_table=num_table)
    carrito, _ = Carrito.objects.get_or_create(table=table, enviado=False)
    categoria = Categoria.objects.all()

    # Preparar detalles del carrito y calcular el total
    total_carrito = 0
    carrito_detalle = []
    for producto_id, cantidad in carrito.producto.items():
        producto = Product.objects.get(id=int(producto_id))
        subtotal = cantidad * producto.precio
        total_carrito += subtotal
        carrito_detalle.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio': producto.precio,
            'subtotal': subtotal,
        })

    # Manejar envío del formulario para agregar producto
    if request.method == "POST":
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))

        # Actualizar carrito
        productos = carrito.productos
        if producto_id in productos:
            productos[producto_id] += cantidad
        else:
            productos[producto_id] = cantidad
        carrito.productos = productos
        carrito.save()

        return redirect("lista_productos")  # Actualizar la vista

    return render(request, "index.html", {
        "productos": productos,
        "num_table": num_table,
        "carrito": carrito_detalle,
        "total_carrito": total_carrito,
        "categorias": categoria,
    })


def agregar_al_carrito(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        producto_id = request.POST.get("producto_id")
        num_table = request.session.get("num_table")

        if not num_table:
            return JsonResponse({"error": "Debes seleccionar una mesa primero."}, status=400)

        # Buscar producto y carrito
        producto = get_object_or_404(Product, id=producto_id)
        table = get_object_or_404(Table, num_table=num_table)
        carrito, _ = Carrito.objects.get_or_create(table=table, enviado=False)

        # Actualizar productos en el carrito
        productos = carrito.producto
        if producto_id in productos:
            productos[producto_id] += 1
        else:
            productos[producto_id] = 1
        carrito.productos = productos
        carrito.save()

        # Calcular total de forma optimizada
        total = sum(Product.objects.get(id=int(pid)).precio * cantidad for pid, cantidad in productos.items())

        return JsonResponse({
            "producto": producto.nombre,
            "cantidad": productos[producto_id],
            "subtotal": productos[producto_id] * producto.precio,
            "total": total,
        })
    return JsonResponse({"error": "Solicitud inválida"}, status=400)


def disminuir_del_carrito(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        producto_id = request.POST.get("producto_id")
        num_table = request.session.get("num_table")

        if not num_table:
            return JsonResponse({"error": "Debes seleccionar una mesa primero."}, status=400)

        # Buscar carrito
        table = get_object_or_404(Table, num_table=num_table)
        carrito = get_object_or_404(Carrito, table=table, enviado=False)

        productos = carrito.producto
        if producto_id in productos:
            if productos[producto_id] > 1:
                productos[producto_id] -= 1
            else:
                del productos[producto_id]  # Eliminar producto si cantidad es 0
            carrito.productos = productos
            carrito.save()

        # Calcular total
        total = sum(Product.objects.get(id=int(pid)).precio * cantidad for pid, cantidad in productos.items())

        return JsonResponse({
            "cantidad": productos.get(producto_id, 0),
            "subtotal": productos.get(producto_id, 0) * Product.objects.get(id=int(producto_id)).precio if producto_id in productos else 0,
            "total": total,
        })
    return JsonResponse({"error": "Solicitud inválida"}, status=400)



def eliminar_producto(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        producto_id = request.POST.get("producto_id")
        num_table = request.session.get("num_table")

        if not num_table:
            return JsonResponse({"error": "Debes seleccionar una mesa primero."}, status=400)

        # Buscar carrito
        table = get_object_or_404(Table, num_table=num_table)
        carrito = get_object_or_404(Carrito, table=table, enviado=False)

        productos = carrito.producto
        if producto_id in productos:
            del productos[producto_id]  # Eliminar producto del carrito
            carrito.productos = productos
            carrito.save()

        # Calcular total
        total = sum(Product.objects.get(id=int(pid)).precio * cantidad for pid, cantidad in productos.items())

        return JsonResponse({"total": total})
    return JsonResponse({"error": "Solicitud inválida"}, status=400)


def seleccionar_mesa(request):
    mesas = Table.objects.all()
    if request.method == "POST":
        num_table = request.POST.get("num_table")
        request.session["num_table"] = num_table  # Guardar número de mesa en la sesión
        return redirect("tables:ver")  # Redirigir a la lista de productos
    return render(request, "table.html", {"mesas": mesas})




def enviar_carrito(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        num_table = request.session.get("num_table")

        if not num_table:
            return JsonResponse({"error": "Debes seleccionar una mesa primero."}, status=400)

        # Buscar carrito
        table = get_object_or_404(Table, num_table=num_table)
        carrito = get_object_or_404(Carrito, table=table, enviado=False)
        
        # Actualizar el estado "enviado" a True
        carrito.enviado = True
        carrito.save()

        return JsonResponse({"success": True})
    return JsonResponse({"error": "Solicitud inválida"}, status=400)




# views.py
from django.shortcuts import render
from .models import Carrito, Product

def pedidos(request):
    carritos_enviados = Carrito.objects.filter(enviado=True)
    carritos_detalle = []

    # Construye los detalles del carrito
    for carrito in carritos_enviados:
        total_precio = 0  # Variable para acumular el total del precio del carrito
        detalle = {
            'id': carrito.id,
            'table': carrito.table.num_table,
            'productos': []
        }
        for producto_id, cantidad in carrito.producto.items():
            producto = Product.objects.get(id=producto_id)
            subtotal = producto.precio * cantidad  # Calcular subtotal para cada producto
            total_precio += subtotal  # Acumular subtotal en el total
            detalle['productos'].append({
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio': producto.precio,
                'subtotal': subtotal  # Añadir subtotal al detalle del producto
            })
        detalle['total_precio'] = total_precio  # Añadir el total del carrito al detalle
        carritos_detalle.append(detalle)

    return render(request, 'pedidos.html', {'carritos': carritos_detalle})





def atender_carrito(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        carrito_id = request.POST.get("carrito_id")
        print(f"Carrito ID recibido: {carrito_id}")  # Verificar si el ID del carrito se está recibiendo
        carrito = get_object_or_404(Carrito, id=carrito_id)

        # Eliminar el carrito de la base de datos
        carrito.delete()
        print(f"Carrito {carrito_id} eliminado")  # Confirmar que el carrito se ha eliminado

        return JsonResponse({"success": True})
    print("Solicitud inválida")  # Verificar si la solicitud es inválida
    return JsonResponse({"error": "Solicitud inválida"}, status=400)

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Carrito, Product

def generar_pdf(request, carrito_id):
    # Obtener el carrito correspondiente
    carrito = Carrito.objects.get(id=carrito_id)
    
    # Calcular el total_precio
    total_precio = 0
    for producto_id, cantidad in carrito.producto.items():
        producto = Product.objects.get(id=producto_id)
        total_precio += producto.precio * cantidad

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="carrito_{carrito_id}.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response)
    p.drawString(100, 800, f'Carrito para Mesa {carrito.table.num_table}')
    p.drawString(100, 780, f'Total: {total_precio} Gs')

    y = 750
    for producto_id, cantidad in carrito.producto.items():
        producto = Product.objects.get(id=producto_id)
        p.drawString(100, y, f'{producto.nombre} - {cantidad} unidades - ${producto.precio * cantidad}')
        y -= 20

    p.showPage()
    p.save()

    # Eliminar el carrito después de generar el PDF
    carrito.delete()

    return response

