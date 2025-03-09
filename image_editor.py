import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import face_recognition
import os

from image_editors.edit_black_n_white import apply_black_n_white_effect
from image_editors.edit_pop_art import apply_pop_art_effect

path = './images'
pathOut = './edited_images'

filters = {
    "Pop Art": apply_pop_art_effect,
    "Black White": apply_black_n_white_effect,
}

def process_images(image_filter):
    if image_filter in filters:
        os.makedirs(pathOut, exist_ok=True)
        for filename in os.listdir(path):
            img_path = os.path.join(path, filename)
            filters[image_filter](img_path, pathOut)
    else:
        print("No such filter")

print("Available Filters:", ", ".join(filters.keys()))
image_filter = input("Enter the desired image filter: ").strip()
process_images(image_filter)