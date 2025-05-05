# kvitsapp/cart.py

from decimal import Decimal
from django.conf import settings
from .models import Product # Import your Product model

# Define the session key for the cart
CART_SESSION_ID = 'cart'

class Cart:
    """
    Manages the shopping cart using Django sessions.
    """
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        # Try to get the cart from the current session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            # If no cart exists in the session, create an empty one
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id) # Session keys must be strings

        if product_id not in self.cart:
            # If the product is not in the cart, add it
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.cena)} # Store price as string
        
        if update_quantity:
            # If update_quantity is True, set the quantity directly
            self.cart[product_id]['quantity'] = quantity
        else:
            # Otherwise, add the quantity to the existing quantity
            self.cart[product_id]['quantity'] += quantity

        # Ensure quantity is not negative
        if self.cart[product_id]['quantity'] < 0:
             self.cart[product_id]['quantity'] = 0

        # Remove item if quantity is zero or less after update/add
        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product)
        else:
            self.save() # Save changes to the session

    def save(self):
        """
        Mark the session as "modified" to ensure it gets saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id] # Delete the item from the cart dictionary
            self.save() # Save changes to the session

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # Get the product objects and add them to the cart items
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy() # Create a copy to modify during iteration
        for product in products:
            cart[str(product.id)]['product'] = product # Add the Product object itself

        # Yield items with calculated total price
        for item in cart.values():
            item['price'] = Decimal(item['price']) # Convert price back to Decimal
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart (sum of quantities).
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total cost of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove the cart from the session entirely.
        """
        del self.session[CART_SESSION_ID]
        self.save()

