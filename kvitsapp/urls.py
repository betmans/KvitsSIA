from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'kvitsapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<slug:slug>/', views.product_list_by_category, name='product_list_by_category'),
    path('search/', views.search_results, name='search_results'),

    # Par uzņēmumu sadaļas
    path('par_uznemumu/vesture.html', TemplateView.as_view(template_name="par_uznemumu/vesture.html"), name='vesture'),
    path('par_uznemumu/kontakti.html', TemplateView.as_view(template_name="par_uznemumu/kontakti.html"), name='kontakti'),
    path('par_uznemumu/piegade_sanemsana.html', TemplateView.as_view(template_name="par_uznemumu/piegade_sanemsana.html"), name='piegade_sanemsana'),
    path('par_uznemumu/privatuma_politika.html', TemplateView.as_view(template_name="par_uznemumu/privatuma_politika.html"), name='privatuma_politika'),

    # ++++++++++ AUTHENTICATION AND PROFILE URLS ++++++++++

    # Registration
    path('register/', views.register, name='register'),

    # Profile view, edit, delete
    path('profile/', views.profile, name='profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),


    # Login view (using Django's built-in view)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Logout view (using Django's built-in view)
    path('logout/', auth_views.LogoutView.as_view(next_page='kvitsapp:index'), name='logout'),

    # Password change views (using Django's built-in views)
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             success_url='/password_change/done/' # Redirect URL after successful change
         ),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ),
         name='password_change_done'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html', # Email template
             subject_template_name='registration/password_reset_subject.txt', # Email subject template
             success_url='/password_reset/done/' # URL after submitting email
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', # URL sent in the email
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/reset/done/' # URL after successfully setting new password
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # ++++++++++ END AUTHENTICATION AND PROFILE URLS ++++++++++

     # ++++++++++ CART URLs ++++++++++
    path('cart/', views.cart_detail, name='cart_detail'),
    # URL for adding an item - expects product ID
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    # URL for removing an item - expects product ID
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    # ++++++++++ END CART URLs ++++++++++

    # ++++++++++ ORDER URL ++++++++++
    path('order/create/', views.create_order, name='create_order'),
    # ++++++++++ END ORDER URL ++++++++++


    
]
