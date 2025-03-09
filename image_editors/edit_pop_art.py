from PIL import Image, ImageEnhance, ImageFilter, ImageOps

import os

def apply_pop_art_effect(img_path, output_path):
    pop_art_folder = os.path.join(output_path, 'pop_art')
    os.makedirs(pop_art_folder, exist_ok=True)

    filename = os.path.basename(img_path)
    try:
        img = Image.open(img_path).convert('RGB')

        # Enhance contrast
        img = ImageEnhance.Contrast(img).enhance(1.2)
        # Enhance color
        img = ImageEnhance.Color(img).enhance(1.6)
        # posterize
        img = ImageOps.posterize(img, 8)
        img = img.filter(ImageFilter.EDGE_ENHANCE)

        clean_name = os.path.splitext(filename)[0]
        img.save(os.path.join(pop_art_folder, f"{clean_name}_pop_art.jpg"))
    except Exception as e:
        print(f"Skipping {filename}: {e}")
