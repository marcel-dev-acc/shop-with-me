from django.urls import path
from . import views

urlpatterns = [
    path("", views.ViewBag.as_view(), name="view_bag"),
    path("add/<item_id>", views.AddToBag.as_view(), name="add_to_bag"),
]
