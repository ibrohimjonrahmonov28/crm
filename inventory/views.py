from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductMaterialSerializer, WarehouseSerializer

class InventoryCheckView(APIView):

    # def post(self, request):
    #     product_name= request.data.get("product_name")
    #     product_qty =request.data.get("product_qty")
    #     response_data = []
    #     product_materials = ProductMaterial.objects.filter(product__name=product_name)
    #     product_data = {
    #             "product_name": product_name,
    #             "product_qty": product_qty,
    #             "product_materials": []
    #         }

    #     for material in product_materials:
    #             warehouses = Warehouse.objects.filter(material=material.material).order_by('-remainder')
    #             material_data = {"material_name": material.material.name, "qty": 0}
    #             for warehouse in warehouses:
    #                 if material_data["qty"] >= material.quantity:
    #                     break
    #                 available_qty = min(warehouse.remainder, material.quantity - material_data["qty"])
    #                 material_data["qty"] += available_qty
    #                 product_data["product_materials"].append({
    #                     "warehouse_id": warehouse.id if available_qty > 0 else None,
    #                     "material_name": material.material.name,
    #                     "qty": available_qty,
    #                     "price": warehouse.price if available_qty > 0 else None
    #                 })
    #     response_data.append(product_data)
    #     return Response(response_data)
    def post(self, request):
        # production_plan = request.data.get("production_plan", [])
        response_data = []
        product_info= request.data
        # for product_info in production_plan:
        product_name = product_info.get("product_name")
        product_qty = float(product_info.get("product_qty"))
        product_materials = ProductMaterial.objects.filter(product__name=product_name)
        product_data = {
                "product_name": product_name,
                "product_qty": product_qty,
                "product_materials": []
            }

        for material in product_materials:
                warehouses = Warehouse.objects.filter(material=material.material).order_by("-remainder")
                material_qty_needed = product_qty * material.quantity
                material_qty_available = 0

                for warehouse in warehouses:
                    if material_qty_available >= material_qty_needed:
                        break

                    available_qty = min(warehouse.remainder, material_qty_needed - material_qty_available)
                    material_qty_available += available_qty

                    product_data["product_materials"].append({
                        "warehouse_id": warehouse.id if available_qty > 0 else None,
                        "material_name": material.material.name,
                        "qty": available_qty,
                        "price": warehouse.price if available_qty > 0 else None
                    })

                if material_qty_needed > material_qty_available:
                    product_data["product_materials"].append({
                        "warehouse_id": None,
                        "material_name": material.material.name,
                        "qty": material_qty_needed - material_qty_available,
                        "price": None
                    })

        response_data.append(product_data)

        return Response({"result": response_data})