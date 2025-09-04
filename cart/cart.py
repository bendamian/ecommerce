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
        product_id = str(product.id)  # Convert product ID to string to ensure it's a valid key in the cart dictionary.product.id
        if product_id  in self.cart:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
       
        self.session.modified = True

   