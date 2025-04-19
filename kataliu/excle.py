import openpyxl
from openpyxl_image_loader import SheetImageLoader
import os

# === CONFIG ===
xlsx_path = r"C:\Users\Oskar\Desktop\kvits.lv\kataliu\katalogs_2024.xlsx"
output_folder = r"C:\Users\Oskar\Desktop\kvits.lv\static\images"
# ==============

# Load workbook
wb = openpyxl.load_workbook(xlsx_path)
sheet = wb.active

image_loader = SheetImageLoader(sheet)

# Loop through rows
for row in range(2, sheet.max_row + 1):  # skip header row
    cell = f"C{row}"  # change C to the column letter where your image is
    if image_loader.image_in(cell):
        image = image_loader.get(cell)
        filename = f"image_row_{row}.png"
        path = os.path.join(output_folder, filename)
        image.save(path)
        print(f"✅ Saved {filename}")
    else:
        print(f"❌ No image in {cell}")
