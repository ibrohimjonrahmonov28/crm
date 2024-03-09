
from django.urls import path
from . import views
urlpatterns = [
    path("checkinventory", views.InventoryCheckView.as_view())
]
