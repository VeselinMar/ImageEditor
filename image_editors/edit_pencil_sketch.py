import os
import cv2


def apply_pencil_sketch_effect(img_path, output_path):
    sketch_folder = os.path.join(output_path, "pencil_sketch")
    os.makedirs(sketch_folder, exist_ok=True)

    filename = os.path.basename(img_path)
    try:
        # Read image
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Invert the grayscale image
        inverted = cv2.bitwise_not(gray)

        # Apply Gaussian blur to the inverted image
        blurred = cv2.GaussianBlur(inverted, (21, 21), sigmaX=0, sigmaY=0)

        # Invert the blurred image
        inverted_blur = cv2.bitwise_not(blurred)

        # Pencil sketch formula: Divide grayscale by the inverted blurred image
        sketch = cv2.divide(gray, inverted_blur, scale=256.0)

        # Save the processed image
        clean_name = os.path.splitext(filename)[0]
        cv2.imwrite(os.path.join(sketch_folder, f"{clean_name}_sketch.jpg"), sketch)

    except Exception as e:
        print(f"Skipping {filename}: {e}")