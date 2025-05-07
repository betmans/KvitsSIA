# kvitsapp/context_processors.py
from datetime import datetime
from .models import Category
# Try importing the cart module directly first
from . import cart as cart_module

def year(request):
    """Adds the current year to the context."""
    return {
        'gads': datetime.now().year
    }

def categories_processor(request):
    """Adds categories and category groups to the context."""
    category_groups = {
        "Eņģes": ["Klasiskās", "Vārtu", "T veida", "Antīkās", "Metināmās", "Atsper", "Klavieru"],
        "Aizbīdņi": ["Aizbīdņi", "Kronšteini", "Krampji", "Vārtiem", "Iekaļamie aizbīdņi"],
        "Slēdzenes": ["Vācu standarta", "Eiro standarta", "Skandināvu standarta", "Profilcilindram", "Universālās", "Pretplāksnes", "Uzliekamās", "Starpistabu", "Rulīšu mehanismi", "WC slēdzenes"],
        "Rokturi": ["Garajām uzlikām", "Dalītajām uzlikām", "Skandināvu rokturi", "Skavveida", "Koka", "Centra", "Stieņi", "Lūkas"],
        "Cilindri": ["Parastie", "Multi Cilindri", "Uzlikas", "WC"],
        "Mēbeļu": ["Mēbeļu slēdzenes", "Magnēti", "Lodītes"],
        "Aksesuāri": ["Actiņas", "Durvju aizvērēji", "Piekaramās atslēgas", "Numuriņi", "Atsperes", "Pakaramie", "Atdures"],
        "Stiprinājumi": ["Margu balsti", "Konsoles"]
    }
    categories = Category.objects.all()
    return {'categories': categories, 'category_groups': category_groups}

def cart_processor(request):
    cart = cart_module.Cart(request) # MUST pass request
    return {'cart': cart}


