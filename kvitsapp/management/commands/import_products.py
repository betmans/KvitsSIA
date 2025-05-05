import os
import openpyxl
from openpyxl_image_loader import SheetImageLoader
from django.core.management.base import BaseCommand
from django.conf import settings
from kvitsapp.models import Product, Category
from decimal import Decimal
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Import products from Excel and extract images'

    def _preprocess_image_mapping(self, sheet, image_loader):
        row_to_image = {}
        image_cells = {}
        for row in range(1, sheet.max_row + 1):
            for cell in sheet[row]:
                if not isinstance(cell, openpyxl.cell.cell.MergedCell):
                    cell_address = cell.coordinate
                    if image_loader.image_in(cell_address):
                        image_cells[cell_address] = (row, cell.column)

        for cell_address, (img_row, img_col) in image_cells.items():
            for merged_range in sheet.merged_cells.ranges:
                start_cell = sheet.cell(row=merged_range.min_row, column=merged_range.min_col)
                if start_cell.coordinate == cell_address:
                    for r in range(merged_range.min_row, merged_range.max_row + 1):
                        row_to_image[r] = cell_address
                    break
            else:
                row_to_image[img_row] = cell_address
                for r in range(img_row + 1, min(img_row + 5, sheet.max_row + 1)): #THis exactly
                    if r not in row_to_image:
                        if sheet.cell(row=r, column=1).value or sheet.cell(row=r, column=2).value:
                            has_own_image = False
                            for check_row in range(r, min(r + 3, sheet.max_row + 1)):
                                if check_row in row_to_image and check_row != img_row:
                                    has_own_image = True
                                    break
                            if not has_own_image:
                                row_to_image[r] = cell_address

        return row_to_image

    def _find_image_for_row(self, sheet, image_loader, row_index, row_to_image_map):
        if row_index in row_to_image_map:
            cell_address = row_to_image_map[row_index]
            is_merged = False
            for merged_range in sheet.merged_cells.ranges:
                if (merged_range.min_row <= row_index <= merged_range.max_row and
                    sheet.cell(row=merged_range.min_row, column=merged_range.min_col).coordinate == cell_address):
                    is_merged = True
                    break
            return cell_address, is_merged

        for check_row in range(row_index, max(1, row_index - 10), -1):
            for cell in sheet[check_row]:
                if not isinstance(cell, openpyxl.cell.cell.MergedCell):
                    cell_address = cell.coordinate
                    if image_loader.image_in(cell_address):
                        return cell_address, check_row != row_index

        return None, False

    def handle(self, *args, **kwargs):
        filepath = os.path.join('katalogs_2024.xlsx')
        output_folder = os.path.join(settings.BASE_DIR, 'kvitsapp', 'static', 'images')
        os.makedirs(output_folder, exist_ok=True)

        category_map = {
            "EL": "Klasiskās",
            "E100"  : "Klasiskās",
            "EM40"  : "Klasiskās",
            "EM50"  : "Klasiskās",
            "EM200"  : "Klasiskās",
            "E138"  : "Klasiskās",
            "E300"  : "Klasiskās",
            "E200"  : "Klasiskās",
            "EV": "Vārtu",
            "EM": "Metināmās",
            "ET": "T veida",
            "EK": "Klavieru",
            "EA100": "Atsper",
            "EA": "Antīkās",
            "DEKORS": "Antīkās",

            "AZ": "Aizbīdņi",
            "AA": "Aizbīdņi",
            "AZV": "Vārtiem",
            "AZ50": "Vārtiem",
            "AZ750": "Vārtiem",
            "AZ30": "Vārtiem",
            "S204": "Vārtiem",
            "AZ4": "Vārtiem",
            "AZ38": "Vārtiem",
            "KR": "Kronšteini",
            "AI": "Iekaļamie aizbīdņi",
            "KR100": "Krampji",
            "KR127": "Krampji",
            "KR250": "Krampji",


            "R21": "Garajām uzlikām",
            "R51": "Garajām uzlikām",
            "R31": "Garajām uzlikām",
            "R06": "Dalītajām uzlikām",
            "R26": "Dalītajām uzlikām",
            "R182": "Dalītajām uzlikām",
            "R199": "Dalītajām uzlikām",
            "R52": "Dalītajām uzlikām",
            "R41": "Dalītajām uzlikām",
            "R103S": "Dalītajām uzlikām",
            "R106S": "Dalītajām uzlikām",
            "R640": "Skandināvu rokturi",
            "R75": "Skavveida",
            "R100": "Skavveida",
            "R125": "Skavveida",
            "R150": "Skavveida",
            "R160": "Skavveida",
            "R162": "Skavveida",	
            "R175": "Skavveida",
            "R200": "Skavveida",
            "R212": "Skavveida",
            "R225": "Skavveida",
            "R230": "Skavveida",
            "R100MM": "Stieņi",
            "R150MM": "Stieņi",
            "RC": "Centra",
            "RL": "Lūkas",
            "RKOKA": "Koka",


            "S0": "Pretplāksnes",
            "S2": "Vācu standarta",
            "S.B": "Uzliekamās",
            "S45": "Starpistabu",
            "S155": "Rulīšu_mehanismi",
            "S55": "WC slēdzenes",
            "ASSA": "Skandināvu standarta",
            "S114": "Skandināvu standarta",
            "S40": "Universālās",
            "S85": "Eiro standarta",
            "S2018": "Profilcilindram",


            "C3": "Parastie",
            "CA": "Parastie",
            "C3": "Parastie",
            "C4": "Parastie",
            "CM": "Multi cilindri",
            "R0": "Uzlikas",
            "R113": "Uzlikas",
            "R115": "Uzlikas",
            "R02P": "Uzlikas",
            "R01PZSS": "Uzlikas",
            "R111": "WC",
            "R02": "WC",
            "R01": "WC",

            "SM": "Mēbeļu slēdzenes",
            "M5": "Magnēti",
            "L00": "Lodītes",

            "MB": "Margu balsti",
            "K": "Konsoles",

            "A20": "Actiņas",   
            "PD": "Piekaramās atslēgas",
            "N": "Numuriņi",
            "AT": "Atsperes",
            "KL": "Durvju aizvērēji",
            "A8": "Durvju aizvērēji",
            "PK": "Pakaramie",
            "KR4": "Pakaramie",
            "KR5": "Pakaramie",
            "A0": "Atdures",


        }

        try:
            wb = openpyxl.load_workbook(filepath, data_only=True)
            sheet = wb.active
            image_loader = SheetImageLoader(sheet)
            self.stdout.write(self.style.SUCCESS('Pre-processing sheet to map rows to images...'))
            row_to_image_map = self._preprocess_image_mapping(sheet, image_loader)
            self.stdout.write(self.style.SUCCESS(f'Found {len(row_to_image_map)} rows with associated images'))

            processed_images = {}
            cell_to_filename = {}

            for row_index, row in enumerate(sheet.iter_rows(min_row=2), start=2):
                try:
                    ean13 = row[0].value
                    pasutijuma_kods = row[1].value
                    if not pasutijuma_kods:
                        continue

                    apraksts = row[3].value
                    cena_raw_value = row[6].value

                    if cena_raw_value is not None:
                        try:
                            cena = Decimal(str(cena_raw_value).replace(',', '.'))
                        except (ValueError, TypeError):
                            continue
                    else:
                        continue

                    kod = str(pasutijuma_kods)
                    prefixes = [kod[:7], kod[:6], kod[:5], kod[:4], kod[:3], kod[:2], kod[:1]]  # Try longest possible matches first

                    for p in prefixes:
                        if p in category_map:
                            category_name = category_map[p]
                            break
                    else:
                        category_name = "Citi"
                    # prefix = str(pasutijuma_kods)[:2]
                    # category_name = category_map.get(prefix, "Citi")
                    category_slug = slugify(category_name)
                    category, _ = Category.objects.get_or_create(name=category_name, slug=category_slug)

                    cell_address, is_merged = self._find_image_for_row(sheet, image_loader, row_index, row_to_image_map)

                    if cell_address:
                        if cell_address in cell_to_filename:
                            attels_filename = cell_to_filename[cell_address]
                        else:
                            image = image_loader.get(cell_address)
                            filename = f"product_{pasutijuma_kods}.png"
                            image_path = os.path.join(output_folder, filename)
                            image.save(image_path)
                            attels_filename = f"images/{filename}"
                            cell_to_filename[cell_address] = attels_filename
                    else:
                        attels_filename = "images/no-image.png"

                    Product.objects.update_or_create(
                        pasutijuma_kods=pasutijuma_kods,
                        defaults={
                            'ean13': ean13 or '',
                            'attels': attels_filename,
                            'apraksts': apraksts or '',
                            'cena': cena,
                            'category': category.name  # Only save the category name
                        }
                    )

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing row {row_index}: {e}'))

            self.stdout.write(self.style.SUCCESS(f'Products imported successfully! Processed {len(cell_to_filename)} unique images.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: The file "{filepath}" was not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))




# docker-compose exec web python manage.py makemigrations kvitsapp
# docker-compose exec web python manage.py migrate


#docker-compose exec web python manage.py import_products
#docker-compose exec web python manage.py flush

#lai apskatītu datubāzi, var izmantot šādu komandu:
#docker-compose exec web bash
    # apt-get update
    # apt-get install -y postgresql-client
#psql -h db -U postgres
#postgres
#SELECT * FROM kvitsapp_product;
#\q