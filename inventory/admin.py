from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductMaterial)
admin.site.register(Warehouse)
admin.site.register(Material)