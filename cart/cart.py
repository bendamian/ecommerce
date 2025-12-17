from decimal import Decimal
from store.models import Product  


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in self.session:
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

    def update(self, product_id, quantity):
        product_id = str(product_id)

        if product_id in self.cart:
            try:
                quantity = int(quantity)
            except:
                quantity = self.cart[product_id]['quantity']

            if quantity <= 0:
                del self.cart[product_id]
            else:
                self.cart[product_id]['quantity'] = quantity

            self.session.modified = True

    def remove(self, product):
        product_id = str(getattr(product, 'id', product))
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            item = self.cart[str(product.id)].copy()
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
