from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import Category, Product
from django.http import JsonResponse
from .cart import Cart

# Create your views here.


def cart_view(request):
    cart = Cart(request)

    return render(request, 'cart/cart_view.html', {'cart': cart})


def cart_add(request):
    cart = Cart(request)

    if request.method == "POST" and request.POST.get("action") == "post":
        # 🔍 Debug: log what was received
        print("POST data:", request.POST)
        product_id = request.POST.get("productid")
        product_quantity = request.POST.get("quantity")

        # Defensive checks
        if not product_id or not product_quantity:
            return JsonResponse({"error": "Missing product ID or quantity"}, status=400)

        try:
            product_id = int(product_id)
            product_quantity = int(product_quantity)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid product ID or quantity"}, status=400)

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_quantity)
        # Return total cart quantity (or whatever you need)
        total_quantity = cart.__len__()

        response = JsonResponse({
            "quantity": total_quantity

        })
        return response

    return JsonResponse({"error": "Invalid request"}, status=400)


def cart_remove(request):
    cart = Cart(request)
    if request.method == "POST" and request.POST.get("action") == "post":
        # 🔍 Debug: log what was received
        print("POST data:", request.POST)
        product_id = request.POST.get("productid")
        cart.remove(product=product_id)

        # Return total cart quantity (or whatever you need)
        total_quantity = cart.__len__()

        cart_total = cart.get_total_price()

        response = JsonResponse({
            "quantity": total_quantity,
            "total": cart_total
        })
        return response

        
def cart_update(request):
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        quantity = int(request.POST.get('quantity'))

        cart = Cart(request)
        cart.update(product_id=product_id, quantity=quantity)

        response = {
            'quantity': cart.__len__(),
            'total': cart.get_total_price()
        }
        return JsonResponse(response)

    # ⭐ Prevent returning NONE here
    return JsonResponse({'error': 'Invalid request'}, status=400)
