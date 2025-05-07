# kvitsapp/cart.py (Correct version - Accepts Request)

from decimal import Decimal
from django.conf import settings
from .models import Product # Import your Product model

# Define the session key for the cart
CART_SESSION_ID = settings.CART_SESSION_ID if hasattr(settings, 'CART_SESSION_ID') else 'cart'

class Cart:
    """
    Manages the shopping cart using Django sessions.
    """
    def __init__(self, request):
        """
        Initialize the cart.
        Accepts the HttpRequest object.
        """
        # Store the session from the request object
        self.session = request.session
        # Try to get the cart from the current session using the defined key
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            # If no cart exists in the session, create an empty dictionary
            # and assign it to the session using the CART_SESSION_ID key.
            cart = self.session[CART_SESSION_ID] = {}
        # Store the cart dictionary (retrieved or newly created) in the instance
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id) # Session keys must be strings

        if product_id not in self.cart:
            # If the product is not in the cart, add it with initial quantity 0
            # and store its price as a string (sessions prefer simple types).
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.cena)}

        if update_quantity:
            # If update_quantity is True, set the quantity directly.
            self.cart[product_id]['quantity'] = quantity
        else:
            # Otherwise, add the requested quantity to the existing quantity.
            self.cart[product_id]['quantity'] += quantity

        # Ensure quantity doesn't become negative after an update/add operation.
        if self.cart[product_id]['quantity'] < 0:
             self.cart[product_id]['quantity'] = 0

        # If the quantity is zero or less after adding/updating, remove the item.
        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product) # Call the remove method
        else:
            # Otherwise, save the changes to the session.
            self.save()

    def save(self):
        """
        Mark the session as "modified" to ensure it gets saved by Django.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        Accepts a Product object.
        """
        product_id = str(product.id)
        # Check if the product exists in the cart dictionary before deleting.
        if product_id in self.cart:
            del self.cart[product_id] # Delete the item using its ID as the key.
            self.save() # Save the changes to the session.

    def __iter__(self):
        """
        Iterate over the items in the cart dictionary.
        Fetches the corresponding Product objects from the database
        and yields cart items enriched with the Product object and total price.
        """
        product_ids = self.cart.keys()
        # Get the product objects from the database efficiently in one query.
        products = Product.objects.filter(id__in=product_ids)
        # Create a mapping from product ID to Product object for quick lookup.
        products_map = {str(p.id): p for p in products}

        # Create a deep copy of the cart to avoid modifying it while iterating.
        cart_copy = self.cart.copy() # Use a different variable name

        # Add the actual Product object to each item in the copied cart dictionary.
        for product_id, item in cart_copy.items():
            if product_id in products_map:
                item['product'] = products_map[product_id]

        # Yield items one by one, converting price back to Decimal and calculating total price.
        for item in cart_copy.values():
            # Ensure the 'product' key exists before proceeding (in case a product was deleted from DB)
            if 'product' in item:
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item
            # Optionally handle items where the product might no longer exist in the DB

    def __len__(self):
        """
        Calculate the total number of individual items (sum of quantities) in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total cost of all items in the cart.
        Converts stored string prices back to Decimal for calculation.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove the cart dictionary entirely from the session.
        """
        # Check if the cart session key exists before trying to delete it.
        if CART_SESSION_ID in self.session:
            del self.session[CART_SESSION_ID]
            self.save() # Save the changes to the session.

