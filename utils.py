import io

from PIL import Image


def to_Image(uploaded_file):
    image = Image.open(io.BytesIO(uploaded_file.read())).convert('RGB')
    return image


def load_Image(path: str):
    return Image.open(path).convert('RGB')
# def compare_images(img_first,img_second):
