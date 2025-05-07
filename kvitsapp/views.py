from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from datetime import datetime
from .models import Category, Product, Profile, Order, OrderItem
from django.conf import settings
from django.template.loader import get_template, render_to_string
import os
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, OrderCreateForm
from .cart import Cart
from django import forms
from django.core.mail import send_mail
from django.urls import reverse


# ++++++++++ CART ADD PRODUCT FORM ++++++++++
# This form is used on product listings/details to add items
class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'width: 60px; display: inline-block;'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

# ++++++++++ EXISTING VIEWS (Index, Category, Search) ++++++++++
def index(request):
    """
    Renders the index/home page.
    """
    context = { 'gads': datetime.now().year }
    return render(request, "index.html", context)

def product_list_by_category(request, slug):
    """
    Displays products filtered by a specific category slug.
    Adds CartAddProductForm to each product's context.
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category.name)
    # Add the cart form to each product for easy adding
    for product in products:
        product.cart_add_form = CartAddProductForm()
    return render(request, 'kvitsapp/product_list.html', {
        'category': category,
        'products': products,
    })

def search_results(request):
    """
    Displays products based on a search query parameter 'q'.
    Adds CartAddProductForm to each product's context.
    """
    query = request.GET.get('q')
    products = []
    if query:
        products = Product.objects.filter(
            Q(apraksts__icontains=query) |
            Q(pasutijuma_kods__icontains=query) |
            Q(ean13__icontains=query)
        )
    # Add the cart form to each product
    for product in products:
        product.cart_add_form = CartAddProductForm()
    return render(request, 'kvitsapp/product_list.html', {
        'products': products,
        'query': query,
    })

# ++++++++++ AUTHENTICATION VIEWS (Register, Profile, Delete) ++++++++++
def register(request):
    """
    Handles user registration.
    GET: Displays the registration form.
    POST: Processes the registration form submission.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Reģistrācija veiksmīga! Jūs esat pieslēdzies.')
            return redirect('kvitsapp:index')
        else:
            messages.error(request, 'Lūdzu, izlabojiet kļūdas zemāk.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    """
    Handles viewing and updating the user's profile information.
    Requires the user to be logged in.
    GET: Displays the user and profile update forms.
    POST: Processes form submissions for updating user and profile info.
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Jūsu profils ir veiksmīgi atjaunināts!')
            return redirect('kvitsapp:profile')
        else:
            messages.error(request, 'Lūdzu, izlabojiet kļūdas zemāk.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'registration/profile.html', context)

@login_required
def delete_profile(request):
    """
    Handles the deletion of a user account.
    Requires the user to be logged in.
    GET request shows confirmation page.
    POST request performs the deletion after confirmation.
    """
    user_to_delete = request.user

    if request.method == 'POST':
        try:
            username = user_to_delete.username
            logout(request)
            user_to_delete.delete()
            messages.success(request, f'Lietotāja "{username}" profils ir veiksmīgi dzēsts.')
            return redirect('kvitsapp:index')
        except Exception as e:
            messages.error(request, f'Kļūda dzēšot profilu: {e}')
            return redirect('kvitsapp:index')

    # Render the confirmation template for GET requests
    return render(request, 'registration/delete_confirm.html')


# ++++++++++ CART VIEWS ++++++++++

@require_POST # Ensures only POST requests can add items
def cart_add(request, product_id):
    """
    Adds a product to the cart or updates its quantity.
    Redirects back to the referring page.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST) # Form to get quantity/update flag

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        messages.success(request, f'"{product.apraksts or product.pasutijuma_kods}" pievienots grozam.')
    else:
        messages.error(request, 'Neizdevās pievienot preci grozam.') # Failed to add item

    # ****** MODIFIED REDIRECT ******
    # Redirect back to the page the user came from (e.g., product list)
    # Use HTTP_REFERER, providing a fallback to the index page if it's not available
    # Note: HTTP_REFERER isn't always reliable, but often works well enough.
    # A more robust solution might involve passing a 'next' URL parameter.
    redirect_url = request.META.get('HTTP_REFERER', reverse('kvitsapp:index'))
    return redirect(redirect_url)
    # ****** END MODIFIED REDIRECT ******

@require_POST # Ensures only POST requests can remove items
def cart_remove(request, product_id):
    """
    Removes a product from the cart.
    Redirects back to the cart detail page.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'"{product.apraksts or product.pasutijuma_kods}" izņemts no groza.')
    # Redirect back to cart detail after removing an item
    return redirect('kvitsapp:cart_detail')

def cart_detail(request):
    """
    Displays the current contents of the shopping cart.
    Adds an update form to each item for quantity modification.
    """
    cart = Cart(request)
    # Prepare update forms for each item in the cart
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                  'update': True}) # Set update=True for replacement
    # Render the cart detail template
    return render(request, 'cart/detail.html', {'cart': cart})

# ++++++++++ CHECKOUT/ORDER VIEW ++++++++++

def create_order(request):
    """
    Handles the checkout process:
    GET: Displays the order form, pre-filled if user is logged in.
    POST: Validates form, creates Order and OrderItem objects, sends email, clears cart.
    """
    cart = Cart(request)
    # Redirect if cart is empty
    if not cart:
        messages.warning(request, "Jūsu grozs ir tukšs, lai veiktu pasūtījumu.") # Your cart is empty to place an order
        return redirect('kvitsapp:index')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST) # Use the imported form
        if form.is_valid():
            order = form.save(commit=False) # Don't save to DB yet
            # Assign user if logged in
            if request.user.is_authenticated:
                order.user = request.user
                # Optionally pre-fill missing fields from profile
                profile = request.user.profile
                if not order.company_name and profile.company_name: order.company_name = profile.company_name
                if not order.phone_number and profile.phone_number: order.phone_number = profile.phone_number
                if not order.address and profile.address: order.address = profile.address
                # Add other fields as needed

            order.save() # Now save the Order instance

            # Create OrderItem objects for each item in the cart
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # --- Send Email Confirmation ---
            try:
                subject = f'Jauns Pasūtījums Nr. {order.id}' # New Order Nr.
                # Render email content from templates
                html_message = render_to_string('emails/order_confirmation_company.html', {'order': order, 'cart': cart})
                plain_message = render_to_string('emails/order_confirmation_company.txt', {'order': order, 'cart': cart})
                from_email = settings.DEFAULT_FROM_EMAIL # Get sender from settings
                # Get recipient from settings, provide a fallback if not defined
                recipient_list = [getattr(settings, 'COMPANY_ORDER_EMAIL', 'your_company_fallback_email@example.com')]

                send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)

            except Exception as e:
                 # Log the error and inform the user, but don't necessarily stop the process
                 print(f"Error sending order confirmation email for order {order.id}: {e}")
                 messages.warning(request, f"Pasūtījums Nr. {order.id} ir izveidots, bet radās kļūda sūtot apstiprinājuma e-pastu uzņēmumam. Lūdzu, sazinieties ar mums, ja nepieciešams.") # Order created, but error sending email...

            # Clear the cart session
            cart.clear()

            messages.success(request, f'Paldies! Jūsu pasūtījums Nr. {order.id} ir veiksmīgi izveidots.') # Thank you! Your order Nr. {order.id} has been successfully created.
            # Redirect to a success page or home
            # Consider creating an order success page: return render(request, 'orders/order_created.html', {'order': order})
            return redirect('kvitsapp:index')

        else: # Form is invalid
             messages.error(request, 'Lūdzu, pārbaudiet ievadīto informāciju pasūtījuma formā.') # Please check the information entered in the order form.

    else: # GET request - display the empty form, pre-filled if user logged in
        initial_data = {}
        if request.user.is_authenticated:
            # Pre-fill form with user/profile data
            profile = request.user.profile
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone_number': profile.phone_number,
                'company_name': profile.company_name,
                'address': profile.address,
            }
        form = OrderCreateForm(initial=initial_data) # Use the imported form

    # Render the checkout page template
    return render(request, 'orders/create_order.html', {'cart': cart, 'form': form})



