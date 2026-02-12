from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from store.models import Product
from cart.cart import Cart
from django.http import JsonResponse
# Create your views here.


def checkout(request):
    #user with account and address details
    if request.user.is_authenticated:
         
         try:
            # user with account and address details
            shipping_addresses = ShippingAddress.objects.get(user=request.user.id)
            context = {
                "shipping": shipping_addresses
            }

            return render(request, 'payment/checkout.html', context)
         
         except :            # user with account but no address details
            return render(request, 'payment/checkout.html')


    # guest user
    else:
       return render(request, 'payment/checkout.html')



def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        address1 = request.POST.get('address_line1')
        address2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        county = request.POST.get('county')
        postal_code = request.POST.get('postal_code')

        # formatted shipping address
        shipping_address =(address1 + "\n" + address2 + "\n" + city + "\n" + county + "\n" + postal_code)
        
        # shopping cart information
        cart = Cart(request)
        # get cart total
        cart_total = cart.get_total_price() 
        
        
        '''
        1. create order USER with and wiwith shipping address
        2. create order GUEST without account and shipping address

        
        '''

        if request.user.is_authenticated:
            # user with account and address details
            #shipping_addresses = ShippingAddress.objects.get(user=request.user.id)
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                status="created",
                amount_paid=cart_total,
                user=request.user,
            )
            order_id = order.pk
            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    quantity=item["quantity"],
                    price_at_purchase=item["price"],

                )

        else:
            # user without account and address details
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                status="created",
                amount_paid=cart_total,
            )
            order_id = order.pk
            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    quantity=item["quantity"],
                    price_at_purchase=item["price"],
                )

        order_success = True
        response = JsonResponse({"success": order_success})
        return response



def payment_success(request):
    #clear cart
    for key in list(request.session.keys()):
        if key == 'cart':
            del request.session[key]


    return render(request, 'payment/payment-success.html')
def payment_failed(request):
    return render(request, 'payment/payment-failed.html')

