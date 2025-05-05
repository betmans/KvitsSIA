from django.db import models
from django.urls import reverse
from django.conf import settings # Import settings to get the User model
from django.db.models.signals import post_save # To create profile automatically
from django.dispatch import receiver # To receive the signal

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    

    def get_absolute_url(self):
        return reverse('kvitsapp:product_list_by_category', args=[self.slug])

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    ean13 = models.CharField(max_length=255)
    pasutijuma_kods = models.CharField(max_length=255, unique=True, null=True)
    apraksts = models.TextField(blank=True)
    attels = models.URLField(blank=True)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.ean13  # Changed from self.name to self.ean13
    
class Product(models.Model):
    ean13 = models.CharField(max_length=255, blank=True, null=True) # Allow blank/null EAN
    pasutijuma_kods = models.CharField(max_length=255, unique=True, null=True)
    apraksts = models.TextField(blank=True)
    # Consider using ImageField for better image management if storing locally
    # attels = models.ImageField(upload_to='product_images/', blank=True, null=True)
    attels = models.CharField(max_length=255, blank=True) # Assuming relative path like 'images/product_xyz.png'
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    # Link to Category model properly if desired, otherwise keep as CharField
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    category = models.CharField(max_length=100, blank=True) # Current implementation

    def __str__(self):
        return self.pasutijuma_kods or f"Product {self.id}" # More robust __str__

# ++++++++++ NEW PROFILE MODEL ++++++++++
class Profile(models.Model):
    """
    Extends the default Django User model to store additional information.
    """
    # Link to the built-in User model. Each User has one Profile.
    # settings.AUTH_USER_MODEL refers to Django's User model.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    # Add fields specific to your user profile needs
    # Example fields (adjust as needed):
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Uzņēmuma nosaukums")
    registration_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Reģistrācijas numurs")
    vat_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="PVN numurs")
    address = models.TextField(blank=True, null=True, verbose_name="Adrese")
    phone_number = models.CharField(max_length=30, blank=True, null=True, verbose_name="Telefona numurs")
    # Add more fields as required...
    # e.g., delivery_address, billing_address, etc.

    def __str__(self):
        # Return a string representation of the profile
        return f"{self.user.username}'s Profile"

# ++++++++++ SIGNAL TO CREATE/UPDATE PROFILE ++++++++++
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that automatically creates or updates a Profile
    instance whenever a User instance is saved.
    """
    if created:
        # If a new User was created, create a corresponding Profile
        Profile.objects.create(user=instance)
    # Ensure the profile is saved even if the user is just updated (optional, but good practice)
    instance.profile.save()
# ++++++++++ END NEW PROFILE MODEL AND SIGNAL ++++++++++




# ++++++++++ NEW ORDER AND ORDER ITEM MODELS ++++++++++

class Order(models.Model):
    """
    Represents a customer order.
    """
    # Link to the user who placed the order (optional if allowing guest checkout)
    # If allowing guests, make user nullable: models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    # Customer details (can be pre-filled from Profile or entered at checkout)
    first_name = models.CharField(max_length=100, verbose_name="Vārds")
    last_name = models.CharField(max_length=100, verbose_name="Uzvārds")
    email = models.EmailField(verbose_name="E-pasts")
    phone_number = models.CharField(max_length=30, blank=True, verbose_name="Telefona numurs")
    company_name = models.CharField(max_length=255, blank=True, verbose_name="Uzņēmuma nosaukums")
    address = models.CharField(max_length=250, verbose_name="Piegādes adrese") # Delivery address
    # postal_code = models.CharField(max_length=20, verbose_name="Pasta indekss")
    # city = models.CharField(max_length=100, verbose_name="Pilsēta")
    # Add more fields as needed (e.g., billing address if different)

    created = models.DateTimeField(auto_now_add=True, verbose_name="Izveidots")
    updated = models.DateTimeField(auto_now=True, verbose_name="Atjaunināts")
    # paid = models.BooleanField(default=False, verbose_name="Apmaksāts") # Add later if implementing payments

    class Meta:
        ordering = ['-created'] # Show newest orders first
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = "Pasūtījums" # Order
        verbose_name_plural = "Pasūtījumi" # Orders

    def __str__(self):
        return f'Pasūtījums {self.id}' # Order {self.id}

    def get_total_cost(self):
        """Calculates the total cost of all items in the order."""
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    """
    Represents a single item within an order.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Link to the actual product
    # on_delete=models.PROTECT prevents deleting a product if it's part of an order
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena") # Price at the time of order
    quantity = models.PositiveIntegerField(default=1, verbose_name="Daudzums")

    class Meta:
        verbose_name = "Pasūtījuma vienība" # Order Item
        verbose_name_plural = "Pasūtījuma vienības" # Order Items

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """Calculates the cost of this specific order item."""
        return self.price * self.quantity

# ++++++++++ END ORDER AND ORDER ITEM MODELS ++++++++++