from django.db import models

# Create your models here.


class Product(models.Model):
  name = models.CharField(max_length=255)
  code = models.IntegerField()

  def __str__(self):
    return self.name

class Material(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class ProductMaterial(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  material = models.ForeignKey(Material, on_delete=models.CASCADE)
  quantity = models.FloatField()

class Warehouse(models.Model):
  material = models.ForeignKey(Material, on_delete=models.CASCADE)
  remainder = models.PositiveIntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  created_date = models.DateTimeField(auto_created=True)

  def __str__(self):
    return f"{self.material.name} - {self.remainder}"
