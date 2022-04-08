from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .models import Product, Category
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages

# Create your views here.
class AllProducts(View):
    """
    Manage the request for all products to be displayed,
    filtered list of products, sorting, etc.
    """

    def get(self, request):
        """Handle GET requests for AllProducts"""

        products = Product.objects.all()
        query = None
        categories = None
        sort = None
        direction = None

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

        current_sorting = f'{sort}_{direction}'

        context = {
            'products': products,
            'search_term': query,
            'current_categories': categories,
            'current_sorting': current_sorting,
        }

        return render(request, 'products/products.html', context)


class ProductDetail(View):
    """
    A view to show individual product details
    """

    def get(self, request, product_id):
        """Handle GET requests for AllProducts"""

        product = get_object_or_404(Product, pk=product_id)

        context = {
            'product': product,
        }

        return render(request, 'products/product_detail.html', context)