from PIL import Image
from io import BytesIO

def compress_image(uploaded_file, quality=60):
    image = Image.open(uploaded_file)
    img_io = BytesIO()
    image.save(img_io, format=image.format, optimize=True, quality=quality)
    img_io.seek(0)
    return img_io
