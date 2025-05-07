Branch, kas domāts lai skatītu lokāri datorā ar Docker ir izrādes main in priekš render.


Lai palasitu lokāli darbu jābūt instelētai un palaistā fonā Docker desktop programmai.
Komandas, kas jāpalaiž termināli lai vietne būtu skatāma lokāli.
Lai uzbūvētu docker containeru:
docker compose build

Lai palaistu konteinerus:
docker compose up

Lai izveidotu datubāzes shēmas un modeļus:
docker compose exec web python manage.py migrate

Lai importētu produktu katalogu no excel faila:
docker-compose exec web python manage.py import_products

Jāieliek pārlūkprogrammā lai apskatītu vietni:
http://localhost:8000/


Komandas, kas noder:
Restartē konteinerus:
docker-compose restart

Novāc konteinerus:
docker-compose down

Idzēš pilnīgi visu izveidoto Docker:
#docker system prune -a --volumes

Super admina izveide priekš admin paneļa lietošanas:
docker-compose exec web python manage.py createsuperuser



