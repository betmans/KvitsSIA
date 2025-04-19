from django.urls import path
from . import views
#from backend.views import index

urlpatterns = [
    path('', views.index, name='index'),
    path('enges/klasiskas.html', views.klasiskas, name='klasiskas'),
    path('enges/vartu_enges.html', views.vartu_enges, name='vartu_enges'),
    path('enges/metinamas.html', views.metinamas, name='metinamas'),
    path('aizbidni_krampisi/aizbidni.html', views.aizbidni, name='aizbidni'),
    path('aizbidni_krampisi/krampisi.html', views.krampisi, name='krampisi'),
    path('aizbidni_krampisi/piekaramajai_atslegai.html', views.piekaramajai_atslegai, name='piekaramajai_atslegai'),
    path('aizbidni_krampisi/vartu.html', views.vartu, name='vartu'),
    path('durvju_rokturi/dalitajam_uzlikam.html', views.dalitajam_uzlikam, name='dalitajam_uzlikam'),
    path('durvju_rokturi/garajam_uzlikam.html', views.garajam_uzlikam, name='garajam_uzlikam'),
    path('durvju_rokturi/skandinavu_standarta.html', views.skandinavu_standarta, name='skandinavu_standarta'),
    path('durvju_rokturi/skavveida.html', views.skavveida, name='skavveida'),
    path('durvju_rokturi/centra.html', views.centra, name='centra'),
    path('sledzenes/vacu_standarta.html', views.vacu_standarta, name='vacu_standarta'),
    path('sledzenes/euro_standarta.html', views.euro_standarta, name='euro_standarta'),
    path('sledzenes/skandinavu_standarta.html', views.euro_standarta, name='euro_standarta'),
    path('par_uznemumu/vesture.html', views.vesture, name='vesture'),
    path('par_uznemumu/kontakti.html', views.kontakti, name='kontakti'),

]