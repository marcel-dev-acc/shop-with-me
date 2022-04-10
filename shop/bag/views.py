from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.views import View
from products.models import Product

# Create your views here.

class ViewBag(View):
    """
    A view that renders the bag contents page
    """

    def get(self, request):
        """
        Handle get requests to viewing hte bag
        """
        
        return render(request, "bag/bag.html")


class AddToBag(View):
    """
    Add a quantity of the specified product to the shopping bag
    """

    def post(self, request, item_id):
        """
        Handle post requests for Add to bag
        """

        product = get_object_or_404(Product, pk=item_id)
        quantity = int(request.POST.get('quantity'))
        redirect_url = request.POST.get('redirect_url')
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            if item_id in list(bag.keys()):
                if size in bag[item_id]['items_by_size'].keys():
                    bag[item_id]['items_by_size'][size] += quantity
                    messages.success(
                        request,
                        f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}'
                    )
                else:
                    bag[item_id]['items_by_size'][size] = quantity
                    messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
            else:
                bag[item_id] = {'items_by_size': {size: quantity}}
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            if item_id in list(bag.keys()):
                bag[item_id] += quantity
                messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
            else:
                bag[item_id] = quantity
                messages.success(request, f'Added {product.name} to your bag')

        request.session['bag'] = bag
        return redirect(redirect_url)


class AdjustBag(View):
    """
    Adjust the quantity of the specified product to the specified amount
    """

    def post(self, request, item_id):
        """
        Handle post requests to Adjust Bag
        """

        product = get_object_or_404(Product, pk=item_id)
        quantity = int(request.POST.get('quantity'))
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            if quantity > 0:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                del bag[item_id]['items_by_size'][size]
                if not bag[item_id]['items_by_size']:
                    bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            if quantity > 0:
                bag[item_id] = quantity
                messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
            else:
                bag.pop(item_id)
                messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return redirect(reverse('view_bag'))