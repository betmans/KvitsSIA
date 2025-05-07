Zars (branch), kas domāts, lai skatītu vietni lokāli datorā ar Docker, ir izstrādes zars. Savukārt main zars ir paredzēts vietnes atrašanās internetā ar Render.

Lai palaistu vietni lokāli, datorā ir jābūt instalētai un fonā palaistai Docker Desktop programmai.
Komandas, kas jāpalaiž terminālī, lai vietne būtu skatāma lokāli:

Lai uzbūvētu Docker konteineri:
docker compose build

Lai palaistu konteinerus:
docker compose up

Lai izveidotu datubāzes shēmas un modeļus:
docker compose exec web python manage.py migrate

Lai importētu produktu katalogu no Excel faila:
docker-compose exec web python manage.py import_products

Lai apskatītu vietni, pārlūkprogrammā jāievada:
http://localhost:8000/


Noderīgas komandas:

Restartē konteinerus:
docker-compose restart

Aptur un noņem konteinerus:
docker-compose down

Izdzēš pilnīgi visu Docker izveidoto (konteinerus, attēlus, tīklus un volumes):
#docker system prune -a --volumes

Superadministratora izveide admin paneļa lietošanai:
docker-compose exec web python manage.py createsuperuser


Datubāzei:

Izdzēst datus datubāzē:
docker-compose exec web python manage.py flush

Lai apskatītu datubāzi jāieliek šīs kommandas termināli pēc kārtas:
docker-compose exec web bash

    Vienreiž jāpalaiž lai būtu pieejams psql:
    apt-get update
    apt-get install -y postgresql-client

psql -h db -U postgres

postgres

SELECT * FROM kvitsapp_product;


Lai izietu no psql:
\q
