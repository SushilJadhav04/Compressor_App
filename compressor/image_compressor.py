from PIL import Image
from io import BytesIO

def compress_image(uploaded_file, quality=60):
    image = Image.open(uploaded_file)
    img_io = BytesIO()

    # Convert PNG to RGB before saving as JPEG
    if image.format == "PNG":
        image = image.convert("RGB")

    image.save(img_io, format="JPEG", optimize=True, quality=quality)
    img_io.seek(0)
    return img_io
