from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductMaterialSerializer, WarehouseSerializer

class InventoryCheckView(APIView):
    def post(self, request):
        response_data = []
        product_name= request.data.get("product_name")
        product_qty =float(request.data.get("product_qty"))
        # Ma'lumotlar bazasidan xomashyolar va ularning narxlari olish
        warehouses = Warehouse.objects.all()
        warehouse_info = {warehouse.material.name: (warehouse.id, warehouse.remainder, warehouse.price) for warehouse in warehouses}

        # Berilgan ma'lumotlarni tekshirish
        product_info = [
            {"product_name": product_name, "product_qty": product_qty}
        ]

        for product_data in product_info:
            product_name = product_data["product_name"]
            product_qty = product_data["product_qty"]
            product_materials = ProductMaterial.objects.filter(product__name=product_name).order_by("- ")
            processed_materials = []

            for material in product_materials:
                material_name = material.material.name
                material_qty_needed = product_qty * material.quantity

                if material_name in warehouse_info:
                    warehouse_id, warehouse_remainder, warehouse_price = warehouse_info[material_name]
                    if material_qty_needed <= warehouse_remainder:
                        processed_materials.append({
                            "warehouse_id": warehouse_id,
                            "material_name": material_name,
                            "qty": material_qty_needed,
                            "price": warehouse_price
                        })
                    else:
                        processed_materials.append({
                            "warehouse_id": None,
                            "material_name": material_name,
                            "qty": material_qty_needed - warehouse_remainder,
                            "price": None
                        })

            response_data.append({
                "product_name": product_name,
                "product_qty": product_qty,
                "product_materials": processed_materials
            })

        return Response({"result": response_data})
