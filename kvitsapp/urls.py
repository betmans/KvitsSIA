from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'kvitsapp'

urlpatterns = [
    path('', views.index, name='index'),

    # Enges
    path('enges/parastas.html', TemplateView.as_view(template_name="enges/parastas.html"), name='parastas'),
    path('enges/vartu_enges.html', TemplateView.as_view(template_name="enges/vartu_enges.html"), name='vartu_enges'),
    path('enges/metinamas.html', TemplateView.as_view(template_name="enges/metinamas.html"), name='metinamas'),
    path('enges/t_veida.html', TemplateView.as_view(template_name="enges/t_veida.html"), name='t_veida'),

    # Aizbidni krampji kronsteini
    path('aizbidni_krampji_kronsteini/aizbidni.html', TemplateView.as_view(template_name="aizbidni_krampji_kronsteini/aizbidni.html"), name='aizbidni'),
    path('aizbidni_krampji_kronsteini/krampji.html', TemplateView.as_view(template_name="aizbidni_krampji_kronsteini/krampji.html"), name='krampji'),
    path('aizbidni_krampji_kronsteini/kronsteini.html', TemplateView.as_view(template_name="aizbidni_krampji_kronsteini/kronsteini.html"), name='kronsteini'),
    path('aizbidni_krampji_kronsteini/vartu.html', TemplateView.as_view(template_name="aizbidni_krampji_kronsteini/vartu.html"), name='vartu'),

    # Rokturi
    path('rokturi/dalitajam_uzlikam.html', TemplateView.as_view(template_name="rokturi/dalitajam_uzlikam.html"), name='dalitajam_uzlikam'),
    path('rokturi/garajam_uzlikam.html', TemplateView.as_view(template_name="rokturi/garajam_uzlikam.html"), name='garajam_uzlikam'),
    path('rokturi/skandinavu_rokturi.html', TemplateView.as_view(template_name="rokturi/skandinavu_rokturi.html"), name='skandinavu_rokturi'),
    path('rokturi/skavveida.html', TemplateView.as_view(template_name="rokturi/skavveida.html"), name='skavveida'),
    path('rokturi/centra.html', TemplateView.as_view(template_name="rokturi/centra.html"), name='centra'),
    path('rokturi/koka.html', TemplateView.as_view(template_name="rokturi/koka.html"), name='koka'),
    path('rokturi/stieni.html', TemplateView.as_view(template_name="rokturi/stieni.html"), name='stieni'),

    # Slēdzenes
    path('sledzenes/vacu_standarta.html', TemplateView.as_view(template_name="sledzenes/vacu_standarta.html"), name='vacu_standarta'),
    path('sledzenes/euro_standarta.html', TemplateView.as_view(template_name="sledzenes/euro_standarta.html"), name='euro_standarta'),
    path('sledzenes/skandinavu_standarta.html', TemplateView.as_view(template_name="sledzenes/euro_standarta.html"), name='skandinavu_standarta'),
    path('sledzenes/koda.html', TemplateView.as_view(template_name="sledzenes/euro_standarta.html"), name='koda'),
    path('sledzenes/pretplaksnes.html', TemplateView.as_view(template_name="sledzenes/euro_standarta.html"), name='pretplaksnes'),
    path('sledzenes/rulisu_mehanismi.html', TemplateView.as_view(template_name="sledzenes/euro_standarta.html"), name='rulisu_mehanismi'),
    path('sledzenes/starpistabu.html', TemplateView.as_view(template_name="sledzenes/euro_standarta.html"), name='starpistabu'),
    path('sledzenes/elbor.html', TemplateView.as_view(template_name="sledzenes/euro_standarta.html"), name='elbor'),

    # Cilindri
    path('cilindri/cilindri.html', TemplateView.as_view(template_name="cilindri/cilindri.html"), name='cilindri'),
    path('cilindri/uzlikas.html', TemplateView.as_view(template_name="cilindri/uzlikas.html"), name='uzlikas'),
    path('cilindri/wc.html', TemplateView.as_view(template_name="cilindri/wc.html"), name='wc'),
    path('cilindri/skandinavu_cilindri.html', TemplateView.as_view(template_name="cilindri/skandinavu_cilindri.html"), name='skandinavu_cilindri'),

    # Mēbeļu furnitūra
    path('mebelu_furnitura/enges.html', TemplateView.as_view(template_name="mebelu_furnitura/enges.html"), name='enges'),
    path('mebelu_furnitura/lodites.html', TemplateView.as_view(template_name="mebelu_furnitura/lodites.html"), name='lodites'),
    path('mebelu_furnitura/magneti.html', TemplateView.as_view(template_name="mebelu_furnitura/magneti.html"), name='magneti'),
    path('mebelu_furnitura/sledzenes.html', TemplateView.as_view(template_name="mebelu_furnitura/sledzenes.html"), name='sledzenes'),

    # Aksesuāri
    path('aksesuari/actinas.html', TemplateView.as_view(template_name="aksesuari/actinas.html"), name='actinas'),
    path('aksesuari/aizvereji.html', TemplateView.as_view(template_name="aksesuari/aizvereji.html"), name='aizvereji'),
    path('aksesuari/atdures.html', TemplateView.as_view(template_name="aksesuari/atdures.html"), name='atdures'),
    path('aksesuari/atsperes.html', TemplateView.as_view(template_name="aksesuari/atsperes.html"), name='atsperes'),
    path('aksesuari/pakaramie.html', TemplateView.as_view(template_name="aksesuari/pakaramie.html"), name='pakaramie'),
    path('aksesuari/paslimejosie_numurini.html', TemplateView.as_view(template_name="aksesuari/paslimejosie_numurini.html"), name='paslimejosie_numurini'),

    # Stiprinājumi
    path('stiprinajumi/margu_balsti.html', TemplateView.as_view(template_name="stiprinajumi/margu_balsti.html"), name='margu_balsti'),
    path('stiprinajumi/plauktu_lenki.html', TemplateView.as_view(template_name="stiprinajumi/plauktu_lenki.html"), name='plauktu_lenki'),


    # Par uzņēmumu
    path('par_uznemumu/vesture.html', TemplateView.as_view(template_name="par_uznemumu/vesture.html"), name='vesture'),
    path('par_uznemumu/kontakti.html', TemplateView.as_view(template_name="par_uznemumu/kontakti.html"), name='kontakti'),
    path('par_uznemumu/atrasanas_vieta.html', TemplateView.as_view(template_name="par_uznemumu/atrasanas_vieta.html"), name='atrasanas_vieta'),
    path('par_uznemumu/rekviziti.html', TemplateView.as_view(template_name="par_uznemumu/rekviziti.html"), name='rekviziti'),
    path('products/', views.product_list, name='product_list'),  # Changed URL pattern
]
