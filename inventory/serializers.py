from rest_framework import serializers
from .models import ProductMaterial, Warehouse

class ProductMaterialSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProductMaterial
    fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Warehouse
    fields = '__all__'
