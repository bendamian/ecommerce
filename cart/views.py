from django.shortcuts import render

# Create your views here.


def cart_view(request):
    return render(request, 'cart/cart_view.html')

def cart_add(request):
    pass

def cart_remove(request):
    pass

def cart_update(request):
    pass