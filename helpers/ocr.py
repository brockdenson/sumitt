import pytesseract
from PIL import Image
import os

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_chat_from_folder(folder_path):
    full_text = ""
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(folder_path, filename)
            full_text += extract_text_from_image(path) + "\n"
    return full_text.strip()
