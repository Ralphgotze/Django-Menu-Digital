from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Product(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria,on_delete=models.SET('Categoria eliminada'))
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)


class Table(models.Model):
    num_table = models.IntegerField()

class Carrito(models.Model):
    producto = models.JSONField(default=dict)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    enviado = models.BooleanField(default=False)
    atendido = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Carrito para Mesa {self.table.num_table}"