from re import L
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView

from products.models import Product

# Create your views here.

class ViewBag(TemplateView):
    """ A view that renders the bag contents page """

    template_name = "bag/bag.html"