from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView
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

def klasiskas(request):
    return render(request, "enges/klasiskas.html")

def vartu_enges(request):
    return render(request, "enges/vartu_enges.html")

def metinamas(request):
    return render(request, "enges/metinamas.html")

def aizbidni(request):
    return render(request, "aizbidni_krampisi/aizbidni.html")

def krampisi(request):
    return render(request, "aizbidni_krampisi/krampisi.html")

def piekaramajai_atslegai(request):
    return render(request, "aizbidni_krampisi/piekaramajai_atslegai.html")

def vartu(request):
    return render(request, "aizbidni_krampisi/vartu.html")

def dalitajam_uzlikam(request):
    return render(request, "durvju_rokturi/dalitajam_uzlikam.html")

def garajam_uzlikam(request):
    return render(request, "durvju_rokturi/garajam_uzlikam.html")

def skandinavu_standarta(request):
    return render(request, "durvju_rokturi/skandinavu_standarta.html")

def skavveida(request):
    return render(request, "durvju_rokturi/skavveida.html")

def centra(request):
    return render(request, "durvju_rokturi/centra.html")

def vacu_standarta(request):
    return render(request, "sledzenes/vacu_standarta.html") 

def euro_standarta(request):
    return render(request, "sledzenes/euro_standarta.html")

def vesture(request):
    return render(request, "par_uznemumu/vesture.html")

def kontakti(request):
    return render(request, "par_uznemumu/kontakti.html")