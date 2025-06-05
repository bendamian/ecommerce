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
