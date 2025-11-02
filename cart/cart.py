from decimal import Decimal
from store.models import Product  # adjust this import to your product model path


class Cart:
    def __init__(self, request):
        # Store the session object from the incoming HTTP request
        self.session = request.session
        # Try to get existing cart from session
        cart = self.session.get('cart')
        if 'cart' not in self.session:
            # Initialize new empty cart if not found
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price)
            }
        self.session.modified = True

    def __len__(self):
        """Return total number of items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    # ✅ Add this new method so your template can loop: {% for item in cart %}
    def __iter__(self):
        """Iterate over the items in the cart and get products from the database."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        # Attach the product objects to cart items
        for product in products:
            item = self.cart[str(product.id)].copy()
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] =Decimal(item['price']) * item['quantity']
            yield item

    def get_total_price(self):
        """Return the total cost of all items in the cart."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

   