from PIL import Image
from io import BytesIO

def compress_image(uploaded_file, target_size_kb=200):
    image = Image.open(uploaded_file)

    if image.mode != "RGB":
        image = image.convert("RGB")

    quality = 95
    img_io = BytesIO()

    while quality > 10:
        img_io.seek(0)
        img_io.truncate(0)

        image.save(img_io, format='JPEG', optimize=True, quality=quality)
        size_kb = len(img_io.getvalue()) / 1024

        if size_kb <= target_size_kb:
            break

        quality -= 5

    img_io.seek(0)
    return img_io
