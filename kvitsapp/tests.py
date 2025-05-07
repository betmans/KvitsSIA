# kvitsapp/tests.py
from django.test import TestCase, Client # Import Client for view testing
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.text import slugify # Import slugify if needed for helpers

# Import your models and forms
from .models import Category, Product, Profile, Order, OrderItem
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, OrderCreateForm, CartAddProductForm
from .cart import Cart, CART_SESSION_ID # Import Cart logic and session key

# --- Helper Functions (Optional but useful) ---

def create_test_user(username='testuser', password='testpassword123', email='test@example.com'):
    """Helper function to create a user for testing."""
    return User.objects.create_user(username=username, password=password, email=email)

def create_test_category(name='Test Category', slug='test-category'):
    """Helper function to create a category."""
    return Category.objects.create(name=name, slug=slug)

def create_test_product(category_name='Test Category', pasutijuma_kods='TEST001', cena='10.99', apraksts='Test Product Description'):
    """Helper function to create a product."""
    # Ensure category exists or create it if needed for simplicity in tests
    # category, _ = Category.objects.get_or_create(name=category_name, defaults={'slug': slugify(category_name)})
    # Assuming Product.category is a CharField based on previous context
    return Product.objects.create(
        pasutijuma_kods=pasutijuma_kods,
        apraksts=apraksts,
        cena=Decimal(cena),
        category=category_name # Using CharField as per current model
        # category=category # Use this if Product.category is a ForeignKey
    )

# --- Model Tests ---
class CategoryModelTest(TestCase):
    def test_category_creation(self):
        """Test if a Category can be created."""
        category = create_test_category()
        self.assertEqual(str(category), 'Test Category')
        self.assertEqual(category.get_absolute_url(), reverse('kvitsapp:product_list_by_category', args=[category.slug]))

class ProductModelTest(TestCase):
    def test_product_creation(self):
        """Test if a Product can be created."""
        product = create_test_product()
        self.assertEqual(str(product), 'TEST001')
        self.assertEqual(product.cena, Decimal('10.99'))

class ProfileModelTest(TestCase):
    def test_profile_creation_signal(self):
        """Test if a Profile is automatically created when a User is created."""
        user = create_test_user()
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)
        self.assertEqual(str(user.profile), f"{user.username}'s Profile")

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.product1 = create_test_product(pasutijuma_kods='P1', cena='10.00')
        self.product2 = create_test_product(pasutijuma_kods='P2', cena='5.50')
        self.order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='123 Test St'
        )
        self.item1 = OrderItem.objects.create(order=self.order, product=self.product1, price=self.product1.cena, quantity=2)
        self.item2 = OrderItem.objects.create(order=self.order, product=self.product2, price=self.product2.cena, quantity=1)

    def test_order_creation(self):
        self.assertEqual(str(self.order), f'Pasūtījums {self.order.id}')
        self.assertEqual(self.order.items.count(), 2)

    def test_order_item_cost(self):
        self.assertEqual(self.item1.get_cost(), Decimal('20.00'))
        self.assertEqual(self.item2.get_cost(), Decimal('5.50'))

    def test_order_total_cost(self):
        self.assertEqual(self.order.get_total_cost(), Decimal('25.50'))


# --- View Tests ---
class StaticPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('kvitsapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'KVITS SIA')

class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = create_test_category()
        self.product = create_test_product(category_name=self.category.name)

    def test_product_list_by_category_view(self):
        url = reverse('kvitsapp:product_list_by_category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kvitsapp/product_list.html')
        self.assertContains(response, self.product.apraksts)
        self.assertContains(response, self.category.name)
        self.assertIn('products', response.context)
        self.assertIn('category', response.context)

    def test_search_results_view(self):
        url = reverse('kvitsapp:search_results') + '?q=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kvitsapp/product_list.html')
        self.assertContains(response, self.product.apraksts)
        self.assertIn('products', response.context)
        self.assertIn('query', response.context)
        self.assertEqual(response.context['query'], 'Test')

    def test_search_no_results_view(self):
        url = reverse('kvitsapp:search_results') + '?q=NoSuchProduct'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.product.apraksts)
        # FIX: Changed assertQuerysetEqual to assertQuerySetEqual (capital S)
        self.assertQuerySetEqual(response.context['products'], [])


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.profile_url = reverse('kvitsapp:profile')
        try:
            self.login_url = reverse('login') # Use 'login' if using django.contrib.auth.urls
        except Exception as e:
            # Provide a fallback or raise a more informative error if 'login' isn't defined
            print(f"Warning: Could not reverse 'login'. Make sure 'django.contrib.auth.urls' are included in your main urls.py. Error: {e}")
            self.login_url = '/accounts/login/' # Fallback path

    def test_profile_view_requires_login(self):
        """Test that accessing profile redirects to login if not authenticated."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302) # Redirect status
        # FIX: Ensure the login URL used here matches the one defined in urls.py
        self.assertRedirects(response, f'{self.login_url}?next={self.profile_url}')

    def test_profile_view_authenticated(self):
        """Test profile view access when logged in."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')
        self.assertContains(response, self.user.username)
        self.assertIn('user_form', response.context)
        self.assertIn('profile_form', response.context)

    # Add tests for register view (GET and POST), login view (POST), logout etc.


class CartViewsTest(TestCase):
    # Tests for the views that interact with the cart
    def setUp(self):
        self.client = Client()
        self.product = create_test_product(cena='15.00')
        self.add_url = reverse('kvitsapp:cart_add', args=[self.product.id])
        self.remove_url = reverse('kvitsapp:cart_remove', args=[self.product.id])
        self.detail_url = reverse('kvitsapp:cart_detail')

    def test_cart_add_view(self):
        """Test adding an item to the cart via the view."""
        response = self.client.post(self.add_url, {'quantity': 2, 'update': False}, follow=False) # Don't follow redirect yet
        # Check if the item is in the session cart after the POST request
        session = self.client.session
        self.assertIn(CART_SESSION_ID, session)
        cart_data = session[CART_SESSION_ID]
        self.assertIn(str(self.product.id), cart_data)
        self.assertEqual(cart_data[str(self.product.id)]['quantity'], 2)
        self.assertEqual(cart_data[str(self.product.id)]['price'], '15.00')
        # Check that it redirects (usually back to referrer or product page)
        self.assertEqual(response.status_code, 302)

    def test_cart_remove_view(self):
        """Test removing an item from the cart via the view."""
        # First, add the item
        self.client.post(self.add_url, {'quantity': 1, 'update': False})
        session = self.client.session
        self.assertIn(str(self.product.id), session[CART_SESSION_ID])

        # Now, remove it using the view
        response = self.client.post(self.remove_url, follow=True) # Follow redirect to detail page
        self.assertEqual(response.status_code, 200) # Should end up on detail page
        self.assertTemplateUsed(response, 'cart/detail.html')

        # Check if item is removed from session
        session = self.client.session # Re-fetch session after redirect
        self.assertNotIn(str(self.product.id), session.get(CART_SESSION_ID, {}))
        self.assertContains(response, 'Jūsu iepirkumu grozs ir tukšs')

    def test_cart_detail_view_empty(self):
        """Test the cart detail view when the cart is empty."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertContains(response, 'Jūsu iepirkumu grozs ir tukšs') # Your cart is empty

    def test_cart_detail_view_with_items(self):
        """Test the cart detail view with items."""
        self.client.post(self.add_url, {'quantity': 3, 'update': False})
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertContains(response, self.product.apraksts)
        self.assertContains(response, '€45.00') # 3 * 15.00
        self.assertContains(response, 'Kopsumma:') # Subtotal


# --- Form Tests ---
class OrderCreateFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'first_name': 'Test', 'last_name': 'User', 'email': 'valid@example.com',
            'phone_number': '12345678', 'company_name': 'Test Inc.', 'address': '123 Main St'
        }
        form = OrderCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_required(self):
        data = {'first_name': 'Test'}
        form = OrderCreateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('address', form.errors)

    def test_invalid_email(self):
        data = {
            'first_name': 'Test', 'last_name': 'User', 'email': 'invalid-email',
            'address': '123 Main St'
        }
        form = OrderCreateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)



#python manage.py test kvitsapp
#docker-compose exec web python manage.py test kvitsapp