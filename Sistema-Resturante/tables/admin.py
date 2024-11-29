from django.contrib import admin
from .models import *

# admin.site.register(Product)
@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('id','nombre','formatted_precio','categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

    def formatted_precio(self, obj):
        return f"{obj.precio:,}"  # Formatear con separador de miles
    formatted_precio.short_description = 'Precio'

@admin.register(Table)
class Table(admin.ModelAdmin):
    list_display = ('id','num_table')

admin.site.register(Carrito)
@admin.register(Categoria)
class Categoria(admin.ModelAdmin):
    list_display = ('id','nombre')
