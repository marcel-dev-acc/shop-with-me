from django.urls import path
from . import views

urlpatterns = [
    path("", views.ViewBag.as_view(), name="view_bag"),
]
