import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

import os

def apply_black_n_white_effect(img_path, output_path):
    bnw_folder = os.path.join(output_path, 'b&w')
    os.makedirs(bnw_folder, exist_ok=True)

    filename = os.path.basename(img_path)
    try:
        img = Image.open(img_path).convert('RGB')
        # convert to b&w
        img_np = np.array(img)

        # Convert to grayscale using NumPy
        bw_np = np.dot(img_np[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
        bw_img = Image.fromarray(bw_np)

        # Detect faces with a resized image for speed-up
        small_image = img_np[::2, ::2, :]
        face_locations = face_recognition.face_locations(small_image, model="hog")
        face_locations = [(top * 2, right * 2, bottom * 2, left * 2) for (top, right, bottom, left) in face_locations]

        # Create face mask
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        for (top, right, bottom, left) in face_locations:
            draw.rectangle([left, top, right, bottom], fill=255)

        # Apply Gaussian Blur with OpenCV
        blurred_np = cv2.GaussianBlur(bw_np, (5, 5), 1.7)
        blurred_img = Image.fromarray(blurred_np)

        # Reduce sharpness slightly
        soft_img = blurred_img.filter(ImageFilter.SMOOTH)

        # Merge faces with processed background
        final_img = Image.composite(img, soft_img, mask)

        clean_name = os.path.splitext(filename)[0]
        final_img.save(os.path.join(bnw_folder, f"{clean_name}_b&w.png"), optimize=True)
    except Exception as e:
        print(f"Skipping {filename}: {e}")
