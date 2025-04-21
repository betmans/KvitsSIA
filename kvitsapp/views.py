from django.views.generic import TemplateView
from django.shortcuts import render
from datetime import datetime
# from django.views.generic import ListView
# from django.core.paginator import Paginator
# from .models import Product
# from .models import Enge, aizbidni_krampisi, sledzenes, durvju_rokturi, cilindri_aizgriezni, mebelu_furnitura, aksesuari, stiprinajumi

# class EngeListView(ListView):
#     model = Enge
#     template_name = 'enges/enge_list.html'  # Create this template
#     context_object_name = 'enges'

def index(request):
    context = {
        'gads': datetime.now().year
    }
    return render(request, "index.html", context)

from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# def product_list(request):
#     """
#     View to display products in a tile layout with pagination
#     """
#     # Get all products ordered by pasutijuma_kods
#     products = Product.objects.all().order_by('pasutijuma_kods')
    
#     # Set up pagination - 12 products per page
#     paginator = Paginator(products, 12)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)
    
#     context = {
#         'page_obj': page_obj,
#         'total_products': products.count(),
#     }
    
#     return render(request, 'kvitsapp/product_list.html', context)

