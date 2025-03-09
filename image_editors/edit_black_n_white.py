import face_recognition
from PIL import Image, ImageEnhance, ImageFilter

import os

def apply_black_n_white_effect(img_path, output_path):
    bnw_folder = os.path.join(output_path, 'b&w')
    os.makedirs(bnw_folder, exist_ok=True)

    filename = os.path.basename(img_path)
    try:
        img = Image.open(img_path).convert('RGB')
        # convert to b&w
        bw_img = img.convert('L')

        # Detect Faces
        image_np = face_recognition.load_image_file(img_path)
        face_locations = face_recognition.face_locations(image_np)

        # Create mask with sharp faces
        mask = Image.new('L', img.size, 0)
        for (top, right, bottom, left) in face_locations:
            mask.paste(255, (left, top, right, bottom))

        # Defocus Background
        blurred_img = bw_img.filter(ImageFilter.GaussianBlur(radius=1.7))

        # Reduce Sharpness
        sharpness_enhancer = ImageEnhance.Sharpness(blurred_img)
        soft_img = sharpness_enhancer.enhance(0.9)

        # Merge faces with processed bg
        final_img = Image.composite(img, soft_img, mask)

        clean_name = os.path.splitext(filename)[0]
        final_img.save(os.path.join(bnw_folder, f"{clean_name}_b&w.jpg"))
    except Exception as e:
        print(f"Skipping {filename}: {e}")
